export interface A2APart {
  kind: "text" | "data";
  text?: string;
  data?: object;
  metadata?: { mimeType: string };
}

export interface A2AMessage {
  contextId: string;
  kind: "message";
  messageId: string;
  parts: A2APart[];
  role: "user" | "agent";
  taskId: string;
}

export interface A2AResponse {
  id: number;
  jsonrpc: string;
  result: {
    contextId: string;
    history: A2AMessage[];
    id: string;
    kind: "task";
    status: {
      message: A2AMessage;
      state: string;
      timestamp: string;
    };
  };
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  userMessage?: string;
  a2aResponse?: A2AResponse;
  timestamp: number;
}

export type SampleType =
  | "typography"
  | "form"
  | "gallery"
  | "dashboard"
  | "profile"
  | "settings"
  | "hitl"
  | "product"
  | "layout"
  | "delete-surface"
  | "hello";
