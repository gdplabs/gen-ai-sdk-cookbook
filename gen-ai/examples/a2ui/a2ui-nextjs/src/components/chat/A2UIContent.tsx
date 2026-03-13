"use client";

import {
  type A2UIAction,
  A2UIMessage,
  GlchatA2UIRenderer,
  GlchatA2UIProvider,
} from "glchat-a2ui-react-renderer";

export function A2UIContent({
  messages,
  onUserAction,
}: Readonly<{
  messages: A2UIMessage[];
  onUserAction?: (action: A2UIAction) => void;
}>) {
  const handleAction = (action: A2UIAction) => {
    onUserAction?.(action);
  }
  
  return (
    <GlchatA2UIProvider messages={messages}>
      <GlchatA2UIRenderer onAction={handleAction} />
    </GlchatA2UIProvider>
  )
}
