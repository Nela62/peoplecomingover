"use client";

import { PreviewMessage, ThinkingMessage } from "@/components/message";
import { MultimodalInput } from "@/components/multimodal-input";
import { Overview } from "@/components/overview";
import { useScrollToBottom } from "@/hooks/use-scroll-to-bottom";
import { ToolInvocation } from "ai";
import { useChat } from "ai/react";
import { useState } from "react";
import { toast } from "sonner";

export type Message = {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
};

export function Chat() {
  const chatId = "001";

  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [input, setInput] = useState("");
  const [files, setFiles] = useState<File[]>([]);

  const handleSubmit = async (event?: { preventDefault?: () => void }) => {
    setIsLoading(true);
    const id = crypto.randomUUID();
    const userMessage: Message = { id, role: "user", content: input };

    // Update your messages state
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInput("");

    // Create FormData and append your messages and files
    const formData = new FormData();
    formData.append("messages", JSON.stringify(updatedMessages));
    // Append each file (if any) with the same key (FastAPI will treat these as a list)
    files.forEach((file) => formData.append("files", file));

    try {
      const response = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      setMessages([
        ...updatedMessages,
        { id: crypto.randomUUID(), role: "assistant", content: data.content },
      ]);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const append = (message: Message) => {
    setMessages((messages) => [...messages, message]);
    handleSubmit();
    return Promise.resolve(null);
  };

  const [messagesContainerRef, messagesEndRef] =
    useScrollToBottom<HTMLDivElement>();

  return (
    <div className="flex flex-col min-w-0 h-[calc(100dvh-52px)] bg-background">
      <div
        ref={messagesContainerRef}
        className="flex flex-col min-w-0 gap-6 flex-1 overflow-y-scroll pt-4"
      >
        {messages.length === 0 && <Overview />}

        {messages.map((message, index) => (
          <PreviewMessage
            key={message.id}
            chatId={chatId}
            message={message}
            isLoading={isLoading && messages.length - 1 === index}
          />
        ))}

        {isLoading &&
          messages.length > 0 &&
          messages[messages.length - 1].role === "user" && <ThinkingMessage />}

        <div
          ref={messagesEndRef}
          className="shrink-0 min-w-[24px] min-h-[24px]"
        />
      </div>

      <form className="flex mx-auto px-4 bg-background pb-4 md:pb-6 gap-2 w-full md:max-w-3xl">
        <MultimodalInput
          chatId={chatId}
          input={input}
          setInput={setInput}
          handleSubmit={handleSubmit}
          isLoading={isLoading}
          // stop={stop}
          messages={messages}
          setMessages={setMessages}
          append={append}
          files={files}
          setFiles={setFiles}
        />
      </form>
    </div>
  );
}
