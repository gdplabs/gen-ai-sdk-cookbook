// ============================================================================
// SAMPLE: Settings - Configuration panel
// ============================================================================
export const settingsSample = [
  {
    version: "1.0",
    createSurface: {
      surfaceId: "main",
      catalogId: "https://a2ui.org/specification/v1_0/catalogs/basic/catalog.json"
    }
  },
  {
    version: "1.0",
    updateDataModel: {
      surfaceId: "main",
      value: {
        settings: {
          emailNotif: true,
          pushNotif: true,
          smsNotif: false,
          publicProfile: true,
          showEmail: false,
          showActivity: true
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
            "settingsHeader",
            "dividerTop",
            "notificationsSection",
            "dividerMid",
            "privacySection",
            "dividerBottom",
            "saveRow"
          ],
          justify: "start",
          align: "stretch"
        },
        {
          id: "settingsHeader",
          component: "Text",
          text: "## ⚙️ Settings"
        },
        {
          id: "dividerTop",
          component: "Divider",
          axis: "horizontal"
        },
        {
          id: "notificationsSection",
          component: "Column",
          children: [
            "notificationsHeader",
            "emailNotif",
            "pushNotif",
            "smsNotif"
          ],
          justify: "start",
          align: "stretch"
        },
        {
          id: "notificationsHeader",
          component: "Text",
          text: "#### Notifications"
        },
        {
          id: "emailNotif",
          component: "CheckBox",
          label: "Email notifications",
          value: {
            "@path": "/settings/emailNotif"
          }
        },
        {
          id: "pushNotif",
          component: "CheckBox",
          label: "Push notifications",
          value: {
            "@path": "/settings/pushNotif"
          }
        },
        {
          id: "smsNotif",
          component: "CheckBox",
          label: "SMS notifications",
          value: {
            "@path": "/settings/smsNotif"
          }
        },
        {
          id: "dividerMid",
          component: "Divider",
          axis: "horizontal"
        },
        {
          id: "privacySection",
          component: "Column",
          children: [
            "privacyHeader",
            "publicProfile",
            "showEmail",
            "showActivity"
          ],
          justify: "start",
          align: "stretch"
        },
        {
          id: "privacyHeader",
          component: "Text",
          text: "#### Privacy"
        },
        {
          id: "publicProfile",
          component: "CheckBox",
          label: "Make profile public",
          value: {
            "@path": "/settings/publicProfile"
          }
        },
        {
          id: "showEmail",
          component: "CheckBox",
          label: "Show email on profile",
          value: {
            "@path": "/settings/showEmail"
          }
        },
        {
          id: "showActivity",
          component: "CheckBox",
          label: "Show activity status",
          value: {
            "@path": "/settings/showActivity"
          }
        },
        {
          id: "dividerBottom",
          component: "Divider",
          axis: "horizontal"
        },
        {
          id: "saveRow",
          component: "Row",
          children: [
            "resetBtn",
            "saveBtn"
          ],
          justify: "end",
          align: "center"
        },
        {
          id: "resetBtn",
          component: "Button",
          catalogId: "https://github.com/GDP-ADMIN/glchat-sdk/blob/main/js/glchat-a2ui-react-renderer/json/v1_0/glchat_extension_catalog_definition.json",
          child: "resetText",
          action: {
            event: {
              name: "reset_settings"
            }
          },
          variant: "default"
        },
        {
          id: "resetText",
          component: "Text",
          text: "Reset to Default",
          variant: "body"
        },
        {
          id: "saveBtn",
          component: "Button",
          catalogId: "https://github.com/GDP-ADMIN/glchat-sdk/blob/main/js/glchat-a2ui-react-renderer/json/v1_0/glchat_extension_catalog_definition.json",
          child: "saveText",
          action: {
            event: {
              name: "save_settings",
              context: {
                emailNotif: {
                  "@path": "/settings/emailNotif"
                },
                pushNotif: {
                  "@path": "/settings/pushNotif"
                },
                smsNotif: {
                  "@path": "/settings/smsNotif"
                },
                publicProfile: {
                  "@path": "/settings/publicProfile"
                },
                showEmail: {
                  "@path": "/settings/showEmail"
                },
                showActivity: {
                  "@path": "/settings/showActivity"
                }
              }
            }
          },
          variant: "primary"
        },
        {
          id: "saveText",
          component: "Text",
          text: "Save Changes",
          variant: "body"
        }
      ]
    }
  }
];
