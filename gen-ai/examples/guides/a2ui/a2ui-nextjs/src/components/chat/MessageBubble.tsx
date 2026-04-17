"use client";

import { A2APart, ChatMessage } from "@/types/chat";
import { A2UIContent } from "./A2UIContent";
import { A2UIMessage } from "glchat-a2ui-react-renderer";
import { Bot, User } from "lucide-react";

// ---- Avatar ----
function Avatar({ isUser }: Readonly<{ isUser: boolean }>) {
  return (
    <div
      className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-white ${
        isUser ? "bg-blue-600" : "bg-emerald-600"
      }`}
    >
      {isUser ? <User size={16} /> : <Bot size={16} />}
    </div>
  );
}

// ---- Role Label ----
function RoleLabel({ isUser }: Readonly<{ isUser: boolean }>) {
  return <p className="mb-1 text-sm font-semibold text-gray-900">{isUser ? "You" : "Assistant"}</p>;
}

// ---- Text Content ----
function TextContent({
  text,
  isStreaming,
}: Readonly<{
  text: string;
  isStreaming?: boolean;
}>) {
  return (
    <div className="text-sm leading-relaxed whitespace-pre-wrap text-gray-700">
      {text}
      {isStreaming && <span className="ml-0.5 animate-pulse text-gray-400">▌</span>}
    </div>
  );
}

// ---- A2UI Content Block ----
function A2UIBlock({ messages }: Readonly<{ messages: object[] }>) {
  if (messages.length === 0) return null;

  return (
    <div className="mt-3">
      <A2UIContent
        messages={messages as A2UIMessage[]}
        onUserAction={(action) => {
          console.log("User action:", action);
        }}
      />
    </div>
  );
}

// ---- Main MessageBubble ----
interface MessageBubbleProps {
  message?: ChatMessage;
  streamingText?: string;
  streamingA2UIMessages?: object[];
}

export default function MessageBubble({
  message,
  streamingText,
  streamingA2UIMessages,
}: Readonly<MessageBubbleProps>) {
  const isUser = message?.role === "user";
  let textContent = "";
  let a2uiMessages: A2UIMessage[] = [];

  if (isUser) {
    textContent = message?.userMessage ?? "";
  } else {
    textContent =
      streamingText ??
      message?.a2aResponse?.result.status.message.parts
        .filter((p: A2APart) => p.kind === "text")
        ?.map((p: A2APart) => p.text ?? "")
        ?.join("") ??
      "";
    a2uiMessages =
      streamingA2UIMessages ??
      message?.a2aResponse?.result.status.message.parts
        .filter((p: A2APart) => p.kind === "data")
        ?.map((p: A2APart) => p.data as A2UIMessage) ??
      [];
  }
  const isStreamingText = !!streamingText && streamingA2UIMessages?.length === 0;

  return (
    <div className={`flex gap-4 px-4 py-6 ${isUser ? "" : "bg-gray-50"}`}>
      <Avatar isUser={isUser ?? false} />

      <div className="min-w-0 flex-1">
        <RoleLabel isUser={isUser ?? false} />

        {textContent && <TextContent text={textContent} isStreaming={isStreamingText} />}

        <A2UIBlock messages={a2uiMessages} />
      </div>
    </div>
  );
}
