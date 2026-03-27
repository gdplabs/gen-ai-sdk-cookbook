// ============================================================================
// SAMPLE: Hello - Simple greeting card
// ============================================================================
export const helloSample = [
  {
    surfaceUpdate: {
      surfaceId: "main",
      components: [
        {
          id: "root",
          component: {
            Card: { child: "content" },
          },
        },
        {
          id: "content",
          component: {
            Column: {
              children: { "explicitList": ["header", "description", "command-list", "divider", "footer"] },
              distribution: "start",
              alignment: "stretch",
            },
          },
        },
        {
          id: "header",
          component: {
            Text: {
              text: { literalString: "Hello! 👋" },
              usageHint: "h2",
            },
          },
        },
        {
          id: "description",
          component: {
            Text: {
              text: {
                literalString: "Welcome to A2UI! Try these commands:",
              },
              usageHint: "body",
            },
          },
        },
        {
          id: "command-list",
          component: {
            List: {
              children: {
                template: {
                  componentId: "command-item",
                  dataBinding: "/commands"
                },
              },
              direction: "vertical",
              alignment: "start"
            }
          },
        },
        {
          id: "command-item",
          component: {
            Text: {
              text: { path: "command" },
              usageHint: "body",
            },
          },
        },
        {
          id: "divider",
          component: {
            Divider: { axis: "horizontal" },
          },
        },
        {
          id: "footer",
          component: {
            Text: {
              text: {
                literalString: "Type any keyword above to see the demo!",
              },
              usageHint: "caption",
            },
          },
        },
      ],
    },
  },
  {
    dataModelUpdate: {
      surfaceId: "main",
      path: "/commands",
      contents: [
        {
          key: "0",
          valueMap: [
            { key: "command", valueString: "• 'typography' - Text styles" },
          ],
        },
        {
          key: "1",
          valueMap: [
            { key: "command", valueString: "• 'form' - Input fields" },
          ],
        },
        {
          key: "2",
          valueMap: [
            { key: "command", valueString: "• 'gallery' - Images" },
          ],
        },
        {
          key: "3",
          valueMap: [
            { key: "command", valueString: "• 'dashboard' - Stats layout" },
          ],
        },
        {
          key: "4",
          valueMap: [
            { key: "command", valueString: "• 'profile' - User profile" },
          ],
        },
        {
          key: "5",
          valueMap: [
            { key: "command", valueString: "• 'settings' - Config panel" },
          ],
        },
        {
          key: "6",
          valueMap: [
            { key: "command", valueString: "• 'hitl' - Approval flow" },
          ],
        },
        {
          key: "7",
          valueMap: [
            { key: "command", valueString: "• 'product' - Product card" },
          ],
        },
        {
          key: "8",
          valueMap: [
            { key: "command", valueString: "• 'layout' - Grid layouts" },
          ],
        },
        {
          key: "9",
          valueMap: [
            { key: "command", valueString: "• 'delete-surface' - Surface deletion (temporary)" },
          ],
        },
      ],
    }
  },
  {
    beginRendering: {
      surfaceId: "main",
      root: "root",
    },
  },
];
