"use client";

import { A2UIMessage } from "glchat-a2ui-react-renderer";
import MessageBubble from "./MessageBubble";

interface StreamingBubbleProps {
  streamingText: string;
  streamingA2UIMessages: A2UIMessage[];
}

export default function StreamingBubble({
  streamingText,
  streamingA2UIMessages,
}: Readonly<StreamingBubbleProps>) {
  const isStreaming = !!(streamingText || streamingA2UIMessages.length > 0);
  if (!isStreaming) return null;

  return (
    <MessageBubble streamingText={streamingText} streamingA2UIMessages={streamingA2UIMessages} />
  );
}
