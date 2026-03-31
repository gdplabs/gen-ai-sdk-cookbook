// ============================================================================
// SAMPLE: Profile - User profile card
// ============================================================================
export const profileSample = [
  {
    surfaceUpdate: {
      surfaceId: "main",
      components: [
        {
          id: "root",
          component: { Card: { child: "profile-content" } },
        },
        {
          id: "profile-content",
          component: {
            Column: {
              children: {
                explicitList: [
                  "profile-header",
                  "divider-1",
                  "profile-details",
                  "divider-2",
                  "profile-actions",
                ],
              },
              distribution: "start",
              alignment: "stretch",
            },
          },
        },
        // Header with avatar and name
        {
          id: "profile-header",
          component: {
            Row: {
              children: { explicitList: ["profile-avatar", "profile-info"] },
              distribution: "start",
              alignment: "center",
            },
          },
        },
        {
          id: "profile-avatar",
          component: {
            Image: {
              url: { path: "/user/avatar" },
              fit: "cover",
              usageHint: "avatar",
            },
          },
        },
        {
          id: "profile-info",
          component: {
            Column: {
              children: { explicitList: ["profile-name", "profile-role", "profile-status"] },
              distribution: "start",
              alignment: "start",
            },
          },
        },
        {
          id: "profile-name",
          component: {
            Text: { text: { path: "/user/name" }, usageHint: "h3" },
          },
        },
        {
          id: "profile-role",
          component: {
            Text: { text: { path: "/user/role" }, usageHint: "body" },
          },
        },
        {
          id: "profile-status",
          component: {
            Text: {
              text: { literalString: "🟢 Online", path: "/user/status" },
              usageHint: "caption",
            },
          },
        },
        {
          id: "divider-1",
          component: { Divider: { axis: "horizontal" } },
        },
        // Profile details
        {
          id: "profile-details",
          component: {
            Column: {
              children: { explicitList: ["detail-email", "detail-location", "detail-joined"] },
              distribution: "start",
              alignment: "stretch",
            },
          },
        },
        {
          id: "detail-email",
          component: {
            Row: {
              children: { explicitList: ["email-label", "email-value"] },
              distribution: "spaceBetween",
              alignment: "center",
            },
          },
        },
        {
          id: "email-label",
          component: {
            Text: { text: { literalString: "Email" }, usageHint: "caption" },
          },
        },
        {
          id: "email-value",
          component: {
            Text: { text: { path: "/user/email" }, usageHint: "body" },
          },
        },
        {
          id: "detail-location",
          component: {
            Row: {
              children: { explicitList: ["location-label", "location-value"] },
              distribution: "spaceBetween",
              alignment: "center",
            },
          },
        },
        {
          id: "location-label",
          component: {
            Text: { text: { literalString: "Location" }, usageHint: "caption" },
          },
        },
        {
          id: "location-value",
          component: {
            Text: { text: { path: "/user/location" }, usageHint: "body" },
          },
        },
        {
          id: "detail-joined",
          component: {
            Row: {
              children: { explicitList: ["joined-label", "joined-value"] },
              distribution: "spaceBetween",
              alignment: "center",
            },
          },
        },
        {
          id: "joined-label",
          component: {
            Text: { text: { literalString: "Joined" }, usageHint: "caption" },
          },
        },
        {
          id: "joined-value",
          component: {
            Text: { text: { path: "/user/joined" }, usageHint: "body" },
          },
        },
        {
          id: "divider-2",
          component: { Divider: { axis: "horizontal" } },
        },
        // Actions
        {
          id: "profile-actions",
          component: {
            Row: {
              children: { explicitList: ["edit-btn", "message-btn", "more-btn"] },
              distribution: "spaceEvenly",
              alignment: "center",
            },
          },
        },
        {
          id: "edit-btn",
          component: {
            Button: {
              child: "edit-text",
              action: { name: "edit_profile" },
              primary: true,
            },
          },
        },
        {
          id: "edit-text",
          component: {
            Text: {
              text: { literalString: "Edit Profile" },
              usageHint: "body",
            },
          },
        },
        {
          id: "message-btn",
          component: {
            Button: {
              child: "message-text",
              action: { name: "send_message" },
              primary: false,
            },
          },
        },
        {
          id: "message-text",
          component: {
            Text: { text: { literalString: "Message" }, usageHint: "body" },
          },
        },
        {
          id: "more-btn",
          component: {
            Button: {
              child: "more-text",
              action: { name: "more_options" },
              primary: false,
            },
          },
        },
        {
          id: "more-text",
          component: {
            Text: { text: { literalString: "..." }, usageHint: "body" },
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
          key: "user",
          valueMap: [
            { key: "avatar", valueString: "https://i.pravatar.cc/200?img=8" },
            { key: "name", valueString: "Sarah Chen" },
            { key: "role", valueString: "Senior Product Designer" },
            { key: "status", valueString: "🟢 Online" },
            { key: "email", valueString: "sarah.chen@company.com" },
            { key: "location", valueString: "San Francisco, CA" },
            { key: "joined", valueString: "January 2023" },
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
