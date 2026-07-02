// ============================================================================
// SAMPLE: Dashboard - Stats and metrics layout
// ============================================================================
export const dashboardSample = [
    {
      version: "v0.9",
      createSurface: {
        surfaceId: "main",
        catalogId: "https://github.com/GDP-ADMIN/glchat-sdk/blob/main/js/glchat-a2ui-react-renderer/json/glchat_standard_catalog_definition.json",
      },
    },
    {
      version: "v0.9",
      updateDataModel: {
        surfaceId: "main",
        value: {
          stats: {
            users: "12,847",
            revenue: "$84,230",
            orders: "1,429",
          },
        },
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
              "dashboard-header",
              "stats-row",
              "divider",
              "details-section",
            ],
            justify: "start",
            align: "stretch",
          },
          {
            id: "dashboard-header",
            component: "Row",
            children: [
              "header-text",
              "refresh-btn",
            ],
            justify: "spaceBetween",
            align: "center",
          },
          {
            id: "header-text",
            component: "Text",
            text: "Analytics Dashboard",
            variant: "h2",
          },
          {
            id: "refresh-btn",
            component: "Button",
            child: "refresh-text",
            action: {
              event: {
                name: "refresh_dashboard",
              },
            },
            variant: "default",
          },
          {
            id: "refresh-text",
            component: "Text",
            text: "Refresh",
            variant: "body",
          },
          {
            id: "stats-row",
            component: "Row",
            children: [
              "stat-card-1",
              "stat-card-2",
              "stat-card-3",
            ],
            justify: "spaceEvenly",
            align: "stretch",
          },
          {
            id: "stat-card-1",
            component: "Card",
            child: "stat-1-content",
          },
          {
            id: "stat-1-content",
            component: "Column",
            children: [
              "stat-1-label",
              "stat-1-value",
              "stat-1-change",
            ],
            justify: "center",
            align: "center",
          },
          {
            id: "stat-1-label",
            component: "Text",
            text: "Total Users",
            variant: "caption",
          },
          {
            id: "stat-1-value",
            component: "Text",
            text: {
              path: "/stats/users",
            },
            variant: "h1",
          },
          {
            id: "stat-1-change",
            component: "Text",
            text: "+12.5% from last month",
            variant: "caption",
          },
          {
            id: "stat-card-2",
            component: "Card",
            child: "stat-2-content",
          },
          {
            id: "stat-2-content",
            component: "Column",
            children: [
              "stat-2-label",
              "stat-2-value",
              "stat-2-change",
            ],
            justify: "center",
            align: "center",
          },
          {
            id: "stat-2-label",
            component: "Text",
            text: "Revenue",
            variant: "caption",
          },
          {
            id: "stat-2-value",
            component: "Text",
            text: {
              path: "/stats/revenue",
            },
            variant: "h1",
          },
          {
            id: "stat-2-change",
            component: "Text",
            text: "+8.2% from last month",
            variant: "caption",
          },
          {
            id: "stat-card-3",
            component: "Card",
            child: "stat-3-content",
          },
          {
            id: "stat-3-content",
            component: "Column",
            children: [
              "stat-3-label",
              "stat-3-value",
              "stat-3-change",
            ],
            justify: "center",
            align: "center",
          },
          {
            id: "stat-3-label",
            component: "Text",
            text: "Orders",
            variant: "caption",
          },
          {
            id: "stat-3-value",
            component: "Text",
            text: {
              path: "/stats/orders",
            },
            variant: "h1",
          },
          {
            id: "stat-3-change",
            component: "Text",
            text: "+23.1% from last month",
            variant: "caption",
          },
          {
            id: "divider",
            component: "Divider",
            axis: "horizontal",
          },
          {
            id: "details-section",
            component: "Column",
            children: [
              "details-header",
              "details-row",
            ],
            justify: "start",
            align: "stretch",
          },
          {
            id: "details-header",
            component: "Text",
            text: "Quick Actions",
            variant: "h4",
          },
          {
            id: "details-row",
            component: "Row",
            children: [
              "action-1",
              "action-2",
              "action-3",
            ],
            justify: "start",
            align: "center",
          },
          {
            id: "action-1",
            component: "Button",
            child: "action-1-text",
            action: {
              event: {
                name: "view_reports",
              },
            },
            variant: "primary",
          },
          {
            id: "action-1-text",
            component: "Text",
            text: "View Reports",
            variant: "body",
          },
          {
            id: "action-2",
            component: "Button",
            child: "action-2-text",
            action: {
              event: {
                name: "export_data",
              },
            },
            variant: "default",
          },
          {
            id: "action-2-text",
            component: "Text",
            text: "Export Data",
            variant: "body",
          },
          {
            id: "action-3",
            component: "Button",
            child: "action-3-text",
            action: {
              event: {
                name: "settings",
              },
            },
            variant: "default",
          },
          {
            id: "action-3-text",
            component: "Text",
            text: "Settings",
            variant: "body",
          },
        ],
      },
    },
  ];
