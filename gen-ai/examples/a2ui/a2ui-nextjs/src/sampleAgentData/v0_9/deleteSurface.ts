// ============================================================================
// SAMPLE: Delete Surface - Multiple surfaces with deletion
// ============================================================================
export const deleteSurfaceSample = [
    {
      version: "v0.9",
      createSurface: {
        surfaceId: "main",
        catalogId: "https://github.com/GDP-ADMIN/glchat-sdk/blob/main/js/glchat-a2ui-react-renderer/json/glchat_standard_catalog_definition.json",
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
            child: "main-content",
          },
          {
            id: "main-content",
            component: "Column",
            children: [
              "main-header",
              "main-body",
            ],
            justify: "start",
            align: "stretch",
          },
          {
            id: "main-header",
            component: "Text",
            text: "Main Surface",
            variant: "h3",
          },
          {
            id: "main-body",
            component: "Text",
            text: "This surface will remain after the temporary one is deleted.",
            variant: "body",
          },
        ],
      },
    },
    {
      version: "v0.9",
      createSurface: {
        surfaceId: "temporary",
        catalogId: "https://github.com/GDP-ADMIN/glchat-sdk/blob/main/js/glchat-a2ui-react-renderer/json/glchat_standard_catalog_definition.json",
      },
    },
    {
      version: "v0.9",
      updateComponents: {
        surfaceId: "temporary",
        components: [
          {
            id: "root",
            component: "Card",
            child: "temp-content",
          },
          {
            id: "temp-content",
            component: "Column",
            children: [
              "temp-header",
              "temp-body",
              "temp-countdown",
            ],
            justify: "start",
            align: "stretch",
          },
          {
            id: "temp-header",
            component: "Text",
            text: "⏱️ Temporary Surface",
            variant: "h3",
          },
          {
            id: "temp-body",
            component: "Text",
            text: "This surface will be automatically deleted in 3 seconds...",
            variant: "body",
          },
          {
            id: "temp-countdown",
            component: "Text",
            text: "Watch it disappear! 👀",
            variant: "caption",
          },
        ],
      },
    },
  ];
