// ============================================================================
// SAMPLE: HITL - Human-in-the-loop approval workflow
// ============================================================================
export const hitlSample = 
[
  {
    surfaceUpdate: {
        surfaceId: 'header',
        components: [
          {
            id: 'root',
            component: {
              Row: {
                children: { 'explicitList': ['title', 'icon'] },
                distribution: 'start',
                alignment: 'center',
              },
            },
          },
          {
            id: 'title',
            component: {
              Text: { text: { path: '/header/title' }, usageHint: 'h2' },
            },
          },
          {
            id: 'icon',
            component: {
              Text: { text: { path: '/header/icon' }, usageHint: 'h2' },
            },
          },
        ],
      }
    },
    {
      dataModelUpdate: {
        surfaceId: 'header',
        contents: [
          {
            key: 'header',
            valueMap: [
              { key: 'title', valueString: 'Approval Required' },
              { key: 'icon', valueString: '⚠️' },
            ],
          },
        ],
      },
    },
    {
      beginRendering: {
        surfaceId: 'header',
        root: 'root',
      },
    },
    {
      surfaceUpdate: {
        surfaceId: 'hitl',
        components: [
          {
            id: 'root',
            component: {
              Column: {
                children: { 'explicitList': ['action-card'] },
                distribution: 'start',
                alignment: 'stretch',
              },
            },
          },
          {
            id: 'hitl-header',
            component: {
              Row: {
                children: { 'explicitList': ['header-icon', 'header-text'] },
                distribution: 'start',
                alignment: 'center',
              },
            },
          },
          {
            id: 'header-icon',
            component: {
              Text: { text: { path: '/hitl/icon' }, usageHint: 'h2' },
            },
          },
          {
            id: 'header-text',
            component: {
              Text: {
                text: { path: '/hitl/title' },
                usageHint: 'h2',
              },
            },
          },
          // Action card
          {
            id: 'action-card',
            component: { Card: { child: 'action-content' } },
          },
          {
            id: 'action-content',
            component: {
              Column: {
                children: { 'explicitList': ['action-label-row', 'action-buttons'] },
                distribution: 'start',
                alignment: 'stretch',
              },
            },
          },
          {
            id: 'action-label-row',
            component: {
              Row: {
                children: { 'explicitList': ['action-label', 'hitl-timeout'] },
                distribution: 'start',
                alignment: 'center',
              },
            },
          },
          {
            id: 'action-label',
            component: {
              Text: {
                text: { literalString: 'Please review and take action:' },
                usageHint: 'body',
              },
            },
          },
          {
            id: 'hitl-timeout',
            component: {
              Timeout: {
                targetTimeUtc: { path: '/hitl/expiresAt' },
                usageHint: 'caption',
              },
            },
          },
          {
            id: 'action-buttons',
            component: {
              Row: {
                children: { 'explicitList': ['approve-btn', 'reject-btn', 'skip-btn'] },
                distribution: 'start',
                alignment: 'start',
              },
            },
          },
          {
            id: 'approve-btn',
            component: {
              Button: {
                child: 'approve-text',
                action: {
                  name: 'hitl_decision',
                  context: [
                    { key: 'decision', value: { literalString: 'approved' } },
                    { key: 'requestId', value: { path: '/hitl/requestId' } },
                  ],
                },
                primary: true,
              },
            },
          },
          {
            id: 'approve-text',
            component: {
              Text: { text: { literalString: '✓ Approve' }, usageHint: 'body' },
            },
          },
          {
            id: 'reject-btn',
            component: {
              Button: {
                child: 'reject-text',
                action: {
                  name: 'hitl_decision',
                  context: [
                    { key: 'decision', value: { literalString: 'rejected' } },
                    { key: 'requestId', value: { path: '/hitl/requestId' } },
                  ],
                },
                primary: false,
                destructive: true,
              },
            },
          },
          {
            id: 'reject-text',
            component: {
              Text: { text: { literalString: '✗ Reject' }, usageHint: 'body' },
            },
          },
          {
            id: 'skip-btn',
            component: {
              Button: {
                child: 'skip-text',
                action: {
                  name: 'hitl_decision',
                  context: [
                    { key: 'decision', value: { literalString: 'skipped' } },
                    { key: 'requestId', value: { path: '/hitl/requestId' } },
                  ],
                },
                primary: false,
              },
            },
          },
          {
            id: 'skip-text',
            component: {
              Text: { text: { literalString: 'Skip' }, usageHint: 'body' },
            },
          },
        ],
      },
    },
    {
      dataModelUpdate: {
        surfaceId: 'hitl',
        contents: [
          {
            key: 'hitl',
            valueMap: [
              { key: 'requestId', valueString: 'REQ-2024-00847' },
              {
                key: 'expiresAt',
                valueString: '2026-03-11T12:00:00Z',
              },
            ],
          },
        ],
      },
    },
    {
      beginRendering: {
        surfaceId: 'hitl',
        root: 'root',
      },
    },
];
