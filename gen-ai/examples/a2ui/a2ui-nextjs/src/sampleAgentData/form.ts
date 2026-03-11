// ============================================================================
// SAMPLE: Form - All input field types
// ============================================================================
export const formSample = [
  {
    surfaceUpdate: {
      surfaceId: "main",
      components: [
        {
          id: "root",
          component: {
            Card: { child: "form-content" },
          },
        },
        {
          id: "form-content",
          component: {
            Column: {
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
                "divider-mid",
                "checkbox-section",
                "divider-bottom",
                "button-row",
              ],
              distribution: "start",
              alignment: "stretch",
            },
          },
        },
        {
          id: "form-header",
          component: {
            Text: {
              text: { literalString: "Registration Form" },
              usageHint: "h2",
            },
          },
        },
        {
          id: "form-description",
          component: {
            Text: {
              text: {
                literalString: "Complete all fields to create your account",
              },
              usageHint: "caption",
            },
          },
        },
        {
          id: "divider-top",
          component: { Divider: { axis: "horizontal" } },
        },
        {
          id: "name-field",
          component: {
            TextField: {
              label: { literalString: "Full Name" },
              text: { path: "/form/name" },
              textFieldType: "shortText",
            },
          },
        },
        {
          id: "email-field",
          component: {
            TextField: {
              label: { literalString: "Email Address" },
              text: { path: "/form/email" },
              textFieldType: "shortText",
              validationRegexp: "^[\\w-\\.]+@([\\w-]+\\.)+[\\w-]{2,4}$",
            },
          },
        },
        {
          id: "password-field",
          component: {
            TextField: {
              label: { literalString: "Password" },
              text: { path: "/form/password" },
              textFieldType: "obscured",
            },
          },
        },
        {
          id: "age-field",
          component: {
            TextField: {
              label: { literalString: "Age" },
              text: { path: "/form/age" },
              textFieldType: "number",
            },
          },
        },
        {
          id: "bio-field",
          component: {
            TextField: {
              label: { literalString: "Bio (Optional)" },
              text: { path: "/form/bio" },
              textFieldType: "longText",
            },
          },
        },
        {
          id: "date-field",
          component: {
            TextField: {
              label: { literalString: "Date of Birth" },
              text: { path: "/form/dob" },
              textFieldType: "date",
            },
          },
        },
        {
          id: "divider-mid",
          component: { Divider: { axis: "horizontal" } },
        },
        {
          id: "checkbox-section",
          component: {
            Column: {
              children: ["terms-checkbox", "newsletter-checkbox"],
              distribution: "start",
              alignment: "start",
            },
          },
        },
        {
          id: "terms-checkbox",
          component: {
            CheckBox: {
              label: { literalString: "I agree to the Terms of Service" },
              checked: { path: "/form/agreeTerms" },
            },
          },
        },
        {
          id: "newsletter-checkbox",
          component: {
            CheckBox: {
              label: { literalString: "Subscribe to newsletter" },
              checked: { path: "/form/newsletter" },
            },
          },
        },
        {
          id: "divider-bottom",
          component: { Divider: { axis: "horizontal" } },
        },
        {
          id: "button-row",
          component: {
            Row: {
              children: ["cancel-btn", "submit-btn"],
              distribution: "end",
              alignment: "center",
            },
          },
        },
        {
          id: "cancel-btn",
          component: {
            Button: {
              child: "cancel-text",
              action: { name: "form_cancel", context: {} },
              primary: false,
            },
          },
        },
        {
          id: "cancel-text",
          component: {
            Text: { text: { literalString: "Cancel" }, usageHint: "body" },
          },
        },
        {
          id: "submit-btn",
          component: {
            Button: {
              child: "submit-text",
              action: {
                name: "form_submit",
                context: [
                  { key: "name", value: { path: "/form/name" } },
                  { key: "email", value: { path: "/form/email" } },
                  {
                    key: "password",
                    value: { path: "/form/password" },
                  },
                  { key: "age", value: { path: "/form/age" } },
                  { key: "bio", value: { path: "/form/bio" } },
                  { key: "dob", value: { path: "/form/dob" } },
                  {
                    key: "agreeTerms",
                    value: { path: "/form/agreeTerms" },
                  },
                  {
                    key: "newsletter",
                    value: { path: "/form/newsletter" },
                  },
                ],
              },
              primary: true,
            },
          },
        },
        {
          id: "submit-text",
          component: {
            Text: {
              text: { literalString: "Create Account" },
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
          key: "form",
          valueMap: [
            { key: "name", valueString: "John Doe" },
            { key: "email", valueString: "john@example.com" },
            { key: "password", valueString: "" },
            { key: "age", valueNumber: 25 },
            {
              key: "bio",
              valueString: "Software developer passionate about UI/UX.",
            },
            { key: "dob", valueString: "1999-01-15" },
            { key: "agreeTerms", valueMap: [
              { key: "value", valueBoolean: false },
              { key: "label", valueString: "I agree to the Terms of Service" }
            ] },
            { key: "newsletter", valueMap: [
              { key: "value", valueBoolean: true },
              { key: "label", valueString: "Subscribe to newsletter" }
            ] },
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
