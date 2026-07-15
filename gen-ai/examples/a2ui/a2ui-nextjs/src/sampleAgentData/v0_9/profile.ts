// ============================================================================
// SAMPLE: Profile - User profile card
// ============================================================================
export const profileSample = [
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
          user: {
            avatar: "https://i.pravatar.cc/200?img=8",
            name: "Sarah Chen",
            role: "Senior Product Designer",
            status: "🟢 Online",
            email: "sarah.chen@company.com",
            location: "San Francisco, CA",
            joined: "January 2023",
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
            component: "Card",
            child: "profile-content",
          },
          {
            id: "profile-content",
            component: "Column",
            children: [
              "profile-header",
              "divider-1",
              "profile-details",
              "divider-2",
              "profile-actions",
            ],
            justify: "start",
            align: "stretch",
          },
          {
            id: "profile-header",
            component: "Row",
            children: [
              "profile-avatar",
              "profile-info",
            ],
            justify: "start",
            align: "center",
          },
          {
            id: "profile-avatar",
            component: "Image",
            url: {
              path: "/user/avatar",
            },
            fit: "cover",
            variant: "avatar",
          },
          {
            id: "profile-info",
            component: "Column",
            children: [
              "profile-name",
              "profile-role",
              "profile-status",
            ],
            justify: "start",
            align: "start",
          },
          {
            id: "profile-name",
            component: "Text",
            text: {
              path: "/user/name",
            },
            variant: "h3",
          },
          {
            id: "profile-role",
            component: "Text",
            text: {
              path: "/user/role",
            },
            variant: "body",
          },
          {
            id: "profile-status",
            component: "Text",
            text: {
              path: "/user/status",
            },
            variant: "caption",
          },
          {
            id: "divider-1",
            component: "Divider",
            axis: "horizontal",
          },
          {
            id: "profile-details",
            component: "Column",
            children: [
              "detail-email",
              "detail-location",
              "detail-joined",
            ],
            justify: "start",
            align: "stretch",
          },
          {
            id: "detail-email",
            component: "Row",
            children: [
              "email-label",
              "email-value",
            ],
            justify: "spaceBetween",
            align: "center",
          },
          {
            id: "email-label",
            component: "Text",
            text: "Email",
            variant: "caption",
          },
          {
            id: "email-value",
            component: "Text",
            text: {
              path: "/user/email",
            },
            variant: "body",
          },
          {
            id: "detail-location",
            component: "Row",
            children: [
              "location-label",
              "location-value",
            ],
            justify: "spaceBetween",
            align: "center",
          },
          {
            id: "location-label",
            component: "Text",
            text: "Location",
            variant: "caption",
          },
          {
            id: "location-value",
            component: "Text",
            text: {
              path: "/user/location",
            },
            variant: "body",
          },
          {
            id: "detail-joined",
            component: "Row",
            children: [
              "joined-label",
              "joined-value",
            ],
            justify: "spaceBetween",
            align: "center",
          },
          {
            id: "joined-label",
            component: "Text",
            text: "Joined",
            variant: "caption",
          },
          {
            id: "joined-value",
            component: "Text",
            text: {
              path: "/user/joined",
            },
            variant: "body",
          },
          {
            id: "divider-2",
            component: "Divider",
            axis: "horizontal",
          },
          {
            id: "profile-actions",
            component: "Row",
            children: [
              "edit-btn",
              "message-btn",
              "more-btn",
            ],
            justify: "spaceEvenly",
            align: "center",
          },
          {
            id: "edit-btn",
            component: "Button",
            child: "edit-text",
            action: {
              event: {
                name: "edit_profile",
              },
            },
            variant: "primary",
          },
          {
            id: "edit-text",
            component: "Text",
            text: "Edit Profile",
            variant: "body",
          },
          {
            id: "message-btn",
            component: "Button",
            child: "message-text",
            action: {
              event: {
                name: "send_message",
              },
            },
            variant: "default",
          },
          {
            id: "message-text",
            component: "Text",
            text: "Message",
            variant: "body",
          },
          {
            id: "more-btn",
            component: "Button",
            child: "more-text",
            action: {
              event: {
                name: "more_options",
              },
            },
            variant: "default",
          },
          {
            id: "more-text",
            component: "Text",
            text: "...",
            variant: "body",
          },
        ],
      },
    },
  ];
