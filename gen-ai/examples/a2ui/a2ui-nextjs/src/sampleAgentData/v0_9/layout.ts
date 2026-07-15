// ============================================================================
// SAMPLE: Layout - Grid and flex layouts
// ============================================================================
export const layoutSample = [
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
              "layout-header",
              "row-demos",
              "column-demos",
            ],
            justify: "start",
            align: "stretch",
          },
          {
            id: "layout-header",
            component: "Text",
            text: "Layout Examples",
            variant: "h2",
          },
          {
            id: "row-demos",
            component: "Column",
            children: [
              "row-header",
              "row-start",
              "row-center",
              "row-end",
              "row-between",
              "row-evenly",
            ],
            justify: "start",
            align: "stretch",
          },
          {
            id: "row-header",
            component: "Text",
            text: "Row Distribution",
            variant: "h4",
          },
          {
            id: "row-start",
            component: "Card",
            child: "row-start-content",
          },
          {
            id: "row-start-content",
            component: "Column",
            children: [
              "row-start-label",
              "row-start-demo",
            ],
            justify: "start",
            align: "stretch",
          },
          {
            id: "row-start-label",
            component: "Text",
            text: "distribution: start",
            variant: "caption",
          },
          {
            id: "row-start-demo",
            component: "Row",
            children: [
              "box-1a",
              "box-1b",
              "box-1c",
            ],
            justify: "start",
            align: "center",
          },
          {
            id: "row-center",
            component: "Card",
            child: "row-center-content",
          },
          {
            id: "row-center-content",
            component: "Column",
            children: [
              "row-center-label",
              "row-center-demo",
            ],
            justify: "start",
            align: "stretch",
          },
          {
            id: "row-center-label",
            component: "Text",
            text: "distribution: center",
            variant: "caption",
          },
          {
            id: "row-center-demo",
            component: "Row",
            children: [
              "box-2a",
              "box-2b",
              "box-2c",
            ],
            justify: "center",
            align: "center",
          },
          {
            id: "row-end",
            component: "Card",
            child: "row-end-content",
          },
          {
            id: "row-end-content",
            component: "Column",
            children: [
              "row-end-label",
              "row-end-demo",
            ],
            justify: "start",
            align: "stretch",
          },
          {
            id: "row-end-label",
            component: "Text",
            text: "distribution: end",
            variant: "caption",
          },
          {
            id: "row-end-demo",
            component: "Row",
            children: [
              "box-3a",
              "box-3b",
              "box-3c",
            ],
            justify: "end",
            align: "center",
          },
          {
            id: "row-between",
            component: "Card",
            child: "row-between-content",
          },
          {
            id: "row-between-content",
            component: "Column",
            children: [
              "row-between-label",
              "row-between-demo",
            ],
            justify: "start",
            align: "stretch",
          },
          {
            id: "row-between-label",
            component: "Text",
            text: "distribution: spaceBetween",
            variant: "caption",
          },
          {
            id: "row-between-demo",
            component: "Row",
            children: [
              "box-4a",
              "box-4b",
              "box-4c",
            ],
            justify: "spaceBetween",
            align: "center",
          },
          {
            id: "row-evenly",
            component: "Card",
            child: "row-evenly-content",
          },
          {
            id: "row-evenly-content",
            component: "Column",
            children: [
              "row-evenly-label",
              "row-evenly-demo",
            ],
            justify: "start",
            align: "stretch",
          },
          {
            id: "row-evenly-label",
            component: "Text",
            text: "distribution: spaceEvenly",
            variant: "caption",
          },
          {
            id: "row-evenly-demo",
            component: "Row",
            children: [
              "box-5a",
              "box-5b",
              "box-5c",
            ],
            justify: "spaceEvenly",
            align: "center",
          },
          {
            id: "box-1a",
            component: "Button",
            child: "box-1a-text",
            action: {
              event: {
                name: "demo",
              },
            },
            variant: "default",
          },
          {
            id: "box-1b",
            component: "Button",
            child: "box-1b-text",
            action: {
              event: {
                name: "demo",
              },
            },
            variant: "default",
          },
          {
            id: "box-1c",
            component: "Button",
            child: "box-1c-text",
            action: {
              event: {
                name: "demo",
              },
            },
            variant: "default",
          },
          {
            id: "box-2a",
            component: "Button",
            child: "box-2a-text",
            action: {
              event: {
                name: "demo",
              },
            },
            variant: "default",
          },
          {
            id: "box-2b",
            component: "Button",
            child: "box-2b-text",
            action: {
              event: {
                name: "demo",
              },
            },
            variant: "default",
          },
          {
            id: "box-2c",
            component: "Button",
            child: "box-2c-text",
            action: {
              event: {
                name: "demo",
              },
            },
            variant: "default",
          },
          {
            id: "box-3a",
            component: "Button",
            child: "box-3a-text",
            action: {
              event: {
                name: "demo",
              },
            },
            variant: "default",
          },
          {
            id: "box-3b",
            component: "Button",
            child: "box-3b-text",
            action: {
              event: {
                name: "demo",
              },
            },
            variant: "default",
          },
          {
            id: "box-3c",
            component: "Button",
            child: "box-3c-text",
            action: {
              event: {
                name: "demo",
              },
            },
            variant: "default",
          },
          {
            id: "box-4a",
            component: "Button",
            child: "box-4a-text",
            action: {
              event: {
                name: "demo",
              },
            },
            variant: "default",
          },
          {
            id: "box-4b",
            component: "Button",
            child: "box-4b-text",
            action: {
              event: {
                name: "demo",
              },
            },
            variant: "default",
          },
          {
            id: "box-4c",
            component: "Button",
            child: "box-4c-text",
            action: {
              event: {
                name: "demo",
              },
            },
            variant: "default",
          },
          {
            id: "box-5a",
            component: "Button",
            child: "box-5a-text",
            action: {
              event: {
                name: "demo",
              },
            },
            variant: "default",
          },
          {
            id: "box-5b",
            component: "Button",
            child: "box-5b-text",
            action: {
              event: {
                name: "demo",
              },
            },
            variant: "default",
          },
          {
            id: "box-5c",
            component: "Button",
            child: "box-5c-text",
            action: {
              event: {
                name: "demo",
              },
            },
            variant: "default",
          },
          {
            id: "box-1a-text",
            component: "Text",
            text: "[1a]",
            variant: "caption",
          },
          {
            id: "box-1b-text",
            component: "Text",
            text: "[1b]",
            variant: "caption",
          },
          {
            id: "box-1c-text",
            component: "Text",
            text: "[1c]",
            variant: "caption",
          },
          {
            id: "box-2a-text",
            component: "Text",
            text: "[2a]",
            variant: "caption",
          },
          {
            id: "box-2b-text",
            component: "Text",
            text: "[2b]",
            variant: "caption",
          },
          {
            id: "box-2c-text",
            component: "Text",
            text: "[2c]",
            variant: "caption",
          },
          {
            id: "box-3a-text",
            component: "Text",
            text: "[3a]",
            variant: "caption",
          },
          {
            id: "box-3b-text",
            component: "Text",
            text: "[3b]",
            variant: "caption",
          },
          {
            id: "box-3c-text",
            component: "Text",
            text: "[3c]",
            variant: "caption",
          },
          {
            id: "box-4a-text",
            component: "Text",
            text: "[4a]",
            variant: "caption",
          },
          {
            id: "box-4b-text",
            component: "Text",
            text: "[4b]",
            variant: "caption",
          },
          {
            id: "box-4c-text",
            component: "Text",
            text: "[4c]",
            variant: "caption",
          },
          {
            id: "box-5a-text",
            component: "Text",
            text: "[5a]",
            variant: "caption",
          },
          {
            id: "box-5b-text",
            component: "Text",
            text: "[5b]",
            variant: "caption",
          },
          {
            id: "box-5c-text",
            component: "Text",
            text: "[5c]",
            variant: "caption",
          },
          {
            id: "column-demos",
            component: "Column",
            children: [
              "col-header",
              "col-demos-row",
            ],
            justify: "start",
            align: "stretch",
          },
          {
            id: "col-header",
            component: "Text",
            text: "Column Alignment",
            variant: "h4",
          },
          {
            id: "col-demos-row",
            component: "Row",
            children: [
              "col-start-card",
              "col-center-card",
              "col-end-card",
            ],
            justify: "spaceEvenly",
            align: "stretch",
          },
          {
            id: "col-start-card",
            component: "Card",
            child: "col-start-content",
          },
          {
            id: "col-start-content",
            component: "Column",
            children: [
              "col-start-label",
              "col-start-item-1",
              "col-start-item-2",
            ],
            justify: "start",
            align: "start",
          },
          {
            id: "col-start-label",
            component: "Text",
            text: "align: start",
            variant: "caption",
          },
          {
            id: "col-start-item-1",
            component: "Text",
            text: "Item 1",
            variant: "body",
          },
          {
            id: "col-start-item-2",
            component: "Text",
            text: "Item 2",
            variant: "body",
          },
          {
            id: "col-center-card",
            component: "Card",
            child: "col-center-content",
          },
          {
            id: "col-center-content",
            component: "Column",
            children: [
              "col-center-label",
              "col-center-item-1",
              "col-center-item-2",
            ],
            justify: "start",
            align: "center",
          },
          {
            id: "col-center-label",
            component: "Text",
            text: "align: center",
            variant: "caption",
          },
          {
            id: "col-center-item-1",
            component: "Text",
            text: "Item 1",
            variant: "body",
          },
          {
            id: "col-center-item-2",
            component: "Text",
            text: "Item 2",
            variant: "body",
          },
          {
            id: "col-end-card",
            component: "Card",
            child: "col-end-content",
          },
          {
            id: "col-end-content",
            component: "Column",
            children: [
              "col-end-label",
              "col-end-item-1",
              "col-end-item-2",
            ],
            justify: "start",
            align: "end",
          },
          {
            id: "col-end-label",
            component: "Text",
            text: "align: end",
            variant: "caption",
          },
          {
            id: "col-end-item-1",
            component: "Text",
            text: "Item 1",
            variant: "body",
          },
          {
            id: "col-end-item-2",
            component: "Text",
            text: "Item 2",
            variant: "body",
          },
        ],
      },
    },
  ];
