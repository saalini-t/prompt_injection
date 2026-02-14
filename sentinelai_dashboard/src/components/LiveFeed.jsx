import React, { useState, useEffect, useRef } from 'react';
import { Tag, CodeSnippet } from '@carbon/react';
import './LiveFeed.scss';

const LiveFeed = () => {
  const [events, setEvents] = useState([]);
  const feedRef = useRef(null);
  const wsRef = useRef(null);

  useEffect(() => {
    const wsBase = import.meta.env.VITE_WS_BASE_URL
      || `${window.location.protocol === 'https:' ? 'wss' : 'ws'}://${window.location.host}`;
    const ws = new WebSocket(`${wsBase}/attacks`);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log('LiveFeed: WebSocket connected to /attacks');
    };

    ws.onmessage = (event) => {
      try {
        const attackData = JSON.parse(event.data);
        const newEvent = {
          id: Date.now() + Math.random(),
          timestamp: new Date().toLocaleTimeString(),
          prompt: attackData.text || attackData.original || attackData.prompt || 'N/A',
          decision: attackData.decision || 'allow',
          confidence: (attackData.risk || attackData.confidence || 0).toFixed(2),
          mlScore: (attackData.injection?.ml_score || attackData.ml_score || 0).toFixed(2),
          similarity: (attackData.injection?.similarity || attackData.similarity || 0).toFixed(2)
        };
        setEvents(prev => [newEvent, ...prev].slice(0, 50));
      } catch (err) {
        console.error('Error parsing attack event:', err);
      }
    };

    ws.onerror = (error) => {
      console.error('LiveFeed WebSocket error:', error);
    };

    ws.onclose = () => {
      console.log('LiveFeed: WebSocket disconnected');
    };

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  const getDecisionTag = (decision) => {
    const types = {
      block: { type: 'red', label: 'BLOCKED' },
      sanitize: { type: 'yellow', label: 'SANITIZED' },
      allow: { type: 'green', label: 'ALLOWED' }
    };
    return types[decision] || types.allow;
  };

  return (
    <div className="live-feed" ref={feedRef}>
      {events.length === 0 ? (
        <div style={{ padding: '1rem', textAlign: 'center', color: '#888' }}>
          Waiting for attack events...
        </div>
      ) : (
        events.map((event) => {
          const tagInfo = getDecisionTag(event.decision);
          return (
            <div key={event.id} className="feed-item">
              <div className="feed-item-header">
                <span className="feed-timestamp">{event.timestamp}</span>
                <Tag type={tagInfo.type} size="sm">{tagInfo.label}</Tag>
              </div>
              <div className="feed-item-content">
                <CodeSnippet type="single" feedback="Copied!" className="feed-prompt">
                  {event.prompt}
                </CodeSnippet>
                <div className="feed-metrics">
                  <span>Confidence: {event.confidence}</span>
                  <span>ML: {event.mlScore}</span>
                  <span>Similarity: {event.similarity}</span>
                </div>
              </div>
            </div>
          );
        })
      )}
    </div>
  );
};

export default LiveFeed;
