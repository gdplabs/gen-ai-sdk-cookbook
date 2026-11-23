// ============================================================================
// SAMPLE: Product - Product card with actions
// ============================================================================
export const productSample = [
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
        product: {
          id: "PRD-12345",
          image: "https://picsum.photos/seed/product/400/300",
          category: "Electronics > Audio",
          name: "Premium Wireless Headphones",
          rating: "★★★★☆ 4.5 (128 reviews)",
          price: "$199.99",
          originalPrice: "$249.99 (-20%)",
          description: "Experience crystal-clear audio with active noise cancellation, 30-hour battery life, and premium comfort for all-day listening.",
          quantity: 1
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
          child: "productContent"
        },
        {
          id: "productContent",
          component: "Column",
          children: [
            "productImage",
            "productDetails",
            "productActions"
          ],
          justify: "start",
          align: "stretch"
        },
        {
          id: "productImage",
          component: "Image",
          url: {
            "@path": "/product/image"
          },
          fit: "contain",
          variant: "largeFeature"
        },
        {
          id: "productDetails",
          component: "Column",
          children: [
            "productCategory",
            "productName",
            "productRating",
            "productPrice",
            "productDescription"
          ],
          justify: "start",
          align: "stretch"
        },
        {
          id: "productCategory",
          component: "Text",
          text: {
            "@path": "/product/category"
          },
          variant: "caption"
        },
        {
          id: "productName",
          component: "Text",
          text: {
            "@call": "formatString",
            args: {
              value: "### ${/product/name}"
            }
          }
        },
        {
          id: "productRating",
          component: "Text",
          text: {
            "@path": "/product/rating"
          },
          variant: "caption"
        },
        {
          id: "productPrice",
          component: "Row",
          children: [
            "currentPrice",
            "originalPrice"
          ],
          justify: "start",
          align: "center"
        },
        {
          id: "currentPrice",
          component: "Text",
          text: {
            "@call": "formatString",
            args: {
              value: "## ${/product/price}"
            }
          }
        },
        {
          id: "originalPrice",
          component: "Text",
          text: {
            "@path": "/product/originalPrice"
          },
          variant: "caption"
        },
        {
          id: "productDescription",
          component: "Text",
          text: {
            "@path": "/product/description"
          },
          variant: "body"
        },
        {
          id: "productActions",
          component: "Column",
          children: [
            "quantityRow",
            "divider",
            "buttonRow"
          ],
          justify: "start",
          align: "stretch"
        },
        {
          id: "quantityRow",
          component: "Row",
          children: [
            "quantityLabel",
            "quantityField"
          ],
          justify: "spaceBetween",
          align: "center"
        },
        {
          id: "quantityLabel",
          component: "Text",
          text: "Quantity",
          variant: "body"
        },
        {
          id: "quantityField",
          component: "TextField",
          label: "",
          value: {
            "@path": "/product/quantity"
          },
          variant: "number"
        },
        {
          id: "divider",
          component: "Divider",
          axis: "horizontal"
        },
        {
          id: "buttonRow",
          component: "Row",
          children: [
            "wishlistBtn",
            "cartBtn"
          ],
          justify: "spaceEvenly",
          align: "center"
        },
        {
          id: "wishlistBtn",
          component: "Button",
          catalogId: "https://github.com/GDP-ADMIN/glchat-sdk/blob/main/js/glchat-a2ui-react-renderer/json/v1_0/glchat_extension_catalog_definition.json",
          child: "wishlistText",
          action: {
            event: {
              name: "add_to_wishlist",
              context: {
                productId: {
                  "@path": "/product/id"
                }
              }
            }
          },
          variant: "default"
        },
        {
          id: "wishlistText",
          component: "Text",
          text: "♡ Wishlist",
          variant: "body"
        },
        {
          id: "cartBtn",
          component: "Button",
          catalogId: "https://github.com/GDP-ADMIN/glchat-sdk/blob/main/js/glchat-a2ui-react-renderer/json/v1_0/glchat_extension_catalog_definition.json",
          child: "cartText",
          action: {
            event: {
              name: "add_to_cart",
              context: {
                productId: {
                  "@path": "/product/id"
                },
                quantity: {
                  "@path": "/product/quantity"
                }
              }
            }
          },
          variant: "primary"
        },
        {
          id: "cartText",
          component: "Text",
          text: "🛒 Add to Cart",
          variant: "body"
        }
      ]
    }
  }
];
