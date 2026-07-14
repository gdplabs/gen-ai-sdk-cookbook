// ============================================================================
// SAMPLE: Typography - All text usage hints
// ============================================================================
export const typographySample = [
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
            component: "Column",
            children: [
              "h1-text",
              "h2-text",
              "h3-text",
              "h4-text",
              "h5-text",
              "divider-1",
              "body-text",
              "caption-text",
            ],
            justify: "start",
            align: "stretch",
          },
          {
            id: "h1-text",
            component: "Text",
            text: "Heading 1 - Main Title",
            variant: "h1",
          },
          {
            id: "h2-text",
            component: "Text",
            text: "Heading 2 - Section Title",
            variant: "h2",
          },
          {
            id: "h3-text",
            component: "Text",
            text: "Heading 3 - Subsection",
            variant: "h3",
          },
          {
            id: "h4-text",
            component: "Text",
            text: "Heading 4 - Minor Heading",
            variant: "h4",
          },
          {
            id: "h5-text",
            component: "Text",
            text: "Heading 5 - Small Heading",
            variant: "h5",
          },
          {
            id: "divider-1",
            component: "Divider",
            axis: "horizontal",
          },
          {
            id: "body-text",
            component: "Text",
            text: "Body text is used for main content paragraphs. It provides comfortable reading for longer passages of text. This is the default style for most content.",
            variant: "body",
          },
          {
            id: "caption-text",
            component: "Text",
            text: "Caption text - Used for labels, hints, and supplementary information",
            variant: "caption",
          },
        ],
      },
    },
  ];
