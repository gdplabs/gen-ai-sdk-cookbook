"use client";

import { type A2UIClientEventMessage, A2UIComponentProps, A2UIProvider, A2UIRenderer, ComponentRegistry, type ServerToClientMessage, StringValue, Surface, Types, useA2UI, useA2UIComponent } from "@a2ui/react";
import { useEffect, useMemo, useState } from "react";

type ButtonProperties = Types.ResolvedButton & {
  primary?: boolean;
  destructive?: boolean;
};
interface CustomButtonProps extends Types.ButtonNode {
  properties: ButtonProperties;
}

function CustomButton({ node, surfaceId }: Readonly<A2UIComponentProps<CustomButtonProps>>) {
  const { sendAction } = useA2UIComponent(node, surfaceId);

  const handleClick = () => {
    // Use the same action info the default button would
    const action = node.properties.action;
    if (action) {
      sendAction(action);
    }
  };


  const variant = useMemo(() => {
    if (node.properties.primary) return 'primary';
    if (node.properties.destructive) return 'destructive';
    return 'outline';
  }, [node.properties.primary, node.properties.destructive]);

  console.log('variant', variant);
  return <button onClick={handleClick}>Custom Button</button>;
}
interface TimeoutNode extends Types.CustomNode {
  type: "Timeout";
  properties: {
    targetTimeUtc: string;
  };
}

function Timeout({ node, surfaceId }: Readonly<A2UIComponentProps<TimeoutNode>>) {
  const { resolveString } = useA2UIComponent(node, surfaceId);
  console.log('node', node);
  console.log('surfaceId', surfaceId);
  const targetTimeUtc = node.properties.targetTimeUtc;
  console.log('targetTimeUtc', targetTimeUtc);
  const resolvedTargetTimeUtc = resolveString(targetTimeUtc as StringValue);
  console.log('resolvedTargetTimeUtc', resolvedTargetTimeUtc);
  return <div>Timeout: {resolvedTargetTimeUtc}</div>;
}

interface A2UIContentProps {
  messages: ServerToClientMessage[];
  onUserAction?: (action: A2UIClientEventMessage) => void;
}

export function A2UIContent(props: Readonly<A2UIContentProps>) {
  const handleAction = (action: A2UIClientEventMessage) => {
    props.onUserAction?.(action);
  }

  return (
    <A2UIProvider onAction={handleAction}>
      <Content {...props} />
    </A2UIProvider>
  )
}


function Content({ messages }: Readonly<A2UIContentProps>) {
  const { processMessages, getSurfaces, clearSurfaces } = useA2UI();
  const [surfaceEntries, setSurfaceEntries] = useState<[string, Surface][]>([]);
  const registry = ComponentRegistry.getInstance();

  useEffect(() => {
    registry.register("Button", { component: CustomButton });
    registry.register("Timeout", { component: Timeout });
  }, [registry]);

  useEffect(() => {
    clearSurfaces();
    processMessages(messages);
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setSurfaceEntries(Array.from(getSurfaces().entries()));
  }, [clearSurfaces, messages, processMessages, getSurfaces]);

  if (surfaceEntries.length === 0) return null;

  return (
    <section className="surfaces">
      {surfaceEntries.map(([surfaceId]) => (
        <A2UIRenderer key={surfaceId} surfaceId={surfaceId} />
      ))}
    </section>
  );
}