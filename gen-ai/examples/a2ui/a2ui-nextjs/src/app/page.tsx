"use client";

import ChatWindow from "@/components/ChatWindow";
import { useChat } from "@/hooks/useChat";
import { injectStyles } from "@a2ui/react/styles";

injectStyles();

export default function Home() {
  const { messages, isLoading, streamingText, streamingA2UIMessages, sendMessage } = useChat();

  return (
    <main className="h-screen overflow-hidden">
      <ChatWindow
        messages={messages}
        onSendMessage={sendMessage}
        isLoading={isLoading}
        streamingText={streamingText}
        streamingA2UIMessages={streamingA2UIMessages}
      />
    </main>
  );
}
