"use client";

import { ChatMessage } from "@/types/chat";
import { useAutoScroll } from "@/hooks/useAutoScroll";
import MessageList from "./chat/MessageList";
import StreamingBubble from "./chat/StreamingBubble";
import MessageInput from "./chat/MessageInput";

interface ChatWindowProps {
  messages: ChatMessage[];
  onSendMessage: (content: string) => void;
  isLoading: boolean;
  streamingText: string;
  streamingA2UIMessages: object[];
}

export default function ChatWindow({
  messages,
  onSendMessage,
  isLoading,
  streamingText,
  streamingA2UIMessages,
}: Readonly<ChatWindowProps>) {
  const messagesEndRef = useAutoScroll([messages, streamingText, streamingA2UIMessages]);
  const isStreaming = !!(streamingText || streamingA2UIMessages.length > 0);

  return (
    <div className="flex h-full flex-col bg-white">
      <div className="flex-1 overflow-y-auto pb-4">
        <div className="mx-auto max-w-3xl">
          <MessageList messages={messages} />
          <StreamingBubble
            streamingText={streamingText}
            streamingA2UIMessages={streamingA2UIMessages}
          />
          <div ref={messagesEndRef} />
        </div>
      </div>

      <MessageInput onSendMessage={onSendMessage} isLoading={isLoading || isStreaming} />
    </div>
  );
}
