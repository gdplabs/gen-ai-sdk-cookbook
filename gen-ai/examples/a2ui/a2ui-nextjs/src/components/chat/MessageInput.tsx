"use client";

import { useState, KeyboardEvent } from "react";
import { SendHorizontal } from "lucide-react";

interface MessageInputProps {
  onSendMessage: (content: string) => void;
  isLoading: boolean;
}

// ---- Send Button ----
function SendButton({ disabled, onClick }: { disabled: boolean; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className="absolute top-1/2 right-3 -translate-y-1/2 cursor-pointer rounded-lg p-1.5 text-gray-400 transition-colors hover:text-gray-700 disabled:cursor-not-allowed disabled:opacity-30"
    >
      <SendHorizontal size={18} />
    </button>
  );
}

// ---- Hint Text ----
function HintText() {
  return (
    <p className="mt-2 text-center text-xs text-gray-400">
      Press Enter to send · Shift+Enter for new line
    </p>
  );
}

// ---- Main MessageInput ----
export default function MessageInput({ onSendMessage, isLoading }: MessageInputProps) {
  const [input, setInput] = useState("");

  const handleSend = () => {
    const trimmed = input.trim();
    if (!trimmed || isLoading) return;
    onSendMessage(trimmed);
    setInput("");
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="border-t border-gray-200 bg-white p-4">
      <div className="relative mx-auto max-w-3xl">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Send simple message like 'show text'"
          rows={1}
          className="w-full resize-none rounded-xl border border-gray-300 bg-gray-100 px-4 py-3 pr-12 text-sm text-gray-900 placeholder-gray-400 focus:border-transparent focus:ring-2 focus:ring-blue-500 focus:outline-none"
        />
        <SendButton disabled={!input.trim() || isLoading} onClick={handleSend} />
      </div>
      <HintText />
    </div>
  );
}
