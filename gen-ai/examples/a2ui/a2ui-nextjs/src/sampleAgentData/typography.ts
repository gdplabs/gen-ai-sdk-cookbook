// ============================================================================
// SAMPLE: Typography - All text usage hints
// ============================================================================
export const typographySample = [
  {
    surfaceUpdate: {
      surfaceId: "main",
      components: [
        {
          id: "root",
          component: {
            Column: {
              children: {
                explicitList: [
                  "h1-text",
                  "h2-text",
                  "h3-text",
                  "h4-text",
                  "h5-text",
                  "divider-1",
                  "body-text",
                  "caption-text",
                ],
              },
              distribution: "start",
              alignment: "stretch",
            },
          },
        },
        {
          id: "h1-text",
          component: {
            Text: {
              text: { literalString: "Heading 1 - Main Title" },
              usageHint: "h1",
            },
          },
        },
        {
          id: "h2-text",
          component: {
            Text: {
              text: { literalString: "Heading 2 - Section Title" },
              usageHint: "h2",
            },
          },
        },
        {
          id: "h3-text",
          component: {
            Text: {
              text: { literalString: "Heading 3 - Subsection" },
              usageHint: "h3",
            },
          },
        },
        {
          id: "h4-text",
          component: {
            Text: {
              text: { literalString: "Heading 4 - Minor Heading" },
              usageHint: "h4",
            },
          },
        },
        {
          id: "h5-text",
          component: {
            Text: {
              text: { literalString: "Heading 5 - Small Heading" },
              usageHint: "h5",
            },
          },
        },
        {
          id: "divider-1",
          component: {
            Divider: { axis: "horizontal" },
          },
        },
        {
          id: "body-text",
          component: {
            Text: {
              text: {
                literalString:
                  "Body text is used for main content paragraphs. It provides comfortable reading for longer passages of text. This is the default style for most content.",
              },
              usageHint: "body",
            },
          },
        },
        {
          id: "caption-text",
          component: {
            Text: {
              text: {
                literalString:
                  "Caption text - Used for labels, hints, and supplementary information",
              },
              usageHint: "caption",
            },
          },
        },
      ],
    },
  },
  {
    beginRendering: {
      surfaceId: "main",
      root: "root",
    },
  },
];
