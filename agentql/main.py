#!/usr/bin/env python3

"""This is an example of how to collect pricing data from e-commerce website using AgentQL."""

import asyncio
import json
import sys

from playwright.async_api import async_playwright

import agentql

# URL of the e-commerce website
# You can replace it with any other e-commerce website but the queries should be updated accordingly
URL = "https://wshop-spring-water-7013.fly.dev/"


async def main(mock_data):
    """Main function."""
    async with async_playwright() as playwright, await playwright.chromium.launch(
        # set headless to False to see the browser UI, useful for debugging and demo
        # set headless to True to run in the background, useful for automation
        # to toggle headless, change the value of headless to True or False
        # or use command line arguments, e.g. python main.py --headless=False
        # or use environment variables, e.g. HEADLESS=False python main.py
        headless=True
        # headless=False
    ) as browser:
        # Create a new page in the browser and wrap it to get access to the AgentQL's querying API
        page = await agentql.wrap_async(browser.new_page())
        await page.goto(URL)  # open the target URL

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
        response = await page.query_elements(form_query)

        await response.cardName.fill(mock_data["cardName"])
        await response.cardNumber.fill(mock_data["cardNumber"])
        await response.expDate.fill(mock_data["expDate"])
        await response.cvc.fill(mock_data["cvc"])
        await response.billingAddress.fill(mock_data["billingAddress"])
        await response.shippingAddress.fill(mock_data["shippingAddress"])

        # response = await page.query_elements(confirm_query)
        await response.buy_now_btn.click()

        await page.wait_for_page_ready_state()
        await page.wait_for_timeout(300)  # wait for 3 seconds
        response = await page.query_elements("{delivery_date}")
        delivery_date = (await response.delivery_date.text_content()) or ""
        result = {
            "delivery_date": delivery_date.strip(),
            "product": "artists_garden_at_giverny_monet",
        }
        return result


if __name__ == "__main__":
    # Load mock data from json file
    with open("../mock_data.json", "r") as f:
        mock_data = json.load(f)

    result = asyncio.run(main(mock_data))
    print(json.dumps(result))
