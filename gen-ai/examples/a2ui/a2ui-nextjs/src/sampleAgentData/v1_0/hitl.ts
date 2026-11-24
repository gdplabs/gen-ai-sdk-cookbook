// ============================================================================
// SAMPLE: HITL - Human-in-the-loop approval workflow
// ============================================================================
export const hitlSample = [
  {
    version: "1.0",
    createSurface: {
      surfaceId: "header",
      catalogId: "https://a2ui.org/specification/v1_0/catalogs/basic/catalog.json"
    }
  },
  {
    version: "1.0",
    updateDataModel: {
      surfaceId: "header",
      value: {
        header: {
          title: "Approval Required",
          icon: "⚠️"
        }
      }
    }
  },
  {
    version: "1.0",
    updateComponents: {
      surfaceId: "header",
      components: [
        {
          id: "root",
          component: "Row",
          children: [
            "title",
            "icon"
          ],
          justify: "start",
          align: "center"
        },
        {
          id: "title",
          component: "Text",
          text: {
            "@call": "formatString",
            args: {
              value: "## ${/header/title}"
            }
          }
        },
        {
          id: "icon",
          component: "Text",
          text: {
            "@call": "formatString",
            args: {
              value: "## ${/header/icon}"
            }
          }
        }
      ]
    }
  },
  {
    version: "1.0",
    createSurface: {
      surfaceId: "hitl",
      catalogId: "https://a2ui.org/specification/v1_0/catalogs/basic/catalog.json"
    }
  },
  {
    version: "1.0",
    updateDataModel: {
      surfaceId: "hitl",
      value: {
        hitl: {
          requestId: "REQ-2024-00847",
          expiresAt: "2026-03-26T10:10:00Z"
        }
      }
    }
  },
  {
    version: "1.0",
    updateComponents: {
      surfaceId: "hitl",
      components: [
        {
          id: "root",
          component: "Column",
          children: [
            "actionCard"
          ],
          justify: "start",
          align: "stretch"
        },
        {
          id: "hitlHeader",
          component: "Row",
          children: [
            "headerIcon",
            "headerText"
          ],
          justify: "start",
          align: "center"
        },
        {
          id: "headerIcon",
          component: "Text",
          text: {
            "@call": "formatString",
            args: {
              value: "## ${/hitl/icon}"
            }
          }
        },
        {
          id: "headerText",
          component: "Text",
          text: {
            "@call": "formatString",
            args: {
              value: "## ${/hitl/title}"
            }
          }
        },
        {
          id: "actionCard",
          component: "Card",
          child: "actionContent"
        },
        {
          id: "actionContent",
          component: "Column",
          children: [
            "actionLabelRow",
            "actionButtons"
          ],
          justify: "start",
          align: "stretch"
        },
        {
          id: "actionLabelRow",
          component: "Row",
          children: [
            "actionLabel",
            "hitlTimeout"
          ],
          justify: "start",
          align: "end"
        },
        {
          id: "actionLabel",
          component: "Text",
          text: "Please review and take action:",
          variant: "body"
        },
        {
          id: "hitlTimeout",
          component: "Timeout",
          catalogId: "https://github.com/GDP-ADMIN/glchat-sdk/blob/main/js/glchat-a2ui-react-renderer/json/v1_0/glchat_extension_catalog_definition.json",
          targetTimeUtc: {
            "@path": "/hitl/expiresAt"
          }
        },
        {
          id: "actionButtons",
          component: "Row",
          children: [
            "approveBtn",
            "rejectBtn",
            "skipBtn"
          ],
          justify: "start",
          align: "start"
        },
        {
          id: "approveBtn",
          component: "Button",
          catalogId: "https://github.com/GDP-ADMIN/glchat-sdk/blob/main/js/glchat-a2ui-react-renderer/json/v1_0/glchat_extension_catalog_definition.json",
          child: "approveText",
          action: {
            event: {
              name: "hitl_decision",
              context: {
                decision: "approved",
                requestId: {
                  "@path": "/hitl/requestId"
                }
              }
            }
          },
          variant: "primary"
        },
        {
          id: "approveText",
          component: "Text",
          text: "✓ Approve",
          variant: "body"
        },
        {
          id: "rejectBtn",
          component: "Button",
          catalogId: "https://github.com/GDP-ADMIN/glchat-sdk/blob/main/js/glchat-a2ui-react-renderer/json/v1_0/glchat_extension_catalog_definition.json",
          child: "rejectText",
          action: {
            event: {
              name: "hitl_decision",
              context: {
                decision: "rejected",
                requestId: {
                  "@path": "/hitl/requestId"
                }
              }
            }
          },
          variant: "destructive"
        },
        {
          id: "rejectText",
          component: "Text",
          text: "✗ Reject",
          variant: "body"
        },
        {
          id: "skipBtn",
          component: "Button",
          catalogId: "https://github.com/GDP-ADMIN/glchat-sdk/blob/main/js/glchat-a2ui-react-renderer/json/v1_0/glchat_extension_catalog_definition.json",
          child: "skipText",
          action: {
            event: {
              name: "hitl_decision",
              context: {
                decision: "skipped",
                requestId: {
                  "@path": "/hitl/requestId"
                }
              }
            }
          },
          variant: "default"
        },
        {
          id: "skipText",
          component: "Text",
          text: "Skip",
          variant: "body"
        }
      ]
    }
  }
];
