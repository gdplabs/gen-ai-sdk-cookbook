// ============================================================================
// SAMPLE: Settings - Configuration panel with checkboxes
// ============================================================================
export const settingsSample = [
  {
    surfaceUpdate: {
      surfaceId: "main",
      components: [
        {
          id: "root",
          component: {
            Column: {
              children: { "explicitList": [
                "settings-header",
                "divider-top",
                "notifications-section",
                "divider-mid",
                "privacy-section",
                "divider-bottom",
                "save-row",
              ] },
              distribution: "start",
              alignment: "stretch",
            },
          },
        },
        {
          id: "settings-header",
          component: {
            Text: { text: { literalString: "⚙️ Settings" }, usageHint: "h2" },
          },
        },
        {
          id: "divider-top",
          component: { Divider: { axis: "horizontal" } },
        },
        // Notifications section
        {
          id: "notifications-section",
          component: {
            Column: {
              children: { "explicitList": [
                "notifications-header",
                "email-notif",
                "push-notif",
                "sms-notif",
              ] },
              distribution: "start",
              alignment: "stretch",
            },
          },
        },
        {
          id: "notifications-header",
          component: {
            Text: { text: { literalString: "Notifications" }, usageHint: "h4" },
          },
        },
        {
          id: "email-notif",
          component: {
            CheckBox: {
              label: { literalString: "Email notifications" },
              value: { path: "/settings/emailNotif" },
            },
          },
        },
        {
          id: "push-notif",
          component: {
            CheckBox: {
              label: { literalString: "Push notifications" },
              value: { path: "/settings/pushNotif" },
            },
          },
        },
        {
          id: "sms-notif",
          component: {
            CheckBox: {
              label: { literalString: "SMS notifications" },
              value: { path: "/settings/smsNotif" },
            },
          },
        },
        {
          id: "divider-mid",
          component: { Divider: { axis: "horizontal" } },
        },
        // Privacy section
        {
          id: "privacy-section",
          component: {
            Column: {
              children: { "explicitList": [
                "privacy-header",
                "public-profile",
                "show-email",
                "show-activity",
              ] },
              distribution: "start",
              alignment: "stretch",
            },
          },
        },
        {
          id: "privacy-header",
          component: {
            Text: { text: { literalString: "Privacy" }, usageHint: "h4" },
          },
        },
        {
          id: "public-profile",
          component: {
            CheckBox: {
              label: { literalString: "Make profile public" },
              value: { path: "/settings/publicProfile" },
            },
          },
        },
        {
          id: "show-email",
          component: {
            CheckBox: {
              label: { literalString: "Show email on profile" },
              value: { path: "/settings/showEmail" },
            },
          },
        },
        {
          id: "show-activity",
          component: {
            CheckBox: {
              label: { literalString: "Show activity status" },
              value: { path: "/settings/showActivity" },
            },
          },
        },
        {
          id: "divider-bottom",
          component: { Divider: { axis: "horizontal" } },
        },
        // Save row
        {
          id: "save-row",
          component: {
            Row: {
              children: { "explicitList": ["reset-btn", "save-btn"] },
              distribution: "end",
              alignment: "center",
            },
          },
        },
        {
          id: "reset-btn",
          component: {
            Button: {
              child: "reset-text",
              action: { name: "reset_settings" },
              primary: false,
            },
          },
        },
        {
          id: "reset-text",
          component: {
            Text: {
              text: { literalString: "Reset to Default" },
              usageHint: "body",
            },
          },
        },
        {
          id: "save-btn",
          component: {
            Button: {
              child: "save-text",
              action: {
                name: "save_settings",
                context: [
                  { key: "emailNotif", value: { path: "/settings/emailNotif" } },
                  { key: "pushNotif", value: { path: "/settings/pushNotif" } },
                  { key: "smsNotif", value: { path: "/settings/smsNotif" } },
                  { key: "publicProfile", value: { path: "/settings/publicProfile" } },
                  { key: "showEmail", value: { path: "/settings/showEmail" } },
                  { key: "showActivity", value: { path: "/settings/showActivity" } },
                ],
              },
              primary: true,
            },
          },
        },
        {
          id: "save-text",
          component: {
            Text: {
              text: { literalString: "Save Changes" },
              usageHint: "body",
            },
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
          key: "settings",
          valueMap: [
            { key: "emailNotif", valueBoolean: true },
            { key: "pushNotif", valueBoolean: true },
            { key: "smsNotif", valueBoolean: false },
            { key: "publicProfile", valueBoolean: true },
            { key: "showEmail", valueBoolean: false },
            { key: "showActivity", valueBoolean: true },
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
