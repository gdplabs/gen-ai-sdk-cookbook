// ============================================================================
// SAMPLE: Settings - Configuration panel
// ============================================================================
export const settingsSample = [
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
          settings: {
            emailNotif: true,
            pushNotif: true,
            smsNotif: false,
            publicProfile: true,
            showEmail: false,
            showActivity: true,
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
              "settings-header",
              "divider-top",
              "notifications-section",
              "divider-mid",
              "privacy-section",
              "divider-bottom",
              "save-row",
            ],
            justify: "start",
            align: "stretch",
          },
          {
            id: "settings-header",
            component: "Text",
            text: "⚙️ Settings",
            variant: "h2",
          },
          {
            id: "divider-top",
            component: "Divider",
            axis: "horizontal",
          },
          {
            id: "notifications-section",
            component: "Column",
            children: [
              "notifications-header",
              "email-notif",
              "push-notif",
              "sms-notif",
            ],
            justify: "start",
            align: "stretch",
          },
          {
            id: "notifications-header",
            component: "Text",
            text: "Notifications",
            variant: "h4",
          },
          {
            id: "email-notif",
            component: "CheckBox",
            label: "Email notifications",
            value: {
              path: "/settings/emailNotif",
            },
          },
          {
            id: "push-notif",
            component: "CheckBox",
            label: "Push notifications",
            value: {
              path: "/settings/pushNotif",
            },
          },
          {
            id: "sms-notif",
            component: "CheckBox",
            label: "SMS notifications",
            value: {
              path: "/settings/smsNotif",
            },
          },
          {
            id: "divider-mid",
            component: "Divider",
            axis: "horizontal",
          },
          {
            id: "privacy-section",
            component: "Column",
            children: [
              "privacy-header",
              "public-profile",
              "show-email",
              "show-activity",
            ],
            justify: "start",
            align: "stretch",
          },
          {
            id: "privacy-header",
            component: "Text",
            text: "Privacy",
            variant: "h4",
          },
          {
            id: "public-profile",
            component: "CheckBox",
            label: "Make profile public",
            value: {
              path: "/settings/publicProfile",
            },
          },
          {
            id: "show-email",
            component: "CheckBox",
            label: "Show email on profile",
            value: {
              path: "/settings/showEmail",
            },
          },
          {
            id: "show-activity",
            component: "CheckBox",
            label: "Show activity status",
            value: {
              path: "/settings/showActivity",
            },
          },
          {
            id: "divider-bottom",
            component: "Divider",
            axis: "horizontal",
          },
          {
            id: "save-row",
            component: "Row",
            children: [
              "reset-btn",
              "save-btn",
            ],
            justify: "end",
            align: "center",
          },
          {
            id: "reset-btn",
            component: "Button",
            child: "reset-text",
            action: {
              event: {
                name: "reset_settings",
              },
            },
            variant: "default",
          },
          {
            id: "reset-text",
            component: "Text",
            text: "Reset to Default",
            variant: "body",
          },
          {
            id: "save-btn",
            component: "Button",
            child: "save-text",
            action: {
              event: {
                name: "save_settings",
                context: {
                  emailNotif: {
                    path: "/settings/emailNotif",
                  },
                  pushNotif: {
                    path: "/settings/pushNotif",
                  },
                  smsNotif: {
                    path: "/settings/smsNotif",
                  },
                  publicProfile: {
                    path: "/settings/publicProfile",
                  },
                  showEmail: {
                    path: "/settings/showEmail",
                  },
                  showActivity: {
                    path: "/settings/showActivity",
                  },
                },
              },
            },
            variant: "primary",
          },
          {
            id: "save-text",
            component: "Text",
            text: "Save Changes",
            variant: "body",
          },
        ],
      },
    },
  ];
