// ============================================================================
// SAMPLE: Hello - Simple greeting card
// ============================================================================
export const helloSample = [
  {
    version: "v0.9",
    createSurface: {
      surfaceId: "main",
      catalogId:
        "https://github.com/GDP-ADMIN/glchat-sdk/blob/main/js/glchat-a2ui-react-renderer/json/glchat_standard_catalog_definition.json",
    },
  },
  {
    version: "v0.9",
    updateDataModel: {
      surfaceId: "main",
      value: {
        commands: [
          {
            command: "• 'typography' - **Text styles**",
          },
          {
            command: "• 'form' - _Input fields_",
          },
          {
            command: "• 'gallery' - Images",
          },
          {
            command: "• 'dashboard' - Stats layout",
          },
          {
            command: "• 'profile' - User profile",
          },
          {
            command: "• 'settings' - Config panel",
          },
          {
            command: "• 'hitl' - Approval flow",
          },
          {
            command: "• 'product' - Product card",
          },
          {
            command: "• 'layout' - Grid layouts",
          },
          {
            command: "• 'delete-surface' - Surface deletion (temporary)",
          },
          {
            command: "• 'components' - Full GLChat catalog (all 20 components)",
          },
        ],
      },
    },
  },
  {
    version: "v0.9",
    updateComponents: {
      surfaceId: "main",
      components: [
        {
          id: "root",
          component: "Card",
          child: "content",
        },
        {
          id: "content",
          component: "Column",
          children: ["header", "description", "command-list", "divider", "footer"],
          justify: "start",
          align: "stretch",
        },
        {
          id: "header",
          component: "Text",
          text: "Hello! 👋",
          variant: "h2",
        },
        {
          id: "description",
          component: "Text",
          text: "Welcome to A2UI! Try these commands:",
          variant: "body",
        },
        {
          id: "command-list",
          component: "List",
          children: {
            componentId: "command-item",
            path: "/commands",
          },
          direction: "vertical",
          align: "start",
        },
        {
          id: "command-item",
          component: "Text",
          text: {
            path: "command",
          },
          variant: "body",
        },
        {
          id: "divider",
          component: "Divider",
          axis: "horizontal",
        },
        {
          id: "footer",
          component: "Text",
          text: "Type any keyword above to see the demo!",
          variant: "caption",
        },
      ],
    },
  },
];
