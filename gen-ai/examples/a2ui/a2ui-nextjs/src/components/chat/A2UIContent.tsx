"use client";

import {
  A2UIMessage,
  A2UISurface,
  DispatchedEvent,
  useA2UIProcessor,
} from "glchat-a2ui-react-renderer";
import "glchat-a2ui-react-renderer/styles.css";
import { useEffect, useRef } from "react";

export function A2UIContent({
  messages,
  onUserAction,
}: Readonly<{
  messages: A2UIMessage[];
  onUserAction?: (event: DispatchedEvent) => void | Promise<A2UIMessage[]>;
}>) {
  const { processor, surfaces, refreshSurfaces } = useA2UIProcessor();

  useEffect(() => {
    if (!messages?.length) return;
    processor.processMessages(messages);
    refreshSurfaces();
  }, [messages, processor, refreshSurfaces]);

  const onUserActionRef = useRef(onUserAction);
  onUserActionRef.current = onUserAction;

  useEffect(() => {
    const unsubscribe = processor.events.subscribe(async (event) => {
      try {
        await onUserActionRef.current?.(event);
      } catch (err) {
        console.error("A2UI user action handling failed:", err);
      } finally {
        event.completion([]);
      }
    });
    return unsubscribe;
  }, [processor, refreshSurfaces]);

  if (surfaces.size === 0) return null;

  return (
    <>
      {Array.from(surfaces.entries()).map(([surfaceId, surface]) => (
        <A2UISurface
          key={surfaceId}
          refreshSurfaces={refreshSurfaces}
          processor={processor}
          surface={surface}
        />
      ))}
    </>
  );
}
