import { useState, useCallback, useEffect, useRef } from "react";
import { simulateA2UIStream } from "@/utils/a2uiMockStream";
import { A2AResponse, A2UIVersion, ChatMessage } from "@/types/chat";
import { A2UIMessage } from "glchat-a2ui-react-renderer";

const initialUserMessage: ChatMessage = {
  id: "msg-init",
  role: "user",
  userMessage: "hello",
  timestamp: Date.now(),
};

export function useChat() {
  const [a2uiVersion, setA2uiVersionState] = useState<A2UIVersion>("0.9");
  const [messages, setMessages] = useState<ChatMessage[]>([initialUserMessage]);
  const [isLoading, setIsLoading] = useState(true);
  const [streamingText, setStreamingText] = useState("");
  const [streamingA2UIMessages, setStreamingA2UIMessages] = useState<A2UIMessage[]>([]);
  const versionRef = useRef(a2uiVersion);
  const streamIdRef = useRef(0);
  const hasInit = useRef(false);

  const streamCallbacks = useCallback(
    (streamId: number) => ({
      onMessageStream: (response: A2AResponse) => {
        if (streamId !== streamIdRef.current) return;
        const parts = response.result.status.message.parts;
        for (const part of parts) {
          if (part.kind === "text") {
            setStreamingText(part.text ?? "");
          } else if (part.kind === "data") {
            setStreamingA2UIMessages((prev) => [...prev, part.data as A2UIMessage]);
          }
        }
      },
      onComplete: (finalMessage: ChatMessage) => {
        if (streamId !== streamIdRef.current) return;
        setMessages((prev) => [...prev, finalMessage]);
        setStreamingText("");
        setStreamingA2UIMessages([]);
        setIsLoading(false);
      },
    }),
    []
  );

  const startHelloStream = useCallback(
    (version: A2UIVersion) => {
      const streamId = ++streamIdRef.current;
      setIsLoading(true);
      setStreamingText("");
      setStreamingA2UIMessages([]);
      void simulateA2UIStream(
        "hello",
        `msg-init-response-${streamId}`,
        streamCallbacks(streamId),
        version
      );
    },
    [streamCallbacks]
  );

  // Stream the initial "hello" response on mount
  useEffect(() => {
    if (hasInit.current) return;
    hasInit.current = true;
    startHelloStream(versionRef.current);
  }, [startHelloStream]);

  const setA2uiVersion = useCallback(
    (version: A2UIVersion) => {
      if (version === versionRef.current) return;
      versionRef.current = version;
      setA2uiVersionState(version);
      setMessages([{ ...initialUserMessage, id: `msg-init-${Date.now()}`, timestamp: Date.now() }]);
      startHelloStream(version);
    },
    [startHelloStream]
  );

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

      const streamId = ++streamIdRef.current;
      await simulateA2UIStream(
        content,
        `msg-${Date.now() + 1}`,
        streamCallbacks(streamId),
        versionRef.current
      );
    },
    [streamCallbacks]
  );

  return {
    messages,
    isLoading,
    streamingText,
    streamingA2UIMessages,
    sendMessage,
    a2uiVersion,
    setA2uiVersion,
  };
}
