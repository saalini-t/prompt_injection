import React, { useEffect, useState, useRef } from 'react';
import { Tile, Tag } from '@carbon/react';
import './LiveTrace.scss';

const STEP_ICONS = {
  'Prompt Received': '🛡',
  'Hybrid Detector Score': '🧠',
  'Policy Decision': '📜',
  'Redis Cache Check': '⚡',
  'Prompt Sanitized': '🧼',
  'MongoDB Log Saved': '📦',
  'Kafka Event Produced': '🌊',
  'WebSocket Broadcast': '📡',
  'Pipeline Complete': '✅'
};

const LiveTrace = () => {
  const [traces, setTraces] = useState([]);
  const wsRef = useRef(null);

  useEffect(() => {
    const wsBase = import.meta.env.VITE_WS_BASE_URL
      || `${window.location.protocol === 'https:' ? 'wss' : 'ws'}://${window.location.host}`;
    const ws = new WebSocket(`${wsBase}/trace`);
    wsRef.current = ws;

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setTraces((prev) => [data, ...prev].slice(0, 50));
      } catch (err) {
        console.error('Trace parse error', err);
      }
    };

    ws.onerror = () => console.warn('Trace WebSocket error');

    return () => {
      ws.close();
    };
  }, []);

  const formatTime = (ts) => {
    return new Date(ts * 1000).toLocaleTimeString();
  };

  return (
    <Tile className="live-trace">
      <h4>🧠 Firewall Execution Trace</h4>
      <p className="subtitle">Watch every step of the prompt firewall in real time.</p>

      <div className="trace-list">
        {traces.length === 0 && (
          <div className="empty">Waiting for traces... Submit a prompt in the simulator.</div>
        )}
        {traces.map((trace, idx) => (
          <div key={idx} className="trace-item">
            <div className="trace-time">{formatTime(trace.ts)}</div>
            <div className="trace-body">
              <span className="trace-icon">{STEP_ICONS[trace.step] || '🔹'}</span>
              <div className="trace-text">
                <div className="trace-step">{trace.step}</div>
                {trace.meta && Object.keys(trace.meta).length > 0 && (
                  <div className="trace-meta">
                    {Object.entries(trace.meta).map(([k, v]) => (
                      <Tag key={k} type="cool-gray" size="sm">{k}: {String(v)}</Tag>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </Tile>
  );
};

export default LiveTrace;
