// ============================================================================
// SAMPLE: Delete Surface - Multiple surfaces with deletion
// ============================================================================
export const deleteSurfaceSample = [
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
          component: "Card",
          child: "mainContent"
        },
        {
          id: "mainContent",
          component: "Column",
          children: [
            "mainHeader",
            "mainBody"
          ],
          justify: "start",
          align: "stretch"
        },
        {
          id: "mainHeader",
          component: "Text",
          text: "### Main Surface"
        },
        {
          id: "mainBody",
          component: "Text",
          text: "This surface will remain after the temporary one is deleted.",
          variant: "body"
        }
      ]
    }
  },
  {
    version: "1.0",
    createSurface: {
      surfaceId: "temporary",
      catalogId: "https://a2ui.org/specification/v1_0/catalogs/basic/catalog.json"
    }
  },
  {
    version: "1.0",
    updateComponents: {
      surfaceId: "temporary",
      components: [
        {
          id: "root",
          component: "Card",
          child: "tempContent"
        },
        {
          id: "tempContent",
          component: "Column",
          children: [
            "tempHeader",
            "tempBody",
            "tempCountdown"
          ],
          justify: "start",
          align: "stretch"
        },
        {
          id: "tempHeader",
          component: "Text",
          text: "### ⏱️ Temporary Surface"
        },
        {
          id: "tempBody",
          component: "Text",
          text: "This surface will be automatically deleted in 3 seconds...",
          variant: "body"
        },
        {
          id: "tempCountdown",
          component: "Text",
          text: "Watch it disappear! 👀",
          variant: "caption"
        }
      ]
    }
  }
];
