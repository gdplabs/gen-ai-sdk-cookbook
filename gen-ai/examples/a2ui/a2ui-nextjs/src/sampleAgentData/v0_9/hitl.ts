// ============================================================================
// SAMPLE: HITL - Human-in-the-loop approval workflow
// ============================================================================
export const hitlSample = [
    {
      version: "v0.9",
      createSurface: {
        surfaceId: "header",
        catalogId: "https://github.com/GDP-ADMIN/glchat-sdk/blob/main/js/glchat-a2ui-react-renderer/json/glchat_standard_catalog_definition.json",
      },
    },
    {
      version: "v0.9",
      updateDataModel: {
        surfaceId: "header",
        value: {
          header: {
            title: "Approval Required",
            icon: "⚠️",
          },
        },
      },
    },
    {
      version: "v0.9",
      updateComponents: {
        surfaceId: "header",
        components: [
          {
            id: "root",
            component: "Row",
            children: [
              "title",
              "icon",
            ],
            justify: "start",
            align: "center",
          },
          {
            id: "title",
            component: "Text",
            text: {
              path: "/header/title",
            },
            variant: "h2",
          },
          {
            id: "icon",
            component: "Text",
            text: {
              path: "/header/icon",
            },
            variant: "h2",
          },
        ],
      },
    },
    {
      version: "v0.9",
      createSurface: {
        surfaceId: "hitl",
        catalogId: "https://github.com/GDP-ADMIN/glchat-sdk/blob/main/js/glchat-a2ui-react-renderer/json/glchat_standard_catalog_definition.json",
      },
    },
    {
      version: "v0.9",
      updateDataModel: {
        surfaceId: "hitl",
        value: {
          hitl: {
            requestId: "REQ-2024-00847",
            expiresAt: "2026-03-26T10:10:00Z",
          },
        },
      },
    },
    {
      version: "v0.9",
      updateComponents: {
        surfaceId: "hitl",
        components: [
          {
            id: "root",
            component: "Column",
            children: [
              "action-card",
            ],
            justify: "start",
            align: "stretch",
          },
          {
            id: "hitl-header",
            component: "Row",
            children: [
              "header-icon",
              "header-text",
            ],
            justify: "start",
            align: "center",
          },
          {
            id: "header-icon",
            component: "Text",
            text: {
              path: "/hitl/icon",
            },
            variant: "h2",
          },
          {
            id: "header-text",
            component: "Text",
            text: {
              path: "/hitl/title",
            },
            variant: "h2",
          },
          {
            id: "action-card",
            component: "Card",
            child: "action-content",
          },
          {
            id: "action-content",
            component: "Column",
            children: [
              "action-label-row",
              "action-buttons",
            ],
            justify: "start",
            align: "stretch",
          },
          {
            id: "action-label-row",
            component: "Row",
            children: [
              "action-label",
              "hitl-timeout",
            ],
            justify: "start",
            align: "end",
          },
          {
            id: "action-label",
            component: "Text",
            text: "Please review and take action:",
            variant: "body",
          },
          {
            id: "hitl-timeout",
            component: "Timeout",
            targetTimeUtc: {
              path: "/hitl/expiresAt",
            },
          },
          {
            id: "action-buttons",
            component: "Row",
            children: [
              "approve-btn",
              "reject-btn",
              "skip-btn",
            ],
            justify: "start",
            align: "start",
          },
          {
            id: "approve-btn",
            component: "Button",
            child: "approve-text",
            action: {
              event: {
                name: "hitl_decision",
                context: {
                  decision: "approved",
                  requestId: {
                    path: "/hitl/requestId",
                  },
                },
              },
            },
            variant: "primary",
          },
          {
            id: "approve-text",
            component: "Text",
            text: "✓ Approve",
            variant: "body",
          },
          {
            id: "reject-btn",
            component: "Button",
            child: "reject-text",
            action: {
              event: {
                name: "hitl_decision",
                context: {
                  decision: "rejected",
                  requestId: {
                    path: "/hitl/requestId",
                  },
                },
              },
            },
            variant: "destructive",
          },
          {
            id: "reject-text",
            component: "Text",
            text: "✗ Reject",
            variant: "body",
          },
          {
            id: "skip-btn",
            component: "Button",
            child: "skip-text",
            action: {
              event: {
                name: "hitl_decision",
                context: {
                  decision: "skipped",
                  requestId: {
                    path: "/hitl/requestId",
                  },
                },
              },
            },
            variant: "default",
          },
          {
            id: "skip-text",
            component: "Text",
            text: "Skip",
            variant: "body",
          },
        ],
      },
    },
  ];
