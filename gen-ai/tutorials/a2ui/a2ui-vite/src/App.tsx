import { useEffect, useRef } from 'react';
import {
  useA2UIProcessor,
  A2UISurface,
  DEFAULT_CATALOG,
} from 'glchat-a2ui-react-renderer';
import sampleMessages from './data/sample-messages.json';
import { EventLog, EventLogHandler } from './components/EventLog';
import { JsonViewer } from './components/JsonViewer';
import { Header } from './components/Header';

export default function App() {
  const { processor, surfaces, refreshSurfaces } = useA2UIProcessor();
  const eventLogRef = useRef<EventLogHandler>(null);

  useEffect(() => {
    const messages = structuredClone(sampleMessages);
    processor.processMessages(messages as any);
    refreshSurfaces();
  }, [processor, refreshSurfaces]);

  useEffect(() => {
    const unsubscribe = processor.events.subscribe((event) => {
      eventLogRef.current?.addEvent(event.message);
      event.completion([]);
    });
    return unsubscribe;
  }, [processor]);

  return (
    <div className="app-layout">
      <Header />

      <EventLog ref={eventLogRef} />

      <JsonViewer data={sampleMessages} />

      <div className="surface-container">
        {Array.from(surfaces.entries()).map(([surfaceId, surface]) => (
          <A2UISurface
            key={surfaceId}
            surfaceId={surfaceId}
            surface={surface}
            processor={processor}
            refreshSurfaces={refreshSurfaces}
            catalog={DEFAULT_CATALOG}
          />
        ))}
      </div>
    </div>
  );
}
