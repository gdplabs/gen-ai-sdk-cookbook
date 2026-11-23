// ============================================================================
// SAMPLE: Hello - Simple greeting card
// ============================================================================
export const helloSample = [
  {
    version: "1.0",
    createSurface: {
      surfaceId: "main",
      catalogId: "https://github.com/GDP-ADMIN/glchat-sdk/blob/main/js/glchat-a2ui-react-renderer/json/v1_0/glchat_standard_catalog_definition.json"
    }
  },
  {
    version: "1.0",
    updateDataModel: {
      surfaceId: "main",
      value: {
        commands: [
          {
            command: "• 'typography' - **Text styles**"
          },
          {
            command: "• 'form' - _Input fields_"
          },
          {
            command: "• 'gallery' - Images"
          },
          {
            command: "• 'dashboard' - Stats layout"
          },
          {
            command: "• 'profile' - User profile"
          },
          {
            command: "• 'settings' - Config panel"
          },
          {
            command: "• 'hitl' - Approval flow"
          },
          {
            command: "• 'product' - Product card"
          },
          {
            command: "• 'layout' - Grid layouts"
          },
          {
            command: "• 'delete-surface' - Surface deletion (temporary)"
          },
          {
            command: "• 'components' - Full GLChat catalog (all 20 components)"
          }
        ]
      }
    }
  },
  {
    version: "1.0",
    updateComponents: {
      surfaceId: "main",
      components: [
        {
          id: "root",
          component: "Card",
          child: "content"
        },
        {
          id: "content",
          component: "Column",
          children: [
            "header",
            "description",
            "commandList",
            "divider",
            "footer"
          ],
          justify: "start",
          align: "stretch"
        },
        {
          id: "header",
          component: "Text",
          text: "## Hello! 👋"
        },
        {
          id: "description",
          component: "Text",
          text: "Welcome to A2UI! Try these commands:",
          variant: "body"
        },
        {
          id: "commandList",
          component: "List",
          children: {
            componentId: "commandItem",
            path: "/commands"
          },
          direction: "vertical",
          align: "start"
        },
        {
          id: "commandItem",
          component: "Text",
          text: {
            "@path": "command"
          },
          variant: "body"
        },
        {
          id: "divider",
          component: "Divider",
          axis: "horizontal"
        },
        {
          id: "footer",
          component: "Text",
          text: "Type any keyword above to see the demo!",
          variant: "caption"
        }
      ]
    }
  }
];
