// ============================================================================
// SAMPLE: Form - All input field types
// ============================================================================
export const formSample = [
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
        form: {
          name: "John Doe",
          email: "john@example.com",
          password: "",
          age: 25,
          bio: "Software developer passionate about UI/UX.",
          dob: "1999-01-15",
          agreeTerms: {
            value: false,
            label: "I agree to the Terms of Service"
          },
          newsletter: {
            value: true,
            label: "Subscribe to newsletter"
          }
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
          child: "formContent"
        },
        {
          id: "formContent",
          component: "Column",
          children: [
            "formHeader",
            "formDescription",
            "dividerTop",
            "nameField",
            "emailField",
            "passwordField",
            "ageField",
            "bioField",
            "dateField",
            "singleSelectField",
            "multiSelectField",
            "dividerMid",
            "checkboxSection",
            "dividerBottom",
            "buttonRow"
          ],
          justify: "start",
          align: "stretch"
        },
        {
          id: "formHeader",
          component: "Text",
          text: "## Registration Form"
        },
        {
          id: "formDescription",
          component: "Text",
          text: "Complete all fields to create your account",
          variant: "caption"
        },
        {
          id: "dividerTop",
          component: "Divider",
          axis: "horizontal"
        },
        {
          id: "nameField",
          component: "TextField",
          label: "Full Name",
          value: {
            "@path": "/form/name"
          },
          variant: "shortText"
        },
        {
          id: "emailField",
          component: "TextField",
          label: "Email Address",
          value: {
            "@path": "/form/email"
          },
          variant: "shortText",
          checks: [
            {
              condition: {
                "@call": "email",
                args: {
                  value: {
                    "@path": "/form/email"
                  }
                }
              },
              message: "Please enter a valid email address."
            }
          ]
        },
        {
          id: "passwordField",
          component: "TextField",
          label: "Password",
          value: {
            "@path": "/form/password"
          },
          variant: "obscured"
        },
        {
          id: "ageField",
          component: "TextField",
          label: "Age",
          value: {
            "@path": "/form/age"
          },
          variant: "number"
        },
        {
          id: "bioField",
          component: "TextField",
          label: "Bio (Optional)",
          value: {
            "@path": "/form/bio"
          },
          variant: "longText"
        },
        {
          id: "dateField",
          component: "DateTimeInput",
          label: "Date of Birth",
          value: {
            "@path": "/form/dob"
          },
          enableDate: true,
          enableTime: false
        },
        {
          id: "singleSelectField",
          component: "ChoicePicker",
          catalogId: "https://github.com/GDP-ADMIN/glchat-sdk/blob/main/js/glchat-a2ui-react-renderer/json/v1_0/glchat_extension_catalog_definition.json",
          label: "Account Plan",
          options: [
            {
              value: "free",
              label: "Free"
            },
            {
              value: "pro",
              label: "Pro"
            },
            {
              value: "enterprise",
              label: "Enterprise"
            }
          ],
          value: {
            "@path": "/form/plan"
          },
          displayStyle: "chips",
          variant: "mutuallyExclusive"
        },
        {
          id: "multiSelectField",
          component: "ChoicePicker",
          catalogId: "https://github.com/GDP-ADMIN/glchat-sdk/blob/main/js/glchat-a2ui-react-renderer/json/v1_0/glchat_extension_catalog_definition.json",
          label: "Areas of Interest",
          options: [
            {
              value: "frontend",
              label: "Frontend"
            },
            {
              value: "backend",
              label: "Backend"
            },
            {
              value: "devops",
              label: "DevOps"
            },
            {
              value: "design",
              label: "Design"
            }
          ],
          value: {
            "@path": "/form/interests"
          },
          displayStyle: "chips",
          variant: "multipleSelection"
        },
        {
          id: "dividerMid",
          component: "Divider",
          axis: "horizontal"
        },
        {
          id: "checkboxSection",
          component: "Column",
          children: [
            "termsCheckbox",
            "newsletterCheckbox"
          ],
          justify: "start",
          align: "start"
        },
        {
          id: "termsCheckbox",
          component: "CheckBox",
          label: {
            "@path": "/form/agreeTerms/label"
          },
          value: {
            "@path": "/form/agreeTerms/value"
          }
        },
        {
          id: "newsletterCheckbox",
          component: "CheckBox",
          label: {
            "@path": "/form/newsletter/label"
          },
          value: {
            "@path": "/form/newsletter/value"
          }
        },
        {
          id: "dividerBottom",
          component: "Divider",
          axis: "horizontal"
        },
        {
          id: "buttonRow",
          component: "Row",
          children: [
            "cancelBtn",
            "submitBtn"
          ],
          justify: "end",
          align: "center"
        },
        {
          id: "cancelBtn",
          component: "Button",
          catalogId: "https://github.com/GDP-ADMIN/glchat-sdk/blob/main/js/glchat-a2ui-react-renderer/json/v1_0/glchat_extension_catalog_definition.json",
          child: "cancelText",
          action: {
            event: {
              name: "form_cancel"
            }
          },
          variant: "default"
        },
        {
          id: "cancelText",
          component: "Text",
          text: "Cancel",
          variant: "body"
        },
        {
          id: "submitBtn",
          component: "Button",
          catalogId: "https://github.com/GDP-ADMIN/glchat-sdk/blob/main/js/glchat-a2ui-react-renderer/json/v1_0/glchat_extension_catalog_definition.json",
          child: "submitText",
          action: {
            event: {
              name: "form_submit",
              context: {
                name: {
                  "@path": "/form/name"
                },
                email: {
                  "@path": "/form/email"
                },
                password: {
                  "@path": "/form/password"
                },
                age: {
                  "@path": "/form/age"
                },
                bio: {
                  "@path": "/form/bio"
                },
                dob: {
                  "@path": "/form/dob"
                },
                plan: {
                  "@path": "/form/plan"
                },
                interests: {
                  "@path": "/form/interests"
                },
                agreeTerms: {
                  "@path": "/form/agreeTerms/value"
                },
                newsletter: {
                  "@path": "/form/newsletter/value"
                }
              }
            }
          },
          variant: "primary"
        },
        {
          id: "submitText",
          component: "Text",
          text: "Create Account",
          variant: "body"
        }
      ]
    }
  }
];
