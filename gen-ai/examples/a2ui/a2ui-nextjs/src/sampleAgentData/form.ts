// ============================================================================
// SAMPLE: Form - All input field types
// ============================================================================
export const formSample = [
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
          form: {
            name: "John Doe",
            email: "john@example.com",
            password: "",
            age: 25,
            bio: "Software developer passionate about UI/UX.",
            dob: "1999-01-15",
            agreeTerms: {
              value: false,
              label: "I agree to the Terms of Service",
            },
            newsletter: {
              value: true,
              label: "Subscribe to newsletter",
            },
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
            child: "form-content",
          },
          {
            id: "form-content",
            component: "Column",
            children: [
              "form-header",
              "form-description",
              "divider-top",
              "name-field",
              "email-field",
              "password-field",
              "age-field",
              "bio-field",
              "date-field",
              "single-select-field",
              "multi-select-field",
              "divider-mid",
              "checkbox-section",
              "divider-bottom",
              "button-row",
            ],
            justify: "start",
            align: "stretch",
          },
          {
            id: "form-header",
            component: "Text",
            text: "Registration Form",
            variant: "h2",
          },
          {
            id: "form-description",
            component: "Text",
            text: "Complete all fields to create your account",
            variant: "caption",
          },
          {
            id: "divider-top",
            component: "Divider",
            axis: "horizontal",
          },
          {
            id: "name-field",
            component: "TextField",
            label: "Full Name",
            value: {
              path: "/form/name",
            },
            variant: "shortText",
          },
          {
            id: "email-field",
            component: "TextField",
            label: "Email Address",
            validationRegexp: "^[\\w-\\.]+@([\\w-]+\\.)+[\\w-]{2,4}$",
            value: {
              path: "/form/email",
            },
            variant: "shortText",
          },
          {
            id: "password-field",
            component: "TextField",
            label: "Password",
            value: {
              path: "/form/password",
            },
            variant: "obscured",
          },
          {
            id: "age-field",
            component: "TextField",
            label: "Age",
            value: {
              path: "/form/age",
            },
            variant: "number",
          },
          {
            id: "bio-field",
            component: "TextField",
            label: "Bio (Optional)",
            value: {
              path: "/form/bio",
            },
            variant: "longText",
          },
          {
            id: "date-field",
            component: "DateTimeInput",
            label: "Date of Birth",
            value: {
              path: "/form/dob",
            },
            enableDate: true,
            enableTime: false,
          },
          {
            id: "single-select-field",
            component: "ChoicePicker",
            label: "Account Plan",
            options: [
              {
                value: "free",
                label: "Free",
              },
              {
                value: "pro",
                label: "Pro",
              },
              {
                value: "enterprise",
                label: "Enterprise",
              },
            ],
            value: {
              path: "/form/plan",
            },
            displayStyle: "chips",
            variant: "mutuallyExclusive",
          },
          {
            id: "multi-select-field",
            component: "ChoicePicker",
            label: "Areas of Interest",
            options: [
              {
                value: "frontend",
                label: "Frontend",
              },
              {
                value: "backend",
                label: "Backend",
              },
              {
                value: "devops",
                label: "DevOps",
              },
              {
                value: "design",
                label: "Design",
              },
            ],
            value: {
              path: "/form/interests",
            },
            displayStyle: "chips",
            variant: "multipleSelection",
          },
          {
            id: "divider-mid",
            component: "Divider",
            axis: "horizontal",
          },
          {
            id: "checkbox-section",
            component: "Column",
            children: [
              "terms-checkbox",
              "newsletter-checkbox",
            ],
            justify: "start",
            align: "start",
          },
          {
            id: "terms-checkbox",
            component: "CheckBox",
            label: {
              path: "/form/agreeTerms/label",
            },
            value: {
              path: "/form/agreeTerms/value",
            },
          },
          {
            id: "newsletter-checkbox",
            component: "CheckBox",
            label: {
              path: "/form/newsletter/label",
            },
            value: {
              path: "/form/newsletter/value",
            },
          },
          {
            id: "divider-bottom",
            component: "Divider",
            axis: "horizontal",
          },
          {
            id: "button-row",
            component: "Row",
            children: [
              "cancel-btn",
              "submit-btn",
            ],
            justify: "end",
            align: "center",
          },
          {
            id: "cancel-btn",
            component: "Button",
            child: "cancel-text",
            action: {
              event: {
                name: "form_cancel",
              },
            },
            variant: "default",
          },
          {
            id: "cancel-text",
            component: "Text",
            text: "Cancel",
            variant: "body",
          },
          {
            id: "submit-btn",
            component: "Button",
            child: "submit-text",
            action: {
              event: {
                name: "form_submit",
                context: {
                  name: {
                    path: "/form/name",
                  },
                  email: {
                    path: "/form/email",
                  },
                  password: {
                    path: "/form/password",
                  },
                  age: {
                    path: "/form/age",
                  },
                  bio: {
                    path: "/form/bio",
                  },
                  dob: {
                    path: "/form/dob",
                  },
                  plan: {
                    path: "/form/plan",
                  },
                  interests: {
                    path: "/form/interests",
                  },
                  agreeTerms: {
                    path: "/form/agreeTerms/value",
                  },
                  newsletter: {
                    path: "/form/newsletter/value",
                  },
                },
              },
            },
            variant: "primary",
          },
          {
            id: "submit-text",
            component: "Text",
            text: "Create Account",
            variant: "body",
          },
        ],
      },
    },
  ];
