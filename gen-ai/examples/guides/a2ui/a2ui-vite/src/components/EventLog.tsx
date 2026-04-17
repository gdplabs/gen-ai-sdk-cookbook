import { forwardRef, useImperativeHandle, useState } from 'react';

export interface EventLogHandler {
  addEvent: (raw: unknown) => void;
  clear: () => void;
}

interface LogEntry {
  id: number;
  timestamp: string;
  raw: unknown;
}

let nextId = 0;

export const EventLog = forwardRef<EventLogHandler>((_props, ref) => {
  const [entries, setEntries] = useState<LogEntry[]>([]);

  useImperativeHandle(ref, () => ({
    addEvent(raw: unknown) {
      setEntries((prev) => [
        { id: nextId++, timestamp: new Date().toLocaleTimeString(), raw },
        ...prev,
      ]);
    },
    clear() {
      setEntries([]);
    },
  }));

  return (
    <div className="event-log">
      <div className="event-log-header">
        <h2>Event Log</h2>
        {entries.length > 0 && (
          <button className="event-log-clear" onClick={() => setEntries([])}>
            Clear
          </button>
        )}
      </div>
      {entries.length === 0 ? (
        <p className="event-log-empty">
          Interact with the components below to see raw userAction events here.
        </p>
      ) : (
        <ul className="event-log-list">
          {entries.map((entry) => (
            <li key={entry.id} className="event-log-entry">
              <span className="event-log-time">{entry.timestamp}</span>
              <pre className="event-log-raw">
                {JSON.stringify(entry.raw, null, 2)}
              </pre>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
});
