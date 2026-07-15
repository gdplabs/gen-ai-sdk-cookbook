"use client";

import {
  type ActionPayload,
  A2UIMessage,
  SurfaceRenderer,
  Provider,
} from "glchat-a2ui-react-renderer";

export function A2UIContent({
  messages,
  onUserAction,
}: Readonly<{
  messages: A2UIMessage[];
  onUserAction?: (action: ActionPayload) => void;
}>) {
  const handleAction = (action: ActionPayload) => {
    onUserAction?.(action);
  };
  return (
    <Provider messages={messages} onAction={handleAction}>
      <SurfaceRenderer />
    </Provider>
  );
}
