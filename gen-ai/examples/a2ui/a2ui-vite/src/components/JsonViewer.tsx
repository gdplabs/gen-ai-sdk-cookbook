import { useState } from 'react';

interface JsonViewerProps {
  readonly data: unknown;
  readonly label?: string;
}

export function JsonViewer({ data, label = 'Sample Messages (JSON)' }: JsonViewerProps) {
  const [open, setOpen] = useState(false);

  return (
    <div className="json-viewer">
      <button
        className="json-viewer-toggle"
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
      >
        {open ? '▾' : '▸'} {label}
      </button>
      {open && (
        <pre className="json-viewer-content">
          {JSON.stringify(data, null, 2)}
        </pre>
      )}
    </div>
  );
}
