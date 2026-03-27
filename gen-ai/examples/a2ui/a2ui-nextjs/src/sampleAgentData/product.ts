// ============================================================================
// SAMPLE: Product - E-commerce product card
// ============================================================================
export const productSample = [
  {
    surfaceUpdate: {
      surfaceId: "main",
      components: [
        {
          id: "root",
          component: { Card: { child: "product-content" } },
        },
        {
          id: "product-content",
          component: {
            Column: {
              children: { explicitList: ["product-image", "product-details", "product-actions"] },
              distribution: "start",
              alignment: "stretch",
            },
          },
        },
        {
          id: "product-image",
          component: {
            Image: {
              url: { path: "/product/image" },
              fit: "contain",
              usageHint: "hero",
            },
          },
        },
        {
          id: "product-details",
          component: {
            Column: {
              children: {
                explicitList: [
                  "product-category",
                  "product-name",
                  "product-rating",
                  "product-price",
                  "product-description",
                ],
              },
              distribution: "start",
              alignment: "stretch",
            },
          },
        },
        {
          id: "product-category",
          component: {
            Text: { text: { path: "/product/category" }, usageHint: "caption" },
          },
        },
        {
          id: "product-name",
          component: {
            Text: { text: { path: "/product/name" }, usageHint: "h3" },
          },
        },
        {
          id: "product-rating",
          component: {
            Text: { text: { path: "/product/rating" }, usageHint: "caption" },
          },
        },
        {
          id: "product-price",
          component: {
            Row: {
              children: { explicitList: ["current-price", "original-price"] },
              distribution: "start",
              alignment: "center",
            },
          },
        },
        {
          id: "current-price",
          component: {
            Text: { text: { path: "/product/price" }, usageHint: "h2" },
          },
        },
        {
          id: "original-price",
          component: {
            Text: {
              text: { path: "/product/originalPrice" },
              usageHint: "caption",
            },
          },
        },
        {
          id: "product-description",
          component: {
            Text: { text: { path: "/product/description" }, usageHint: "body" },
          },
        },
        // Quantity and actions
        {
          id: "product-actions",
          component: {
            Column: {
              children: { explicitList: ["quantity-row", "divider", "button-row"] },
              distribution: "start",
              alignment: "stretch",
            },
          },
        },
        {
          id: "quantity-row",
          component: {
            Row: {
              children: { explicitList: ["quantity-label", "quantity-field"] },
              distribution: "spaceBetween",
              alignment: "center",
            },
          },
        },
        {
          id: "quantity-label",
          component: {
            Text: { text: { literalString: "Quantity" }, usageHint: "body" },
          },
        },
        {
          id: "quantity-field",
          component: {
            TextField: {
              text: { path: "/product/quantity" },
              textFieldType: "number",
            },
          },
        },
        {
          id: "divider",
          component: { Divider: { axis: "horizontal" } },
        },
        {
          id: "button-row",
          component: {
            Row: {
              children: { explicitList: ["wishlist-btn", "cart-btn"] },
              distribution: "spaceEvenly",
              alignment: "center",
            },
          },
        },
        {
          id: "wishlist-btn",
          component: {
            Button: {
              child: "wishlist-text",
              action: {
                name: "add_to_wishlist",
                context: [{ key: "productId", value: { path: "/product/id" } }],
              },
              primary: false,
            },
          },
        },
        {
          id: "wishlist-text",
          component: {
            Text: { text: { literalString: "♡ Wishlist" }, usageHint: "body" },
          },
        },
        {
          id: "cart-btn",
          component: {
            Button: {
              child: "cart-text",
              action: {
                name: "add_to_cart",
                context: [
                  { key: "productId", value: { path: "/product/id" } },
                  { key: "quantity", value: { path: "/product/quantity" } },
                ],
              },
              primary: true,
            },
          },
        },
        {
          id: "cart-text",
          component: {
            Text: {
              text: { literalString: "🛒 Add to Cart" },
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
          key: "product",
          valueMap: [
            { key: "id", valueString: "PRD-12345" },
            {
              key: "image",
              valueString: "https://picsum.photos/seed/product/400/300",
            },
            { key: "category", valueString: "Electronics > Audio" },
            { key: "name", valueString: "Premium Wireless Headphones" },
            { key: "rating", valueString: "★★★★☆ 4.5 (128 reviews)" },
            { key: "price", valueString: "$199.99" },
            { key: "originalPrice", valueString: "$249.99 (-20%)" },
            {
              key: "description",
              valueString:
                "Experience crystal-clear audio with active noise cancellation, 30-hour battery life, and premium comfort for all-day listening.",
            },
            { key: "quantity", valueNumber: 1 },
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
