// ============================================================================
// SAMPLE: Dashboard - Stats and metrics layout
// ============================================================================
export const dashboardSample = [
  {
    surfaceUpdate: {
      surfaceId: "main",
      components: [
        {
          id: "root",
          component: {
            Column: {
              children: {
                explicitList: ["dashboard-header", "stats-row", "divider", "details-section"],
              },
              distribution: "start",
              alignment: "stretch",
            },
          },
        },
        {
          id: "dashboard-header",
          component: {
            Row: {
              children: { explicitList: ["header-text", "refresh-btn"] },
              distribution: "spaceBetween",
              alignment: "center",
            },
          },
        },
        {
          id: "header-text",
          component: {
            Text: {
              text: { literalString: "Analytics Dashboard" },
              usageHint: "h2",
            },
          },
        },
        {
          id: "refresh-btn",
          component: {
            Button: {
              child: "refresh-text",
              action: { name: "refresh_dashboard", context: {} },
              primary: false,
            },
          },
        },
        {
          id: "refresh-text",
          component: {
            Text: { text: { literalString: "Refresh" }, usageHint: "body" },
          },
        },
        // Stats cards row
        {
          id: "stats-row",
          component: {
            Row: {
              children: { explicitList: ["stat-card-1", "stat-card-2", "stat-card-3"] },
              distribution: "spaceEvenly",
              alignment: "stretch",
            },
          },
        },
        // Stat Card 1 - Users
        {
          id: "stat-card-1",
          component: { Card: { child: "stat-1-content" } },
        },
        {
          id: "stat-1-content",
          component: {
            Column: {
              children: { explicitList: ["stat-1-label", "stat-1-value", "stat-1-change"] },
              distribution: "center",
              alignment: "center",
            },
          },
        },
        {
          id: "stat-1-label",
          component: {
            Text: {
              text: { literalString: "Total Users" },
              usageHint: "caption",
            },
          },
        },
        {
          id: "stat-1-value",
          component: {
            Text: { text: { path: "/stats/users" }, usageHint: "h1" },
          },
        },
        {
          id: "stat-1-change",
          component: {
            Text: {
              text: { literalString: "+12.5% from last month" },
              usageHint: "caption",
            },
          },
        },
        // Stat Card 2 - Revenue
        {
          id: "stat-card-2",
          component: { Card: { child: "stat-2-content" } },
        },
        {
          id: "stat-2-content",
          component: {
            Column: {
              children: { explicitList: ["stat-2-label", "stat-2-value", "stat-2-change"] },
              distribution: "center",
              alignment: "center",
            },
          },
        },
        {
          id: "stat-2-label",
          component: {
            Text: { text: { literalString: "Revenue" }, usageHint: "caption" },
          },
        },
        {
          id: "stat-2-value",
          component: {
            Text: { text: { path: "/stats/revenue" }, usageHint: "h1" },
          },
        },
        {
          id: "stat-2-change",
          component: {
            Text: {
              text: { literalString: "+8.2% from last month" },
              usageHint: "caption",
            },
          },
        },
        // Stat Card 3 - Orders
        {
          id: "stat-card-3",
          component: { Card: { child: "stat-3-content" } },
        },
        {
          id: "stat-3-content",
          component: {
            Column: {
              children: { explicitList: ["stat-3-label", "stat-3-value", "stat-3-change"] },
              distribution: "center",
              alignment: "center",
            },
          },
        },
        {
          id: "stat-3-label",
          component: {
            Text: { text: { literalString: "Orders" }, usageHint: "caption" },
          },
        },
        {
          id: "stat-3-value",
          component: {
            Text: { text: { path: "/stats/orders" }, usageHint: "h1" },
          },
        },
        {
          id: "stat-3-change",
          component: {
            Text: {
              text: { literalString: "+23.1% from last month" },
              usageHint: "caption",
            },
          },
        },
        {
          id: "divider",
          component: { Divider: { axis: "horizontal" } },
        },
        // Details section
        {
          id: "details-section",
          component: {
            Column: {
              children: { explicitList: ["details-header", "details-row"] },
              distribution: "start",
              alignment: "stretch",
            },
          },
        },
        {
          id: "details-header",
          component: {
            Text: { text: { literalString: "Quick Actions" }, usageHint: "h4" },
          },
        },
        {
          id: "details-row",
          component: {
            Row: {
              children: { explicitList: ["action-1", "action-2", "action-3"] },
              distribution: "start",
              alignment: "center",
            },
          },
        },
        {
          id: "action-1",
          component: {
            Button: {
              child: "action-1-text",
              action: { name: "view_reports", context: {} },
              primary: true,
            },
          },
        },
        {
          id: "action-1-text",
          component: {
            Text: {
              text: { literalString: "View Reports" },
              usageHint: "body",
            },
          },
        },
        {
          id: "action-2",
          component: {
            Button: {
              child: "action-2-text",
              action: { name: "export_data", context: {} },
              primary: false,
            },
          },
        },
        {
          id: "action-2-text",
          component: {
            Text: { text: { literalString: "Export Data" }, usageHint: "body" },
          },
        },
        {
          id: "action-3",
          component: {
            Button: {
              child: "action-3-text",
              action: { name: "settings", context: {} },
              primary: false,
            },
          },
        },
        {
          id: "action-3-text",
          component: {
            Text: { text: { literalString: "Settings" }, usageHint: "body" },
          },
        },
      ],
    },
  },
  {
    dataModelUpdate: {
      surfaceId: "main",
      contents: [
        {
          key: "stats",
          valueMap: [
            { key: "users", valueString: "12,847" },
            { key: "revenue", valueString: "$84,230" },
            { key: "orders", valueString: "1,429" },
          ],
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
