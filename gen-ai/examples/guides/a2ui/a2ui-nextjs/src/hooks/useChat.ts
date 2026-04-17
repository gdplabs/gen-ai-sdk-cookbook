import { useState, useCallback, useEffect, useRef } from "react";
import { simulateA2UIStream } from "@/utils/a2uiMockStream";
import { A2AResponse, ChatMessage } from "@/types/chat";

const initialMessage: ChatMessage = {
  id: "msg-init",
  role: "user",
  userMessage: "hello",
  timestamp: Date.now(),
};

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([initialMessage]);
  const [isLoading, setIsLoading] = useState(true);
  const [streamingText, setStreamingText] = useState("");
  const [streamingA2UIMessages, setStreamingA2UIMessages] = useState<object[]>([]);
  const hasInit = useRef(false);

  const streamCallbacks = useCallback(
    () => ({
      onMessageStream: (response: A2AResponse) => {
        const parts = response.result.status.message.parts;
        for (const part of parts) {
          if (part.kind === "text") {
            setStreamingText(part.text ?? "");
          } else if (part.kind === "data") {
            setStreamingA2UIMessages((prev) => [...prev, part.data as object]);
          }
        }
      },
      onComplete: (finalMessage: ChatMessage) => {
        setMessages((prev) => [...prev, finalMessage]);
        setStreamingText("");
        setStreamingA2UIMessages([]);
        setIsLoading(false);
      },
    }),
    []
  );

  // Stream the initial "hello" response on mount
  useEffect(() => {
    if (hasInit.current) return;
    hasInit.current = true;

    simulateA2UIStream("hello", "msg-init-response", streamCallbacks());
  }, [streamCallbacks]);

  const sendMessage = useCallback(
    async (content: string) => {
      const userMessage: ChatMessage = {
        id: `msg-${Date.now()}`,
        role: "user",
        userMessage: content,
        timestamp: Date.now(),
      };

      setMessages((prev) => [...prev, userMessage]);
      setIsLoading(true);
      setStreamingText("");
      setStreamingA2UIMessages([]);

      await simulateA2UIStream(content, `msg-${Date.now() + 1}`, streamCallbacks());
    },
    [streamCallbacks]
  );

  return { messages, isLoading, streamingText, streamingA2UIMessages, sendMessage };
}
