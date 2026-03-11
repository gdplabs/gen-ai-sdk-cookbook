// ============================================================================
// SAMPLE: Gallery - Image showcase with all fit types
// ============================================================================
export const gallerySample = [
  {
    surfaceUpdate: {
      surfaceId: "main",
      components: [
        {
          id: "root",
          component: {
            Column: {
              children: { "explicitList": [
                "gallery-header",
                "hero-section",
                "divider-1",
                "thumbnails-section",
                "divider-2",
                "avatars-section",
              ] },
              distribution: "start",
              alignment: "stretch",
            },
          },
        },
        {
          id: "gallery-header",
          component: {
            Text: {
              text: { literalString: "Image Gallery" },
              usageHint: "h2",
            },
          },
        },
        // Hero image section
        {
          id: "hero-section",
          component: {
            Column: {
              children: { "explicitList": ["hero-label", "hero-image"] },
              distribution: "start",
              alignment: "stretch",
            },
          },
        },
        {
          id: "hero-label",
          component: {
            Text: {
              text: { literalString: "Hero Image (cover fit)" },
              usageHint: "caption",
            },
          },
        },
        {
          id: "hero-image",
          component: {
            Image: {
              url: { path: "/gallery/heroUrl" },
              fit: "cover",
              usageHint: "hero",
            },
          },
        },
        {
          id: "divider-1",
          component: { Divider: { axis: "horizontal" } },
        },
        // Thumbnails section
        {
          id: "thumbnails-section",
          component: {
            Column: {
              children: { "explicitList": ["thumbnails-label", "thumbnails-row"] },
              distribution: "start",
              alignment: "stretch",
            },
          },
        },
        {
          id: "thumbnails-label",
          component: {
            Text: {
              text: { literalString: "Thumbnails (contain fit)" },
              usageHint: "caption",
            },
          },
        },
        {
          id: "thumbnails-row",
          component: {
            Row: {
              children: { "explicitList": ["thumb-1", "thumb-2", "thumb-3", "thumb-4"] },
              distribution: "spaceEvenly",
              alignment: "center",
            },
          },
        },
        {
          id: "thumb-1",
          component: {
            Image: {
              url: {
                literalString: "https://picsum.photos/seed/a2ui1/150/150",
              },
              fit: "contain",
              usageHint: "thumbnail",
            },
          },
        },
        {
          id: "thumb-2",
          component: {
            Image: {
              url: {
                literalString: "https://picsum.photos/seed/a2ui2/150/150",
              },
              fit: "contain",
              usageHint: "thumbnail",
            },
          },
        },
        {
          id: "thumb-3",
          component: {
            Image: {
              url: {
                literalString: "https://picsum.photos/seed/a2ui3/150/150",
              },
              fit: "contain",
              usageHint: "thumbnail",
            },
          },
        },
        {
          id: "thumb-4",
          component: {
            Image: {
              url: {
                literalString: "https://picsum.photos/seed/a2ui4/150/150",
              },
              fit: "contain",
              usageHint: "thumbnail",
            },
          },
        },
        {
          id: "divider-2",
          component: { Divider: { axis: "horizontal" } },
        },
        // Avatars section
        {
          id: "avatars-section",
          component: {
            Column: {
              children: { "explicitList": ["avatars-label", "avatars-row"] },
              distribution: "start",
              alignment: "stretch",
            },
          },
        },
        {
          id: "avatars-label",
          component: {
            Text: {
              text: { literalString: "Avatars (avatar hint)" },
              usageHint: "caption",
            },
          },
        },
        {
          id: "avatars-row",
          component: {
            Row: {
              children: { "explicitList": ["avatar-1", "avatar-2", "avatar-3"] },
              distribution: "start",
              alignment: "center",
            },
          },
        },
        {
          id: "avatar-1",
          component: {
            Image: {
              url: { literalString: "https://i.pravatar.cc/100?img=1" },
              fit: "cover",
              usageHint: "avatar",
            },
          },
        },
        {
          id: "avatar-2",
          component: {
            Image: {
              url: { literalString: "https://i.pravatar.cc/100?img=2" },
              fit: "cover",
              usageHint: "avatar",
            },
          },
        },
        {
          id: "avatar-3",
          component: {
            Image: {
              url: { literalString: "https://i.pravatar.cc/100?img=3" },
              fit: "cover",
              usageHint: "avatar",
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
          key: "gallery",
          valueMap: [
            {
              key: "heroUrl",
              valueString: "https://picsum.photos/seed/hero/800/400",
            },
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
