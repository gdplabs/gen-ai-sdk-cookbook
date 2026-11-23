// ============================================================================
// SAMPLE: Layout - Grid and flex layouts
// ============================================================================
export const layoutSample = [
  {
    version: "1.0",
    createSurface: {
      surfaceId: "main",
      catalogId: "https://github.com/GDP-ADMIN/glchat-sdk/blob/main/js/glchat-a2ui-react-renderer/json/v1_0/glchat_standard_catalog_definition.json"
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
            "layoutHeader",
            "rowDemos",
            "columnDemos"
          ],
          justify: "start",
          align: "stretch"
        },
        {
          id: "layoutHeader",
          component: "Text",
          text: "## Layout Examples"
        },
        {
          id: "rowDemos",
          component: "Column",
          children: [
            "rowHeader",
            "rowStart",
            "rowCenter",
            "rowEnd",
            "rowBetween",
            "rowEvenly"
          ],
          justify: "start",
          align: "stretch"
        },
        {
          id: "rowHeader",
          component: "Text",
          text: "#### Row Distribution"
        },
        {
          id: "rowStart",
          component: "Card",
          child: "rowStartContent"
        },
        {
          id: "rowStartContent",
          component: "Column",
          children: [
            "rowStartLabel",
            "rowStartDemo"
          ],
          justify: "start",
          align: "stretch"
        },
        {
          id: "rowStartLabel",
          component: "Text",
          text: "distribution: start",
          variant: "caption"
        },
        {
          id: "rowStartDemo",
          component: "Row",
          children: [
            "box1a",
            "box1b",
            "box1c"
          ],
          justify: "start",
          align: "center"
        },
        {
          id: "rowCenter",
          component: "Card",
          child: "rowCenterContent"
        },
        {
          id: "rowCenterContent",
          component: "Column",
          children: [
            "rowCenterLabel",
            "rowCenterDemo"
          ],
          justify: "start",
          align: "stretch"
        },
        {
          id: "rowCenterLabel",
          component: "Text",
          text: "distribution: center",
          variant: "caption"
        },
        {
          id: "rowCenterDemo",
          component: "Row",
          children: [
            "box2a",
            "box2b",
            "box2c"
          ],
          justify: "center",
          align: "center"
        },
        {
          id: "rowEnd",
          component: "Card",
          child: "rowEndContent"
        },
        {
          id: "rowEndContent",
          component: "Column",
          children: [
            "rowEndLabel",
            "rowEndDemo"
          ],
          justify: "start",
          align: "stretch"
        },
        {
          id: "rowEndLabel",
          component: "Text",
          text: "distribution: end",
          variant: "caption"
        },
        {
          id: "rowEndDemo",
          component: "Row",
          children: [
            "box3a",
            "box3b",
            "box3c"
          ],
          justify: "end",
          align: "center"
        },
        {
          id: "rowBetween",
          component: "Card",
          child: "rowBetweenContent"
        },
        {
          id: "rowBetweenContent",
          component: "Column",
          children: [
            "rowBetweenLabel",
            "rowBetweenDemo"
          ],
          justify: "start",
          align: "stretch"
        },
        {
          id: "rowBetweenLabel",
          component: "Text",
          text: "distribution: spaceBetween",
          variant: "caption"
        },
        {
          id: "rowBetweenDemo",
          component: "Row",
          children: [
            "box4a",
            "box4b",
            "box4c"
          ],
          justify: "spaceBetween",
          align: "center"
        },
        {
          id: "rowEvenly",
          component: "Card",
          child: "rowEvenlyContent"
        },
        {
          id: "rowEvenlyContent",
          component: "Column",
          children: [
            "rowEvenlyLabel",
            "rowEvenlyDemo"
          ],
          justify: "start",
          align: "stretch"
        },
        {
          id: "rowEvenlyLabel",
          component: "Text",
          text: "distribution: spaceEvenly",
          variant: "caption"
        },
        {
          id: "rowEvenlyDemo",
          component: "Row",
          children: [
            "box5a",
            "box5b",
            "box5c"
          ],
          justify: "spaceEvenly",
          align: "center"
        },
        {
          id: "box1a",
          component: "Button",
          child: "box1aText",
          action: {
            event: {
              name: "demo"
            }
          },
          variant: "default"
        },
        {
          id: "box1b",
          component: "Button",
          child: "box1bText",
          action: {
            event: {
              name: "demo"
            }
          },
          variant: "default"
        },
        {
          id: "box1c",
          component: "Button",
          child: "box1cText",
          action: {
            event: {
              name: "demo"
            }
          },
          variant: "default"
        },
        {
          id: "box2a",
          component: "Button",
          child: "box2aText",
          action: {
            event: {
              name: "demo"
            }
          },
          variant: "default"
        },
        {
          id: "box2b",
          component: "Button",
          child: "box2bText",
          action: {
            event: {
              name: "demo"
            }
          },
          variant: "default"
        },
        {
          id: "box2c",
          component: "Button",
          child: "box2cText",
          action: {
            event: {
              name: "demo"
            }
          },
          variant: "default"
        },
        {
          id: "box3a",
          component: "Button",
          child: "box3aText",
          action: {
            event: {
              name: "demo"
            }
          },
          variant: "default"
        },
        {
          id: "box3b",
          component: "Button",
          child: "box3bText",
          action: {
            event: {
              name: "demo"
            }
          },
          variant: "default"
        },
        {
          id: "box3c",
          component: "Button",
          child: "box3cText",
          action: {
            event: {
              name: "demo"
            }
          },
          variant: "default"
        },
        {
          id: "box4a",
          component: "Button",
          child: "box4aText",
          action: {
            event: {
              name: "demo"
            }
          },
          variant: "default"
        },
        {
          id: "box4b",
          component: "Button",
          child: "box4bText",
          action: {
            event: {
              name: "demo"
            }
          },
          variant: "default"
        },
        {
          id: "box4c",
          component: "Button",
          child: "box4cText",
          action: {
            event: {
              name: "demo"
            }
          },
          variant: "default"
        },
        {
          id: "box5a",
          component: "Button",
          child: "box5aText",
          action: {
            event: {
              name: "demo"
            }
          },
          variant: "default"
        },
        {
          id: "box5b",
          component: "Button",
          child: "box5bText",
          action: {
            event: {
              name: "demo"
            }
          },
          variant: "default"
        },
        {
          id: "box5c",
          component: "Button",
          child: "box5cText",
          action: {
            event: {
              name: "demo"
            }
          },
          variant: "default"
        },
        {
          id: "box1aText",
          component: "Text",
          text: "[1a]",
          variant: "caption"
        },
        {
          id: "box1bText",
          component: "Text",
          text: "[1b]",
          variant: "caption"
        },
        {
          id: "box1cText",
          component: "Text",
          text: "[1c]",
          variant: "caption"
        },
        {
          id: "box2aText",
          component: "Text",
          text: "[2a]",
          variant: "caption"
        },
        {
          id: "box2bText",
          component: "Text",
          text: "[2b]",
          variant: "caption"
        },
        {
          id: "box2cText",
          component: "Text",
          text: "[2c]",
          variant: "caption"
        },
        {
          id: "box3aText",
          component: "Text",
          text: "[3a]",
          variant: "caption"
        },
        {
          id: "box3bText",
          component: "Text",
          text: "[3b]",
          variant: "caption"
        },
        {
          id: "box3cText",
          component: "Text",
          text: "[3c]",
          variant: "caption"
        },
        {
          id: "box4aText",
          component: "Text",
          text: "[4a]",
          variant: "caption"
        },
        {
          id: "box4bText",
          component: "Text",
          text: "[4b]",
          variant: "caption"
        },
        {
          id: "box4cText",
          component: "Text",
          text: "[4c]",
          variant: "caption"
        },
        {
          id: "box5aText",
          component: "Text",
          text: "[5a]",
          variant: "caption"
        },
        {
          id: "box5bText",
          component: "Text",
          text: "[5b]",
          variant: "caption"
        },
        {
          id: "box5cText",
          component: "Text",
          text: "[5c]",
          variant: "caption"
        },
        {
          id: "columnDemos",
          component: "Column",
          children: [
            "colHeader",
            "colDemosRow"
          ],
          justify: "start",
          align: "stretch"
        },
        {
          id: "colHeader",
          component: "Text",
          text: "#### Column Alignment"
        },
        {
          id: "colDemosRow",
          component: "Row",
          children: [
            "colStartCard",
            "colCenterCard",
            "colEndCard"
          ],
          justify: "spaceEvenly",
          align: "stretch"
        },
        {
          id: "colStartCard",
          component: "Card",
          child: "colStartContent"
        },
        {
          id: "colStartContent",
          component: "Column",
          children: [
            "colStartLabel",
            "colStartItem1",
            "colStartItem2"
          ],
          justify: "start",
          align: "start"
        },
        {
          id: "colStartLabel",
          component: "Text",
          text: "align: start",
          variant: "caption"
        },
        {
          id: "colStartItem1",
          component: "Text",
          text: "Item 1",
          variant: "body"
        },
        {
          id: "colStartItem2",
          component: "Text",
          text: "Item 2",
          variant: "body"
        },
        {
          id: "colCenterCard",
          component: "Card",
          child: "colCenterContent"
        },
        {
          id: "colCenterContent",
          component: "Column",
          children: [
            "colCenterLabel",
            "colCenterItem1",
            "colCenterItem2"
          ],
          justify: "start",
          align: "center"
        },
        {
          id: "colCenterLabel",
          component: "Text",
          text: "align: center",
          variant: "caption"
        },
        {
          id: "colCenterItem1",
          component: "Text",
          text: "Item 1",
          variant: "body"
        },
        {
          id: "colCenterItem2",
          component: "Text",
          text: "Item 2",
          variant: "body"
        },
        {
          id: "colEndCard",
          component: "Card",
          child: "colEndContent"
        },
        {
          id: "colEndContent",
          component: "Column",
          children: [
            "colEndLabel",
            "colEndItem1",
            "colEndItem2"
          ],
          justify: "start",
          align: "end"
        },
        {
          id: "colEndLabel",
          component: "Text",
          text: "align: end",
          variant: "caption"
        },
        {
          id: "colEndItem1",
          component: "Text",
          text: "Item 1",
          variant: "body"
        },
        {
          id: "colEndItem2",
          component: "Text",
          text: "Item 2",
          variant: "body"
        }
      ]
    }
  }
];
