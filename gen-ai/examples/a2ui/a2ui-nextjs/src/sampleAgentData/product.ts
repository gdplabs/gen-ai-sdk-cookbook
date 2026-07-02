// ============================================================================
// SAMPLE: Product - Product card with actions
// ============================================================================
export const productSample = [
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
          product: {
            id: "PRD-12345",
            image: "https://picsum.photos/seed/product/400/300",
            category: "Electronics > Audio",
            name: "Premium Wireless Headphones",
            rating: "★★★★☆ 4.5 (128 reviews)",
            price: "$199.99",
            originalPrice: "$249.99 (-20%)",
            description: "Experience crystal-clear audio with active noise cancellation, 30-hour battery life, and premium comfort for all-day listening.",
            quantity: 1,
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
            child: "product-content",
          },
          {
            id: "product-content",
            component: "Column",
            children: [
              "product-image",
              "product-details",
              "product-actions",
            ],
            justify: "start",
            align: "stretch",
          },
          {
            id: "product-image",
            component: "Image",
            url: {
              path: "/product/image",
            },
            fit: "contain",
            variant: "largeFeature",
          },
          {
            id: "product-details",
            component: "Column",
            children: [
              "product-category",
              "product-name",
              "product-rating",
              "product-price",
              "product-description",
            ],
            justify: "start",
            align: "stretch",
          },
          {
            id: "product-category",
            component: "Text",
            text: {
              path: "/product/category",
            },
            variant: "caption",
          },
          {
            id: "product-name",
            component: "Text",
            text: {
              path: "/product/name",
            },
            variant: "h3",
          },
          {
            id: "product-rating",
            component: "Text",
            text: {
              path: "/product/rating",
            },
            variant: "caption",
          },
          {
            id: "product-price",
            component: "Row",
            children: [
              "current-price",
              "original-price",
            ],
            justify: "start",
            align: "center",
          },
          {
            id: "current-price",
            component: "Text",
            text: {
              path: "/product/price",
            },
            variant: "h2",
          },
          {
            id: "original-price",
            component: "Text",
            text: {
              path: "/product/originalPrice",
            },
            variant: "caption",
          },
          {
            id: "product-description",
            component: "Text",
            text: {
              path: "/product/description",
            },
            variant: "body",
          },
          {
            id: "product-actions",
            component: "Column",
            children: [
              "quantity-row",
              "divider",
              "button-row",
            ],
            justify: "start",
            align: "stretch",
          },
          {
            id: "quantity-row",
            component: "Row",
            children: [
              "quantity-label",
              "quantity-field",
            ],
            justify: "spaceBetween",
            align: "center",
          },
          {
            id: "quantity-label",
            component: "Text",
            text: "Quantity",
            variant: "body",
          },
          {
            id: "quantity-field",
            component: "TextField",
            label: "",
            value: {
              path: "/product/quantity",
            },
            variant: "number",
          },
          {
            id: "divider",
            component: "Divider",
            axis: "horizontal",
          },
          {
            id: "button-row",
            component: "Row",
            children: [
              "wishlist-btn",
              "cart-btn",
            ],
            justify: "spaceEvenly",
            align: "center",
          },
          {
            id: "wishlist-btn",
            component: "Button",
            child: "wishlist-text",
            action: {
              event: {
                name: "add_to_wishlist",
                context: {
                  productId: {
                    path: "/product/id",
                  },
                },
              },
            },
            variant: "default",
          },
          {
            id: "wishlist-text",
            component: "Text",
            text: "♡ Wishlist",
            variant: "body",
          },
          {
            id: "cart-btn",
            component: "Button",
            child: "cart-text",
            action: {
              event: {
                name: "add_to_cart",
                context: {
                  productId: {
                    path: "/product/id",
                  },
                  quantity: {
                    path: "/product/quantity",
                  },
                },
              },
            },
            variant: "primary",
          },
          {
            id: "cart-text",
            component: "Text",
            text: "🛒 Add to Cart",
            variant: "body",
          },
        ],
      },
    },
  ];
