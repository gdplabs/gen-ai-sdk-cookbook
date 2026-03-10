"use client";

import { A2UIAction, A2UIProvider, A2UIRenderer, A2UIMessage, standardCatalog } from "@a2ui-sdk/react/0.8";
import { CustomButtonComponent } from "../custom/Button";

export function A2UIContent({
  messages,
  onUserAction,
}: Readonly<{
  messages: A2UIMessage[];
  onUserAction?: (event: A2UIAction) => void;
}>) {
  const handleAction = (action: A2UIAction) => {
    onUserAction?.(action);
  }

  // Extend standard catalog with custom components
const customCatalog = {
  ...standardCatalog,
  components: {
    ...standardCatalog.components,
    // Override default components or add new ones
    Button: CustomButtonComponent,
  },
}

  return (
    <A2UIProvider messages={messages} catalog={customCatalog}>
      <A2UIRenderer onAction={handleAction} />
    </A2UIProvider>
  )
}
