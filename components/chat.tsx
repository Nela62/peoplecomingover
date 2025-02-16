"use client";

import { PreviewMessage, ThinkingMessage } from "@/components/message";
import { MultimodalInput } from "@/components/multimodal-input";
import { Overview } from "@/components/overview";
import { useScrollToBottom } from "@/hooks/use-scroll-to-bottom";
import { ToolInvocation } from "ai";
import { useChat } from "ai/react";
import { useState } from "react";
import { toast } from "sonner";

type TextContent = {
  type: "text";
  text: string;
};

type ImageContent = {
  type: "image_url";
  image_url: {
    name: string;
    url: string;
  };
};

type Product = {
  id: string;
  name: string;
  description: string;
  price: number;
  image_url: string;
  placement?: string;
  color_options?: string[];
  dimensions?: {
    width: number;
    height: number;
    depth?: number;
    unit: string;
  };
};

type ShopResponse = {
  analysis: {
    text: string;
    cleanup_tasks: string[];
  };
  recommendations: {
    [category: string]: Product[];
  };
};

type Content = TextContent | ImageContent;

export type Message = {
  id: string;
  role: "user" | "assistant" | "system";
  content: string | Content[];
  toolInvocations?: ToolInvocation[];
  shopResponse?: ShopResponse;
};

export const isTextContent = (content: Content): content is TextContent =>
  content.type === "text";

export const isImageContent = (content: Content): content is ImageContent =>
  content.type === "image_url";

export function Chat() {
  const chatId = "001";

  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [input, setInput] = useState("");
  const [files, setFiles] = useState<File[]>([]);

  function convertToBase64(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();

      reader.onloadend = () => {
        const base64String = reader.result;
        if (base64String) {
          resolve(base64String.toString());
        } else {
          reject(new Error("Failed to convert file to Base64."));
        }
      };

      reader.onerror = (error) => {
        reject(error);
      };

      reader.readAsDataURL(file);
    });
  }

  const handleSubmit = async (event?: { preventDefault?: () => void }) => {
    setIsLoading(true);
    const id = crypto.randomUUID();
    let userMessage: Message;
    const base64Images: ImageContent[] = await Promise.all(
      files.map(async (file) => {
        const base64 = await convertToBase64(file);
        return {
          type: "image_url",
          image_url: {
            name: file.name,
            url: base64,
          },
        };
      })
    );

    if (files.length > 0) {
      userMessage = {
        id,
        role: "user",
        content: [
          {
            type: "text",
            text: input,
          },
          ...base64Images,
        ],
      };
    } else {
      userMessage = { id, role: "user", content: input };
    }

    // Update your messages state
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInput("");
    setFiles([]);

    try {
      console.log("updatedMessages", updatedMessages);
      const response = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ messages: updatedMessages }),
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
