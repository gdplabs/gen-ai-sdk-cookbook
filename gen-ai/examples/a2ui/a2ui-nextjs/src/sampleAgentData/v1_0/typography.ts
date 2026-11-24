// ============================================================================
// SAMPLE: Typography - All text usage hints
// ============================================================================
export const typographySample = [
  {
    version: "1.0",
    createSurface: {
      surfaceId: "main",
      catalogId: "https://a2ui.org/specification/v1_0/catalogs/basic/catalog.json"
    }
  },
  {
    version: "1.0",
    updateComponents: {
      surfaceId: "main",
      components: [
        {
          id: "root",
          component: "Column",
          children: [
            "h1Text",
            "h2Text",
            "h3Text",
            "h4Text",
            "h5Text",
            "divider1",
            "bodyText",
            "captionText"
          ],
          justify: "start",
          align: "stretch"
        },
        {
          id: "h1Text",
          component: "Text",
          text: "# Heading 1 - Main Title"
        },
        {
          id: "h2Text",
          component: "Text",
          text: "## Heading 2 - Section Title"
        },
        {
          id: "h3Text",
          component: "Text",
          text: "### Heading 3 - Subsection"
        },
        {
          id: "h4Text",
          component: "Text",
          text: "#### Heading 4 - Minor Heading"
        },
        {
          id: "h5Text",
          component: "Text",
          text: "##### Heading 5 - Small Heading"
        },
        {
          id: "divider1",
          component: "Divider",
          axis: "horizontal"
        },
        {
          id: "bodyText",
          component: "Text",
          text: "Body text is used for main content paragraphs. It provides comfortable reading for longer passages of text. This is the default style for most content.",
          variant: "body"
        },
        {
          id: "captionText",
          component: "Text",
          text: "Caption text - Used for labels, hints, and supplementary information",
          variant: "caption"
        }
      ]
    }
  }
];
