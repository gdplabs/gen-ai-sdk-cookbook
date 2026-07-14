"use client";

import type { A2UIVersion, ChatMessage } from "@/types/chat";
import { useAutoScroll } from "@/hooks/useAutoScroll";
import MessageList from "./chat/MessageList";
import StreamingBubble from "./chat/StreamingBubble";
import MessageInput from "./chat/MessageInput";
import type { A2UIMessage } from "glchat-a2ui-react-renderer";

interface ChatWindowProps {
  messages: ChatMessage[];
  onSendMessage: (content: string) => void;
  isLoading: boolean;
  streamingText: string;
  streamingA2UIMessages: A2UIMessage[];
  a2uiVersion: A2UIVersion;
  onA2uiVersionChange: (version: A2UIVersion) => void;
}

export default function ChatWindow({
  messages,
  onSendMessage,
  isLoading,
  streamingText,
  streamingA2UIMessages,
  a2uiVersion,
  onA2uiVersionChange,
}: Readonly<ChatWindowProps>) {
  const messagesEndRef = useAutoScroll([messages, streamingText, streamingA2UIMessages]);
  const isStreaming = !!(streamingText || streamingA2UIMessages.length > 0);
  const selectorDisabled = isLoading || isStreaming;

  return (
    <div className="flex h-full flex-col bg-white">
      <div className="border-b border-gray-200 bg-white px-4 py-3">
        <div className="mx-auto flex max-w-3xl items-center justify-between gap-4">
          <div>
            <p className="text-sm font-semibold text-gray-900">A2UI Chat Assistant</p>
            <p className="text-xs text-gray-500">Switch A2UI schema version for sample payloads</p>
          </div>
          <label className="flex items-center gap-2 text-xs text-gray-600">
            <span className="whitespace-nowrap">A2UI Version</span>
            <select
              aria-label="A2UI protocol version"
              value={a2uiVersion}
              disabled={selectorDisabled}
              onChange={(e) => onA2uiVersionChange(e.target.value as A2UIVersion)}
              className="rounded-md border border-gray-200 bg-white px-2.5 py-1.5 text-xs font-medium text-gray-900 outline-none focus:border-gray-400 disabled:cursor-not-allowed disabled:opacity-50"
            >
              <option value="0.8">0.8</option>
              <option value="0.9">0.9</option>
            </select>
          </label>
        </div>
      </div>

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
