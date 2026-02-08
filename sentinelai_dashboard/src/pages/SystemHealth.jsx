import React from 'react';
import { Tile, Grid, Column, ProgressBar, Tag } from '@carbon/react';
import { CheckmarkFilled } from '@carbon/icons-react';

const SystemHealth = () => {
  const components = [
    { name: 'Prompt Injection Detection (Sentence Transformers)', health: 100, status: 'operational', uptime: '99.9%' },
    { name: 'ML Classifier (TF-IDF + Logistic Regression)', health: 98, status: 'operational', uptime: '99.8%' },
    { name: 'Hybrid Scoring Engine', health: 100, status: 'operational', uptime: '100%' },
    { name: 'Redis Policy Cache', health: 97, status: 'operational', uptime: '99.7%' },
    { name: 'MongoDB Telemetry Store', health: 99, status: 'operational', uptime: '99.9%' },
    { name: 'Kafka Cloud Event Streaming', health: 95, status: 'operational', uptime: '99.5%' },
    { name: 'WebSocket Live Feed', health: 96, status: 'operational', uptime: '99.6%' },
    { name: 'Tool Firewall', health: 100, status: 'operational', uptime: '100%' },
    { name: 'Policy Engine', health: 100, status: 'operational', uptime: '100%' }
  ];

  return (
    <div>
      <h2 style={{ marginBottom: '2rem' }}>System Health</h2>
      <Grid fullWidth>
        {components.map((component, index) => (
          <Column key={index} lg={8} md={4} sm={4}>
            <Tile style={{ padding: '1.5rem', marginBottom: '1rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <h4 style={{ fontSize: '1rem' }}>{component.name}</h4>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <CheckmarkFilled size={16} style={{ color: '#24a148' }} />
                  <Tag type="green" size="sm">{component.status}</Tag>
                </div>
              </div>
              <div style={{ marginBottom: '0.5rem' }}>
                <ProgressBar 
                  value={component.health} 
                  label="Health" 
                  helperText={`${component.health}% - Uptime: ${component.uptime}`}
                />
              </div>
            </Tile>
          </Column>
        ))}
      </Grid>
    </div>
  );
};

export default SystemHealth;
