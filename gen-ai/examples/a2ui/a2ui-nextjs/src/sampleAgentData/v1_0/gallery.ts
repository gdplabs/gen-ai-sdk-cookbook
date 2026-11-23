// ============================================================================
// SAMPLE: Gallery - Image showcase with all fit types
// ============================================================================
export const gallerySample = [
  {
    version: "1.0",
    createSurface: {
      surfaceId: "main",
      catalogId: "https://github.com/GDP-ADMIN/glchat-sdk/blob/main/js/glchat-a2ui-react-renderer/json/v1_0/glchat_standard_catalog_definition.json"
    }
  },
  {
    version: "1.0",
    updateDataModel: {
      surfaceId: "main",
      value: {
        gallery: {
          heroUrl: "https://picsum.photos/seed/hero/800/400"
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
            "galleryHeader",
            "heroSection",
            "divider1",
            "thumbnailsSection",
            "divider2",
            "avatarsSection"
          ],
          justify: "start",
          align: "stretch"
        },
        {
          id: "galleryHeader",
          component: "Text",
          text: "## Image Gallery"
        },
        {
          id: "heroSection",
          component: "Column",
          children: [
            "heroLabel",
            "heroImage"
          ],
          justify: "start",
          align: "stretch"
        },
        {
          id: "heroLabel",
          component: "Text",
          text: "Hero Image (cover fit)",
          variant: "caption"
        },
        {
          id: "heroImage",
          component: "Image",
          url: {
            "@path": "/gallery/heroUrl"
          },
          fit: "cover",
          variant: "largeFeature"
        },
        {
          id: "divider1",
          component: "Divider",
          axis: "horizontal"
        },
        {
          id: "thumbnailsSection",
          component: "Column",
          children: [
            "thumbnailsLabel",
            "thumbnailsRow"
          ],
          justify: "start",
          align: "stretch"
        },
        {
          id: "thumbnailsLabel",
          component: "Text",
          text: "Thumbnails (contain fit)",
          variant: "caption"
        },
        {
          id: "thumbnailsRow",
          component: "Row",
          children: [
            "thumb1",
            "thumb2",
            "thumb3",
            "thumb4"
          ],
          justify: "spaceEvenly",
          align: "center"
        },
        {
          id: "thumb1",
          component: "Image",
          url: "https://picsum.photos/seed/a2ui1/150/150",
          fit: "contain",
          variant: "smallFeature"
        },
        {
          id: "thumb2",
          component: "Image",
          url: "https://picsum.photos/seed/a2ui2/150/150",
          fit: "contain",
          variant: "smallFeature"
        },
        {
          id: "thumb3",
          component: "Image",
          url: "https://picsum.photos/seed/a2ui3/150/150",
          fit: "contain",
          variant: "smallFeature"
        },
        {
          id: "thumb4",
          component: "Image",
          url: "https://picsum.photos/seed/a2ui4/150/150",
          fit: "contain",
          variant: "smallFeature"
        },
        {
          id: "divider2",
          component: "Divider",
          axis: "horizontal"
        },
        {
          id: "avatarsSection",
          component: "Column",
          children: [
            "avatarsLabel",
            "avatarsRow"
          ],
          justify: "start",
          align: "stretch"
        },
        {
          id: "avatarsLabel",
          component: "Text",
          text: "Avatars (avatar hint)",
          variant: "caption"
        },
        {
          id: "avatarsRow",
          component: "Row",
          children: [
            "avatar1",
            "avatar2",
            "avatar3"
          ],
          justify: "start",
          align: "center"
        },
        {
          id: "avatar1",
          component: "Image",
          url: "https://i.pravatar.cc/100?img=1",
          fit: "cover",
          variant: "avatar"
        },
        {
          id: "avatar2",
          component: "Image",
          url: "https://i.pravatar.cc/100?img=2",
          fit: "cover",
          variant: "avatar"
        },
        {
          id: "avatar3",
          component: "Image",
          url: "https://i.pravatar.cc/100?img=3",
          fit: "cover",
          variant: "avatar"
        }
      ]
    }
  }
];
