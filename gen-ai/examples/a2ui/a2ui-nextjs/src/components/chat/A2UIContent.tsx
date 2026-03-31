"use client";

import {
  type ActionPayload,
  A2UIComponentProps,
  A2UIMessage,
  AllSurfacesRenderer,
  Provider,
  Types,
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
      {/* <div className="border border-primary p-4 bg-card">test</div> */}

      <AllSurfacesRenderer />
    </Provider>
  );
}
