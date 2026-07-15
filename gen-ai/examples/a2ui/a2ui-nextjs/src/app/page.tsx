"use client";

import ChatWindow from "@/components/ChatWindow";
import { useChat } from "@/hooks/useChat";

export default function Home() {
  const {
    messages,
    isLoading,
    streamingText,
    streamingA2UIMessages,
    sendMessage,
    a2uiVersion,
    changeA2uiVersion,
  } = useChat();

  return (
    <main className="h-screen overflow-hidden">
      <ChatWindow
        messages={messages}
        onSendMessage={sendMessage}
        isLoading={isLoading}
        streamingText={streamingText}
        streamingA2UIMessages={streamingA2UIMessages}
        a2uiVersion={a2uiVersion}
        onA2uiVersionChange={changeA2uiVersion}
      />
    </main>
  );
}
