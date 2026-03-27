"use client";

import {
  type ActionPayload,
  A2UIComponentProps,
  A2UIMessage,
  AllSurfacesRenderer,
  ComponentRegistry,
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
  }


  console.log(messages);

  const registry = ComponentRegistry.getInstance();
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  registry.register('MyNodeType', { component: MyNodeComponent as any });
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  // registry.register('Button', { component: ButtonComponent as any });
  
  return (
    <Provider messages={messages} onAction={handleAction}>
      {/* <div className="border border-primary p-4 bg-card">test</div> */}

      <AllSurfacesRenderer />
    </Provider>
  )
}

function MyNodeComponent({ node }: Readonly<A2UIComponentProps<Types.CustomNode>>) {
  const label = (node.properties as Record<string, unknown>).label as string | undefined;
  return <div>ini label tambahan kak: {label}</div>;
}

function ButtonComponent({ node }: Readonly<A2UIComponentProps<Types.Button>>) {
  const label = (node.properties as Record<string, unknown>).label as string | undefined;
  return <button>button bikin sendiri: {label}</button>;
}
