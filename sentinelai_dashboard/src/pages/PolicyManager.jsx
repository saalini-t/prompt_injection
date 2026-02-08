import React from 'react';
import { Tile, Grid, Column, Tag } from '@carbon/react';

const PolicyManager = () => {
  const policies = [
    {
      level: 'Low Risk',
      range: '0.0 - 0.45',
      action: 'Allow',
      description: 'Low confidence threats are allowed through',
      color: 'green'
    },
    {
      level: 'Medium Risk',
      range: '0.45 - 0.65',
      action: 'Sanitize',
      description: 'Moderate threats are sanitized before processing',
      color: 'yellow'
    },
    {
      level: 'High Risk',
      range: '0.65 - 1.0',
      action: 'Block',
      description: 'High confidence threats are immediately blocked',
      color: 'red'
    }
  ];

  return (
    <div>
      <h2 style={{ marginBottom: '2rem' }}>Policy Manager</h2>
      <Grid fullWidth>
        {policies.map((policy, index) => (
          <Column key={index} lg={5} md={4} sm={4}>
            <Tile style={{ padding: '1.5rem', height: '100%' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <h4>{policy.level}</h4>
                <Tag type={policy.color}>{policy.action}</Tag>
              </div>
              <p style={{ fontSize: '0.875rem', color: '#525252', marginBottom: '1rem' }}>
                {policy.description}
              </p>
              <div style={{ backgroundColor: '#f4f4f4', padding: '0.75rem', borderRadius: '4px' }}>
                <strong>Confidence Range:</strong> {policy.range}
              </div>
            </Tile>
          </Column>
        ))}
      </Grid>
    </div>
  );
};

export default PolicyManager;
