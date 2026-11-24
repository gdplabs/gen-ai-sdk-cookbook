// ============================================================================
// SAMPLE: Profile - User profile card
// ============================================================================
export const profileSample = [
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
        user: {
          avatar: "https://i.pravatar.cc/200?img=8",
          name: "Sarah Chen",
          role: "Senior Product Designer",
          status: "🟢 Online",
          email: "sarah.chen@company.com",
          location: "San Francisco, CA",
          joined: "January 2023"
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
          component: "Card",
          child: "profileContent"
        },
        {
          id: "profileContent",
          component: "Column",
          children: [
            "profileHeader",
            "divider1",
            "profileDetails",
            "divider2",
            "profileActions"
          ],
          justify: "start",
          align: "stretch"
        },
        {
          id: "profileHeader",
          component: "Row",
          children: [
            "profileAvatar",
            "profileInfo"
          ],
          justify: "start",
          align: "center"
        },
        {
          id: "profileAvatar",
          component: "Image",
          url: {
            "@path": "/user/avatar"
          },
          fit: "cover",
          variant: "avatar"
        },
        {
          id: "profileInfo",
          component: "Column",
          children: [
            "profileName",
            "profileRole",
            "profileStatus"
          ],
          justify: "start",
          align: "start"
        },
        {
          id: "profileName",
          component: "Text",
          text: {
            "@call": "formatString",
            args: {
              value: "### ${/user/name}"
            }
          }
        },
        {
          id: "profileRole",
          component: "Text",
          text: {
            "@path": "/user/role"
          },
          variant: "body"
        },
        {
          id: "profileStatus",
          component: "Text",
          text: {
            "@path": "/user/status"
          },
          variant: "caption"
        },
        {
          id: "divider1",
          component: "Divider",
          axis: "horizontal"
        },
        {
          id: "profileDetails",
          component: "Column",
          children: [
            "detailEmail",
            "detailLocation",
            "detailJoined"
          ],
          justify: "start",
          align: "stretch"
        },
        {
          id: "detailEmail",
          component: "Row",
          children: [
            "emailLabel",
            "emailValue"
          ],
          justify: "spaceBetween",
          align: "center"
        },
        {
          id: "emailLabel",
          component: "Text",
          text: "Email",
          variant: "caption"
        },
        {
          id: "emailValue",
          component: "Text",
          text: {
            "@path": "/user/email"
          },
          variant: "body"
        },
        {
          id: "detailLocation",
          component: "Row",
          children: [
            "locationLabel",
            "locationValue"
          ],
          justify: "spaceBetween",
          align: "center"
        },
        {
          id: "locationLabel",
          component: "Text",
          text: "Location",
          variant: "caption"
        },
        {
          id: "locationValue",
          component: "Text",
          text: {
            "@path": "/user/location"
          },
          variant: "body"
        },
        {
          id: "detailJoined",
          component: "Row",
          children: [
            "joinedLabel",
            "joinedValue"
          ],
          justify: "spaceBetween",
          align: "center"
        },
        {
          id: "joinedLabel",
          component: "Text",
          text: "Joined",
          variant: "caption"
        },
        {
          id: "joinedValue",
          component: "Text",
          text: {
            "@path": "/user/joined"
          },
          variant: "body"
        },
        {
          id: "divider2",
          component: "Divider",
          axis: "horizontal"
        },
        {
          id: "profileActions",
          component: "Row",
          children: [
            "editBtn",
            "messageBtn",
            "moreBtn"
          ],
          justify: "spaceEvenly",
          align: "center"
        },
        {
          id: "editBtn",
          component: "Button",
          catalogId: "https://github.com/GDP-ADMIN/glchat-sdk/blob/main/js/glchat-a2ui-react-renderer/json/v1_0/glchat_extension_catalog_definition.json",
          child: "editText",
          action: {
            event: {
              name: "edit_profile"
            }
          },
          variant: "primary"
        },
        {
          id: "editText",
          component: "Text",
          text: "Edit Profile",
          variant: "body"
        },
        {
          id: "messageBtn",
          component: "Button",
          catalogId: "https://github.com/GDP-ADMIN/glchat-sdk/blob/main/js/glchat-a2ui-react-renderer/json/v1_0/glchat_extension_catalog_definition.json",
          child: "messageText",
          action: {
            event: {
              name: "send_message"
            }
          },
          variant: "default"
        },
        {
          id: "messageText",
          component: "Text",
          text: "Message",
          variant: "body"
        },
        {
          id: "moreBtn",
          component: "Button",
          catalogId: "https://github.com/GDP-ADMIN/glchat-sdk/blob/main/js/glchat-a2ui-react-renderer/json/v1_0/glchat_extension_catalog_definition.json",
          child: "moreText",
          action: {
            event: {
              name: "more_options"
            }
          },
          variant: "default"
        },
        {
          id: "moreText",
          component: "Text",
          text: "...",
          variant: "body"
        }
      ]
    }
  }
];
