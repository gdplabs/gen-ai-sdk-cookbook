// ============================================================================
// SAMPLE: Dashboard - Stats and metrics layout
// ============================================================================
export const dashboardSample = [
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
        stats: {
          users: "12,847",
          revenue: "$84,230",
          orders: "1,429"
        }
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
          component: "Column",
          children: [
            "dashboardHeader",
            "statsRow",
            "divider",
            "detailsSection"
          ],
          justify: "start",
          align: "stretch"
        },
        {
          id: "dashboardHeader",
          component: "Row",
          children: [
            "headerText",
            "refreshBtn"
          ],
          justify: "spaceBetween",
          align: "center"
        },
        {
          id: "headerText",
          component: "Text",
          text: "## Analytics Dashboard"
        },
        {
          id: "refreshBtn",
          component: "Button",
          child: "refreshText",
          action: {
            event: {
              name: "refresh_dashboard"
            }
          },
          variant: "default"
        },
        {
          id: "refreshText",
          component: "Text",
          text: "Refresh",
          variant: "body"
        },
        {
          id: "statsRow",
          component: "Row",
          children: [
            "statCard1",
            "statCard2",
            "statCard3"
          ],
          justify: "spaceEvenly",
          align: "stretch"
        },
        {
          id: "statCard1",
          component: "Card",
          child: "stat1Content"
        },
        {
          id: "stat1Content",
          component: "Column",
          children: [
            "stat1Label",
            "stat1Value",
            "stat1Change"
          ],
          justify: "center",
          align: "center"
        },
        {
          id: "stat1Label",
          component: "Text",
          text: "Total Users",
          variant: "caption"
        },
        {
          id: "stat1Value",
          component: "Text",
          text: {
            "@call": "formatString",
            args: {
              value: "# ${/stats/users}"
            }
          }
        },
        {
          id: "stat1Change",
          component: "Text",
          text: "+12.5% from last month",
          variant: "caption"
        },
        {
          id: "statCard2",
          component: "Card",
          child: "stat2Content"
        },
        {
          id: "stat2Content",
          component: "Column",
          children: [
            "stat2Label",
            "stat2Value",
            "stat2Change"
          ],
          justify: "center",
          align: "center"
        },
        {
          id: "stat2Label",
          component: "Text",
          text: "Revenue",
          variant: "caption"
        },
        {
          id: "stat2Value",
          component: "Text",
          text: {
            "@call": "formatString",
            args: {
              value: "# ${/stats/revenue}"
            }
          }
        },
        {
          id: "stat2Change",
          component: "Text",
          text: "+8.2% from last month",
          variant: "caption"
        },
        {
          id: "statCard3",
          component: "Card",
          child: "stat3Content"
        },
        {
          id: "stat3Content",
          component: "Column",
          children: [
            "stat3Label",
            "stat3Value",
            "stat3Change"
          ],
          justify: "center",
          align: "center"
        },
        {
          id: "stat3Label",
          component: "Text",
          text: "Orders",
          variant: "caption"
        },
        {
          id: "stat3Value",
          component: "Text",
          text: {
            "@call": "formatString",
            args: {
              value: "# ${/stats/orders}"
            }
          }
        },
        {
          id: "stat3Change",
          component: "Text",
          text: "+23.1% from last month",
          variant: "caption"
        },
        {
          id: "divider",
          component: "Divider",
          axis: "horizontal"
        },
        {
          id: "detailsSection",
          component: "Column",
          children: [
            "detailsHeader",
            "detailsRow"
          ],
          justify: "start",
          align: "stretch"
        },
        {
          id: "detailsHeader",
          component: "Text",
          text: "#### Quick Actions"
        },
        {
          id: "detailsRow",
          component: "Row",
          children: [
            "action1",
            "action2",
            "action3"
          ],
          justify: "start",
          align: "center"
        },
        {
          id: "action1",
          component: "Button",
          child: "action1Text",
          action: {
            event: {
              name: "view_reports"
            }
          },
          variant: "primary"
        },
        {
          id: "action1Text",
          component: "Text",
          text: "View Reports",
          variant: "body"
        },
        {
          id: "action2",
          component: "Button",
          child: "action2Text",
          action: {
            event: {
              name: "export_data"
            }
          },
          variant: "default"
        },
        {
          id: "action2Text",
          component: "Text",
          text: "Export Data",
          variant: "body"
        },
        {
          id: "action3",
          component: "Button",
          child: "action3Text",
          action: {
            event: {
              name: "settings"
            }
          },
          variant: "default"
        },
        {
          id: "action3Text",
          component: "Text",
          text: "Settings",
          variant: "body"
        }
      ]
    }
  }
];
