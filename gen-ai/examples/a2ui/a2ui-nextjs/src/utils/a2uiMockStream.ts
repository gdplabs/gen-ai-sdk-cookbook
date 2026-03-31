import { A2AMessage, A2APart, A2AResponse, ChatMessage } from "@/types/chat";
import { detectSampleType, getDeleteSurfaceAction, getMockMessage } from "./a2uiMockMessage";

export interface StreamCallbacks {
  onMessageStream: (message: A2AResponse) => void;
  onComplete: (finalMessage: ChatMessage) => void;
}

function createTextPart(text: string): A2APart {
  return { kind: "text", text };
}

function createA2UIDataPart(data: object): A2APart {
  return {
    data,
    kind: "data",
    metadata: { mimeType: "application/json+a2ui" },
  };
}

function createA2AResponse(
  contextId: string,
  taskId: string,
  messageId: string,
  parts: A2APart[],
  role: "user" | "agent" = "agent"
): A2AResponse {
  const message: A2AMessage = {
    contextId,
    kind: "message" as const,
    messageId,
    parts,
    role,
    taskId,
  };

  return {
    id: 1,
    jsonrpc: "2.0",
    result: {
      contextId,
      id: taskId,
      kind: "task" as const,
      history: [],
      status: {
        message,
        state: "input-required",
        timestamp: new Date().toISOString(),
      },
    },
  };
}

export async function simulateA2UIStream(
  userInput: string,
  messageId: string,
  callbacks: StreamCallbacks
) {
  const sampleType = detectSampleType(userInput);
  const rawA2UIMessages = getMockMessage(sampleType);

  const contextId = `ctx-${messageId}`;
  const taskId = `task-${messageId}`;
  const textContent = `Showing A2UI sample: ${userInput}`;

  // Stream text word by word
  const words = textContent.split(" ");
  for (let i = 0; i < words.length; i++) {
    await delay(50);
    const message = createTextPart(words.slice(0, i + 1).join(" "));
    callbacks.onMessageStream(createA2AResponse(contextId, taskId, messageId, [message]));
  }

  await delay(500);

  // Stream raw A2UI messages to the renderer, and collect wrapped data parts for the A2A response
  const statusParts: A2APart[] = [createTextPart(textContent)];

  for (const rawMsg of rawA2UIMessages) {
    statusParts.push(createA2UIDataPart(rawMsg));
    callbacks.onMessageStream(
      createA2AResponse(contextId, taskId, messageId, [createA2UIDataPart(rawMsg)])
    );
    await delay(300);
  }

  if (sampleType === "delete-surface") {
    await delay(3000);
    const deleteActions = getDeleteSurfaceAction();
    for (const action of deleteActions) {
      statusParts.push(createA2UIDataPart(action));
      callbacks.onMessageStream(
        createA2AResponse(contextId, taskId, messageId, [createA2UIDataPart(action)])
      );
    }
  }

  const finalMessage: ChatMessage = {
    id: messageId,
    role: "assistant",
    a2aResponse: createA2AResponse(contextId, taskId, messageId, statusParts),
    timestamp: Date.now(),
  };

  callbacks.onComplete(finalMessage);
}

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
