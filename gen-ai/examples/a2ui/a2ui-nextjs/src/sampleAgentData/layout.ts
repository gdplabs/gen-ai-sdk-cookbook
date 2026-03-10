// ============================================================================
// SAMPLE: Layout - Demonstrating Row/Column distribution and alignment
// ============================================================================
export const layoutSample = [
  {
    surfaceUpdate: {
      surfaceId: "main",
      components: [
        {
          id: "root",
          component: {
            Column: {
              children: { "explicitList": ["layout-header", "row-demos", "column-demos"] },
              distribution: "start",
              alignment: "stretch",
            },
          },
        },
        {
          id: "layout-header",
          component: {
            Text: {
              text: { literalString: "Layout Examples" },
              usageHint: "h2",
            },
          },
        },
        // Row distribution demos
        {
          id: "row-demos",
          component: {
            Column: {
              children: { "explicitList": [
                "row-header",
                "row-start",
                "row-center",
                "row-end",
                "row-between",
                "row-evenly",
              ] },
              distribution: "start",
              alignment: "stretch",
            },
          },
        },
        {
          id: "row-header",
          component: {
            Text: {
              text: { literalString: "Row Distribution" },
              usageHint: "h4",
            },
          },
        },
        // Row start
        {
          id: "row-start",
          component: {
            Card: { child: "row-start-content" },
          },
        },
        {
          id: "row-start-content",
          component: {
            Column: {
              children: { "explicitList": ["row-start-label", "row-start-demo"] },
              distribution: "start",
              alignment: "stretch",
            },
          },
        },
        {
          id: "row-start-label",
          component: {
            Text: {
              text: { literalString: "distribution: start" },
              usageHint: "caption",
            },
          },
        },
        {
          id: "row-start-demo",
          component: {
            Row: {
              children: { "explicitList": ["box-1a", "box-1b", "box-1c"] },
              distribution: "start",
              alignment: "center",
            },
          },
        },
        // Row center
        {
          id: "row-center",
          component: {
            Card: { child: "row-center-content" },
          },
        },
        {
          id: "row-center-content",
          component: {
            Column: {
              children: { "explicitList": ["row-center-label", "row-center-demo"] },
              distribution: "start",
              alignment: "stretch",
            },
          },
        },
        {
          id: "row-center-label",
          component: {
            Text: {
              text: { literalString: "distribution: center" },
              usageHint: "caption",
            },
          },
        },
        {
          id: "row-center-demo",
          component: {
            Row: {
              children: { "explicitList": ["box-2a", "box-2b", "box-2c"] },
              distribution: "center",
              alignment: "center",
            },
          },
        },
        // Row end
        {
          id: "row-end",
          component: {
            Card: { child: "row-end-content" },
          },
        },
        {
          id: "row-end-content",
          component: {
            Column: {
              children: { "explicitList": ["row-end-label", "row-end-demo"] },
              distribution: "start",
              alignment: "stretch",
            },
          },
        },
        {
          id: "row-end-label",
          component: {
            Text: {
              text: { literalString: "distribution: end" },
              usageHint: "caption",
            },
          },
        },
        {
          id: "row-end-demo",
          component: {
            Row: {
              children: { "explicitList": ["box-3a", "box-3b", "box-3c"] },
              distribution: "end",
              alignment: "center",
            },
          },
        },
        // Row spaceBetween
        {
          id: "row-between",
          component: {
            Card: { child: "row-between-content" },
          },
        },
        {
          id: "row-between-content",
          component: {
            Column: {
              children: { "explicitList": ["row-between-label", "row-between-demo"] },
              distribution: "start",
              alignment: "stretch",
            },
          },
        },
        {
          id: "row-between-label",
          component: {
            Text: {
              text: { literalString: "distribution: spaceBetween" },
              usageHint: "caption",
            },
          },
        },
        {
          id: "row-between-demo",
          component: {
            Row: {
              children: { "explicitList": ["box-4a", "box-4b", "box-4c"] },
              distribution: "spaceBetween",
              alignment: "center",
            },
          },
        },
        // Row spaceEvenly
        {
          id: "row-evenly",
          component: {
            Card: { child: "row-evenly-content" },
          },
        },
        {
          id: "row-evenly-content",
          component: {
            Column: {
              children: { "explicitList": ["row-evenly-label", "row-evenly-demo"] },
              distribution: "start",
              alignment: "stretch",
            },
          },
        },
        {
          id: "row-evenly-label",
          component: {
            Text: {
              text: { literalString: "distribution: spaceEvenly" },
              usageHint: "caption",
            },
          },
        },
        {
          id: "row-evenly-demo",
          component: {
            Row: {
              children: { "explicitList": ["box-5a", "box-5b", "box-5c"] },
              distribution: "spaceEvenly",
              alignment: "center",
            },
          },
        },
        // Box components for demos
        ...[
          "1a",
          "1b",
          "1c",
          "2a",
          "2b",
          "2c",
          "3a",
          "3b",
          "3c",
          "4a",
          "4b",
          "4c",
          "5a",
          "5b",
          "5c",
        ].map((id) => ({
          id: `box-${id}`,
          component: {
            Button: {
              child: `box-${id}-text`,
              primary: false,
            },
          },
        })),
        ...[
          "1a",
          "1b",
          "1c",
          "2a",
          "2b",
          "2c",
          "3a",
          "3b",
          "3c",
          "4a",
          "4b",
          "4c",
          "5a",
          "5b",
          "5c",
        ].map((id) => ({
          id: `box-${id}-text`,
          component: {
            Text: { text: { literalString: `[${id}]` }, usageHint: "caption" },
          },
        })),
        // Column demos
        {
          id: "column-demos",
          component: {
            Column: {
              children: { "explicitList": ["col-header", "col-demos-row"] },
              distribution: "start",
              alignment: "stretch",
            },
          },
        },
        {
          id: "col-header",
          component: {
            Text: {
              text: { literalString: "Column Alignment" },
              usageHint: "h4",
            },
          },
        },
        {
          id: "col-demos-row",
          component: {
            Row: {
              children: { "explicitList": ["col-start-card", "col-center-card", "col-end-card"] },
              distribution: "spaceEvenly",
              alignment: "stretch",
            },
          },
        },
        {
          id: "col-start-card",
          component: { Card: { child: "col-start-content" } },
        },
        {
          id: "col-start-content",
          component: {
            Column: {
              children: { "explicitList": [
                "col-start-label",
                "col-start-item-1",
                "col-start-item-2",
              ] },
              distribution: "start",
              alignment: "start",
            },
          },
        },
        {
          id: "col-start-label",
          component: {
            Text: {
              text: { literalString: "align: start" },
              usageHint: "caption",
            },
          },
        },
        {
          id: "col-start-item-1",
          component: {
            Text: { text: { literalString: "Item 1" }, usageHint: "body" },
          },
        },
        {
          id: "col-start-item-2",
          component: {
            Text: { text: { literalString: "Item 2" }, usageHint: "body" },
          },
        },
        {
          id: "col-center-card",
          component: { Card: { child: "col-center-content" } },
        },
        {
          id: "col-center-content",
          component: {
            Column: {
              children: { "explicitList": [
                "col-center-label",
                "col-center-item-1",
                "col-center-item-2",
              ] },
              distribution: "start",
              alignment: "center",
            },
          },
        },
        {
          id: "col-center-label",
          component: {
            Text: {
              text: { literalString: "align: center" },
              usageHint: "caption",
            },
          },
        },
        {
          id: "col-center-item-1",
          component: {
            Text: { text: { literalString: "Item 1" }, usageHint: "body" },
          },
        },
        {
          id: "col-center-item-2",
          component: {
            Text: { text: { literalString: "Item 2" }, usageHint: "body" },
          },
        },
        {
          id: "col-end-card",
          component: { Card: { child: "col-end-content" } },
        },
        {
          id: "col-end-content",
          component: {
            Column: {
              children: { "explicitList": ["col-end-label", "col-end-item-1", "col-end-item-2"] },
              distribution: "start",
              alignment: "end",
            },
          },
        },
        {
          id: "col-end-label",
          component: {
            Text: {
              text: { literalString: "align: end" },
              usageHint: "caption",
            },
          },
        },
        {
          id: "col-end-item-1",
          component: {
            Text: { text: { literalString: "Item 1" }, usageHint: "body" },
          },
        },
        {
          id: "col-end-item-2",
          component: {
            Text: { text: { literalString: "Item 2" }, usageHint: "body" },
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
