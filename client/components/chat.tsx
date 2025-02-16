"use client";

import { PreviewMessage, ThinkingMessage } from "@/components/message";
import { MultimodalInput } from "@/components/multimodal-input";
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
  [category: string]: Product[];
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

const sampleMessages: Message[] = [
  {
    id: "1",
    role: "user",
    content: [
      {
        type: "text",
        text: "I need help with my room",
      },
    ],
  },
  {
    id: "2",
    role: "assistant",
    content: [
      {
        type: "text",
        text: "Looking at your room, I'd rate it a 6/10 - it has good potential but needs some thoughtful touches! \n\nHere's what's working well:\n- Great natural light from your windows\n- Good room size\n- Nice hardwood floors\n\nTo elevate the space and make it more inviting, I'd recommend:\n1. The bed area looks a bit messy - let's make it the focal point with new bedding and proper pillows\n2. The blank wall across from your bed is perfect for some artwork to add personality\n3. You're missing ambient lighting - relying on just the ceiling light can feel harsh\n4. A small seating area would give guests a comfortable place sit besides the bed\n\nAdditionally, consider these cleanup tasks:\n- Make the bed with fresh sheets\n- Clear floor clutter\n- Organize visible cables\n- Add a hamper for dirty clothes\n\nI've selected some pieces that would transform your space: ",
      },
    ],
    shopResponse: {
      bedding: [
        {
          id: "bd-001",
          name: "Hotel Collection Duvet Set",
          description:
            "Crisp, hotel-quality cotton bedding that feels luxurious and looks sharp. Perfect for creating that put-together look.",
          price: 189.99,
          image_url: "https://example.com/images/bedding-001.jpg",
          placement:
            "On your bed - the white will brighten the room and look clean and fresh",
          // available_sizes: ["Twin", "Full", "Queen", "King"],
          color_options: ["Crisp White", "Soft Gray", "Navy"],
        },
      ],
      seating: [
        {
          id: "ch-001",
          name: "Modern Accent Chair",
          description:
            "Comfortable yet stylish chair that provides extra seating without taking up too much space",
          price: 299.99,
          image_url: "https://example.com/images/chair-001.jpg",
          placement:
            "In the corner near the window - creates a nice reading nook and gives guests a place to sit",
          dimensions: {
            width: 70,
            height: 85,
            depth: 75,
            unit: "cm",
          },
          color_options: ["Gray Velvet", "Navy Blue", "Forest Green"],
        },
      ],
      lighting: [
        {
          id: "lt-001",
          name: "Floor Lamp with Fabric Shade",
          description: "Warm, dimmable lighting that creates a cozy atmosphere",
          price: 129.99,
          image_url: "https://example.com/images/lamp-001.jpg",
          placement:
            "Next to the accent chair - perfect for reading or creating ambient lighting",
          color_options: ["Black/White Shade", "Brass/Beige Shade"],
        },
        {
          id: "lt-002",
          name: "String Lights",
          description: "Warm white LED string lights to add a magical touch",
          price: 29.99,
          image_url: "https://example.com/images/lights-002.jpg",
          placement:
            "Along the headboard or window - creates a warm, inviting atmosphere",
        },
      ],
      wall_decor: [
        {
          id: "art-001",
          name: "Abstract Canvas Print Set",
          description:
            "Set of 3 coordinating abstract prints that add color and interest",
          price: 159.99,
          image_url: "https://example.com/images/art-001.jpg",
          placement:
            "On the blank wall across from your bed - creates a focal point and add personality",
          dimensions: {
            width: 40,
            height: 60,
            unit: "cm",
          },
        },
      ],
      storage: [
        {
          id: "st-001",
          name: "Sleek Hamper with Lid",
          description: "Modern hamper that keeps laundry out of sight",
          price: 45.99,
          image_url: "https://example.com/images/hamper-001.jpg",
          placement: "In the corner near your closet",
          color_options: ["White", "Gray", "Black"],
        },
      ],
    },
  },
];

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

    // Random delay between 2-4 seconds
    const delay = Math.floor(Math.random() * 2000) + 4000;

    // Handle scripted responses
    setTimeout(async () => {
      let assistantResponse: Message;

      if (input.toLowerCase().includes("rate my room")) {
        assistantResponse = {
          id: crypto.randomUUID(),
          role: "assistant",
          content: `The image shows a bedroom with a bed, desk, chair, and bookshelf. The room
 is small and cozy, with a single bed against one wall and a desk and chair against another.
 Bookshelf is located in the corner of the room, and a window with white curtains is visible
 the back wall.

 To improve the comfort and functionality of the room, here are some suggestions:\n 1. Add a comfortable reading chair near the bookshelf to create a cozy reading nook.\n2. Place a floor lamp beside the reading chair for soft lighting and a warm ambiance.\n3. Hang a piece of artwork or a framed print above the bed or desk to personalize the space.\n4. Add a plant on the desk or bookshelf for a refreshing touch of greenery.\n5. Use a comfortable throw blanket to add both warmth and texture to the room.`,
        };
      } else if (input.toLowerCase().includes("art")) {
        assistantResponse = {
          id: crypto.randomUUID(),
          role: "assistant",
          content:
            "I recommend 'The Artist's Garden at Giverny' by Claude Monet. This masterpiece captures the serene beauty of Monet's garden with vibrant colors and impressionistic style. It would add a peaceful atmosphere to your room. The price is $450 for a high-quality reproduction.",
        };
      } else if (input.toLowerCase().includes("buy")) {
        assistantResponse = {
          id: crypto.randomUUID(),
          role: "assistant",
          content:
            "To proceed with the purchase of 'The Artist's Garden at Giverny', I'll need your card information. Please provide your card number, expiration date, and CVV.",
        };
      } else if (input.includes("card")) {
        assistantResponse = {
          id: crypto.randomUUID(),
          role: "assistant",
          content:
            "Thank you for your purchase! Your order has been confirmed. Tracking number is TR-2024-89321. Expected delivery: 5-7 business days. You'll receive an email confirmation shortly.",
        };
      } else {
        assistantResponse = {
          id: crypto.randomUUID(),
          role: "assistant",
          content:
            "I'm not sure how to respond to that. Could you please clarify your question?",
        };
      }

      setMessages((prevMessages) => [...prevMessages, assistantResponse]);
      setIsLoading(false);
    }, delay);

    try {
      // const response = await fetch("http://localhost:8000/api/chat", {
      //   method: "POST",
      //   headers: {
      //     "Content-Type": "application/json",
      //   },
      //   body: JSON.stringify({ messages: updatedMessages }),
      // });
      // const data = await response.json();
      // setMessages([
      //   ...updatedMessages,
      //   { id: crypto.randomUUID(), role: "assistant", content: data.content },
      // ]);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      // setIsLoading(false);
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
        {messages.length === 0 && (
          <div className="w-full grow mx-auto max-w-3xl px-4 flex flex-col gap-2 justify-center items-center">
            <p className="text-center text-2xl">Have people coming over?</p>
            <p className="text-center text-xl text-muted-foreground">
              Drop the image of your room and we&apos;ll tell you how to improve
              it!
            </p>
          </div>
        )}

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
