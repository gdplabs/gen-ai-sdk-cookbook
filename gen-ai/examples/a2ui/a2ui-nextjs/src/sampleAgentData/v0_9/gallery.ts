// ============================================================================
// SAMPLE: Gallery - Image showcase with all fit types
// ============================================================================
export const gallerySample = [
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
          gallery: {
            heroUrl: "https://picsum.photos/seed/hero/800/400",
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
              "gallery-header",
              "hero-section",
              "divider-1",
              "thumbnails-section",
              "divider-2",
              "avatars-section",
            ],
            justify: "start",
            align: "stretch",
          },
          {
            id: "gallery-header",
            component: "Text",
            text: "Image Gallery",
            variant: "h2",
          },
          {
            id: "hero-section",
            component: "Column",
            children: [
              "hero-label",
              "hero-image",
            ],
            justify: "start",
            align: "stretch",
          },
          {
            id: "hero-label",
            component: "Text",
            text: "Hero Image (cover fit)",
            variant: "caption",
          },
          {
            id: "hero-image",
            component: "Image",
            url: {
              path: "/gallery/heroUrl",
            },
            fit: "cover",
            variant: "largeFeature",
          },
          {
            id: "divider-1",
            component: "Divider",
            axis: "horizontal",
          },
          {
            id: "thumbnails-section",
            component: "Column",
            children: [
              "thumbnails-label",
              "thumbnails-row",
            ],
            justify: "start",
            align: "stretch",
          },
          {
            id: "thumbnails-label",
            component: "Text",
            text: "Thumbnails (contain fit)",
            variant: "caption",
          },
          {
            id: "thumbnails-row",
            component: "Row",
            children: [
              "thumb-1",
              "thumb-2",
              "thumb-3",
              "thumb-4",
            ],
            justify: "spaceEvenly",
            align: "center",
          },
          {
            id: "thumb-1",
            component: "Image",
            url: "https://picsum.photos/seed/a2ui1/150/150",
            fit: "contain",
            variant: "smallFeature",
          },
          {
            id: "thumb-2",
            component: "Image",
            url: "https://picsum.photos/seed/a2ui2/150/150",
            fit: "contain",
            variant: "smallFeature",
          },
          {
            id: "thumb-3",
            component: "Image",
            url: "https://picsum.photos/seed/a2ui3/150/150",
            fit: "contain",
            variant: "smallFeature",
          },
          {
            id: "thumb-4",
            component: "Image",
            url: "https://picsum.photos/seed/a2ui4/150/150",
            fit: "contain",
            variant: "smallFeature",
          },
          {
            id: "divider-2",
            component: "Divider",
            axis: "horizontal",
          },
          {
            id: "avatars-section",
            component: "Column",
            children: [
              "avatars-label",
              "avatars-row",
            ],
            justify: "start",
            align: "stretch",
          },
          {
            id: "avatars-label",
            component: "Text",
            text: "Avatars (avatar hint)",
            variant: "caption",
          },
          {
            id: "avatars-row",
            component: "Row",
            children: [
              "avatar-1",
              "avatar-2",
              "avatar-3",
            ],
            justify: "start",
            align: "center",
          },
          {
            id: "avatar-1",
            component: "Image",
            url: "https://i.pravatar.cc/100?img=1",
            fit: "cover",
            variant: "avatar",
          },
          {
            id: "avatar-2",
            component: "Image",
            url: "https://i.pravatar.cc/100?img=2",
            fit: "cover",
            variant: "avatar",
          },
          {
            id: "avatar-3",
            component: "Image",
            url: "https://i.pravatar.cc/100?img=3",
            fit: "cover",
            variant: "avatar",
          },
        ],
      },
    },
  ];
