import asyncio
import json
import os
import sys
import traceback
import uuid
from typing import Optional

import agentql
import uvicorn
from fastapi import FastAPI
from hyperpocket.tool import from_git, function_tool
from hyperpocket_langgraph import PocketLanggraph
from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import tools_condition
from langgraph.types import Command
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
from pydantic import BaseModel
from starlette.responses import StreamingResponse


@function_tool
def fill_payment():
    """
    fill_payment is a tool that fills the payment form on an e-commerce website and orders the product.
    It fills in a name, credit card info, billing address, and shipping address. Then it buys the product. Then it returns the delivery date.
    """
    # URL of the e-commerce website
    # You can replace it with any other e-commerce website but the queries should be updated accordingly
    store_url = "https://wshop-spring-water-7013.fly.dev/"
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True
            # headless=False
        )
        # Create a new page in the browser and wrap it to get access to the AgentQL's querying API
        page = agentql.wrap(browser.new_page())
        page.goto(store_url)  # open the target URL

        form_query = """
{
    cardName
    cardNumber
    expDate
    cvc
    billingAddress
    shippingAddress
    buy_now_btn
    delivery_date
}
        """
        response = page.query_elements(form_query)

        response.cardName.fill("Kirill Igumenshchev")
        response.cardNumber.fill("4111 1111 1111 1111")
        response.expDate.fill("12/25")
        response.cvc.fill("123")
        response.billingAddress.fill("123 Elm Street, Springfield, IL, 62704")
        response.shippingAddress.fill("456 Oak Avenue, Springfield, IL, 62704")

        # response = page.query_elements(confirm_query)
        response.buy_now_btn.click()

        page.wait_for_page_ready_state()
        page.wait_for_timeout(300)  # wait for 3 seconds
        response = page.query_elements("{delivery_date}")
        delivery_date = response.delivery_date.text_content() or ""
        # result = {
        #     "delivery_date": delivery_date.strip(),
        #     "product": "artists_garden_at_giverny_monet",
        # }
        return delivery_date.strip()


def build():
    pocket = PocketLanggraph(
        tools=[
            fill_payment,
        ]
    )

    llm = ChatOpenAI(
        model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"), streaming=True
    )
    llm_with_tools = llm.bind_tools(pocket.get_tools())

    graph_builder = StateGraph(MessagesState)

    def agent(state) -> dict:
        print("---CALL AGENT---")
        messages = state["messages"]
        msg = [
            SystemMessage(
                content="""
If you think you're done with the user's request, just express appreciation and ask
if there is anything else you can help with.
"""
            )
        ]
        response = llm_with_tools.invoke(messages + msg)
        print(response)
        return {"messages": [response]}

    async def rewrite(state) -> dict:
        print("---TRANSFORM TOOL MESSAGE---")
        messages = state["messages"]
        question = messages[0].content
        tool_resp = messages[-1].content
        msg = [
            SystemMessage(
                content=f"""
Look at the input and try to reason about the underlying semantic intent / meaning.
Here is the initial question:

---
{question}
---

By your understanding, you decided to invoke a tool and you got the following response:

---
{tool_resp}
---

Answer the user what you did with the tool. It is, you have to explain what you have done,
and what is the result of the tool invocation, in a more human-friendly way.
Think twice about the context and the user's needs.
                """
            )
        ]
        response = await llm.ainvoke(messages + msg)
        return {"messages": [response]}

    graph_builder.add_node("agent", agent)
    graph_builder.add_node("tools", pocket.get_tool_node(should_interrupt=True))
    graph_builder.add_node("rewrite", rewrite)

    graph_builder.add_edge(START, "agent")
    graph_builder.add_conditional_edges(
        "agent",
        tools_condition,
        {
            "tools": "tools",
            END: END,
        },
    )
    graph_builder.add_edge("tools", "rewrite")
    graph_builder.add_edge("rewrite", "agent")

    memory = MemorySaver()
    return graph_builder.compile(checkpointer=memory)


def server_example(graph):
    app = FastAPI()

    class Body(BaseModel):
        message: str
        thread_id: Optional[str] = None

    class Response(BaseModel):
        content: str
        type: str

    conversation_paused = {}

    @app.post("/chat")
    async def chat(body: Body) -> StreamingResponse:
        async def generate(_cfg: RunnableConfig = None):
            try:
                if conversation_paused.get(_cfg["configurable"]["thread_id"], False):
                    conversation_paused.pop(_cfg["configurable"]["thread_id"])
                    async for _, chunk in graph.astream(
                        Command(resume={"action": "continue"}),
                        config=_cfg,
                        stream_mode="updates",
                        subgraphs=True,
                    ):
                        if intr := chunk.get("__interrupt__"):
                            conversation_paused[_cfg["configurable"]["thread_id"]] = (
                                True
                            )
                            result = Response(content=intr[0].value, type="system")
                            yield result.model_dump_json() + "\n"
                        else:
                            message = list(chunk.values())[0]["messages"][-1]
                            if (
                                message.type == "ai"
                                and message.content is not None
                                and message.content != ""
                            ):
                                result = Response(
                                    content=message.content, type=message.type
                                )
                                yield result.model_dump_json() + "\n"
                else:
                    async for _, chunk in graph.astream(
                        {"messages": [("user", body.message)]},
                        config=_cfg,
                        stream_mode="updates",
                        subgraphs=True,
                    ):
                        if intr := chunk.get("__interrupt__"):
                            conversation_paused[_cfg["configurable"]["thread_id"]] = (
                                True
                            )
                            result = Response(content=intr[0].value, type="system")
                            yield result.model_dump_json() + "\n"
                        else:
                            message = list(chunk.values())[0]["messages"][-1]
                            if (
                                message.type == "ai"
                                and message.content is not None
                                and message.content != ""
                            ):
                                result = Response(
                                    content=message.content, type=message.type
                                )
                                yield result.model_dump_json() + "\n"
            except Exception as e:
                print(traceback.print_exc())
                yield {"error": str(e)}

        thread_id = body.thread_id if body.thread_id else str(uuid.uuid4())
        config = RunnableConfig(
            recursion_limit=30,
            configurable={"thread_id": thread_id},
        )
        return StreamingResponse(
            generate(config),
            media_type="text/event-stream",
            headers={"X-Pocket-Langgraph-Thread-Id": thread_id},
        )

    uvicorn.run(app, host="0.0.0.0", port=8008)


def main():
    server_example(build())


if __name__ == "__main__":
    main()
