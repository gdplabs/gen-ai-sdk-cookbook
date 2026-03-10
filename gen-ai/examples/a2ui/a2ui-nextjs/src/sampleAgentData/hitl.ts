// ============================================================================
// SAMPLE: HITL - Human-in-the-loop approval workflow
// ============================================================================
export const hitlSample = [
  {
    surfaceUpdate: {
      surfaceId: "main",
      components: [
        {
          id: "root",
          component: {
            Column: {
              children: { "explicitList": ["hitl-header", "hitl-card", "action-card"] },
              distribution: "start",
              alignment: "stretch",
            },
          },
        },
        {
          id: "hitl-header",
          component: {
            Row: {
              children: { "explicitList": ["header-icon", "header-text"] },
              distribution: "start",
              alignment: "center",
            },
          },
        },
        {
          id: "header-icon",
          component: {
            Text: { text: { literalString: "⚠️" }, usageHint: "h2" },
          },
        },
        {
          id: "header-text",
          component: {
            Text: {
              text: { literalString: "Approval Required" },
              usageHint: "h2",
            },
          },
        },
        // Request details card
        {
          id: "hitl-card",
          component: { Card: { child: "hitl-card-content" } },
        },
        {
          id: "hitl-card-content",
          component: {
            Column: {
              children: { "explicitList": [
                "request-title",
                "request-id",
                "divider-1",
                "request-details",
                "divider-2",
                "request-reason",
              ] },
              distribution: "start",
              alignment: "stretch",
            },
          },
        },
        {
          id: "request-title",
          component: {
            Text: { text: { path: "/hitl/title" }, usageHint: "h4" },
          },
        },
        {
          id: "request-id",
          component: {
            Text: { text: { path: "/hitl/requestId" }, usageHint: "caption" },
          },
        },
        {
          id: "divider-1",
          component: { Divider: { axis: "horizontal" } },
        },
        {
          id: "request-details",
          component: {
            Column: {
              children: { "explicitList": [
                "detail-amount",
                "detail-from",
                "detail-to",
                "detail-time",
              ] },
              distribution: "start",
              alignment: "stretch",
            },
          },
        },
        {
          id: "detail-amount",
          component: {
            Row: {
              children: { "explicitList": ["amount-label", "amount-value"] },
              distribution: "spaceBetween",
              alignment: "center",
            },
          },
        },
        {
          id: "amount-label",
          component: {
            Text: { text: { literalString: "Amount" }, usageHint: "caption" },
          },
        },
        {
          id: "amount-value",
          component: {
            Text: { text: { path: "/hitl/amount" }, usageHint: "body" },
          },
        },
        {
          id: "detail-from",
          component: {
            Row: {
              children: { "explicitList": ["from-label", "from-value"] },
              distribution: "spaceBetween",
              alignment: "center",
            },
          },
        },
        {
          id: "from-label",
          component: {
            Text: { text: { literalString: "From" }, usageHint: "caption" },
          },
        },
        {
          id: "from-value",
          component: {
            Text: { text: { path: "/hitl/from" }, usageHint: "body" },
          },
        },
        {
          id: "detail-to",
          component: {
            Row: {
              children: { "explicitList": ["to-label", "to-value"] },
              distribution: "spaceBetween",
              alignment: "center",
            },
          },
        },
        {
          id: "to-label",
          component: {
            Text: { text: { literalString: "To" }, usageHint: "caption" },
          },
        },
        {
          id: "to-value",
          component: {
            Text: { text: { path: "/hitl/to" }, usageHint: "body" },
          },
        },
        {
          id: "detail-time",
          component: {
            Row: {
              children: { "explicitList": ["time-label", "time-value"] },
              distribution: "spaceBetween",
              alignment: "center",
            },
          },
        },
        {
          id: "time-label",
          component: {
            Text: {
              text: { literalString: "Expires in" },
              usageHint: "caption",
            },
          },
        },
        {
          id: "time-value",
          component: {
            Text: { text: { path: "/hitl/timeLeft" }, usageHint: "body" },
          },
        },
        {
          id: "divider-2",
          component: { Divider: { axis: "horizontal" } },
        },
        {
          id: "request-reason",
          component: {
            Text: { text: { path: "/hitl/reason" }, usageHint: "body" },
          },
        },
        // Action card
        {
          id: "action-card",
          component: { Card: { child: "action-content" } },
        },
        {
          id: "action-content",
          component: {
            Column: {
              children: { "explicitList": ["action-label-row", "action-buttons"] },
              distribution: "start",
              alignment: "stretch",
            },
          },
        },
        {
          id: "action-label-row",
          component: {
            Row: {
              children: { "explicitList": ["action-label", "hitl-timeout"] },
              distribution: "start",
              alignment: "center",
            },
          },
        },
        {
          id: "action-label",
          component: {
            Text: {
              text: { literalString: "Please review and take action:" },
              usageHint: "body",
            },
          },
        },
        {
          id: "hitl-timeout",
          component: {
            Timeout: {
              targetTimeUtc: { path: "/hitl/expiresAt" },
              usageHint: "caption",
            },
          },
        },
        {
          id: "action-buttons",
          component: {
            Row: {
              children: { "explicitList": ["approve-btn", "reject-btn", "escalate-btn"] },
              distribution: "spaceEvenly",
              alignment: "center",
            },
          },
        },
        {
          id: "approve-btn",
          component: {
            Button: {
              child: "approve-text",
              action: {
                name: "hitl_decision",
                context: [
                  { key: "decision", value: { literalString: "approved" } },
                  { key: "requestId", value: { path: "/hitl/requestId" } },
                ],
              },
              primary: true,
            },
          },
        },
        {
          id: "approve-text",
          component: {
            Text: { text: { literalString: "✓ Approve" }, usageHint: "body" },
          },
        },
        {
          id: "reject-btn",
          component: {
            Button: {
              child: "reject-text",
              action: {
                name: "hitl_decision",
                context: [
                  { key: "decision", value: { literalString: "rejected" } },
                  { key: "requestId", value: { path: "/hitl/requestId" } },
                ],
              },
              primary: false,
              destructive: true,
            },
          },
        },
        {
          id: "reject-text",
          component: {
            Text: { text: { literalString: "✗ Reject" }, usageHint: "body" },
          },
        },
        {
          id: "escalate-btn",
          component: {
            Button: {
              child: "escalate-text",
              action: {
                name: "hitl_decision",
                context: [
                  { key: "decision", value: { literalString: "escalated" } },
                  { key: "requestId", value: { path: "/hitl/requestId" } },
                ] },
              primary: false,
            },
          },
        },
        {
          id: "escalate-text",
          component: {
            Text: { text: { literalString: "↑ Escalate" }, usageHint: "body" },
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
          key: "hitl",
          valueMap: [
            { key: "title", valueString: "Wire Transfer Request" },
            { key: "requestId", valueString: "REQ-2024-00847" },
            { key: "amount", valueString: "$15,000.00 USD" },
            { key: "from", valueString: "Operations Account (*4521)" },
            { key: "to", valueString: "Vendor Payment Account" },
            { key: "timeLeft", valueString: "4 minutes 32 seconds" },
            {
              key: "expiresAt",
              valueString: "2026-02-13T15:00:00.000Z",
            },
            {
              key: "reason",
              valueString:
                "This transfer exceeds the automatic approval limit of $10,000. Manual review required per company policy.",
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
