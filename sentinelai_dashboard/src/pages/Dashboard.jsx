import React, { useState, useEffect } from 'react';
import {
  Grid,
  Column,
  Tile,
  StructuredListWrapper,
  StructuredListHead,
  StructuredListRow,
  StructuredListCell,
  StructuredListBody,
  Tag,
  Loading
} from '@carbon/react';
import { 
  Security, 
  CheckmarkFilled, 
  WarningFilled,
  ErrorFilled 
} from '@carbon/icons-react';
import MetricsCard from '../components/MetricsCard';
import ThreatChart from '../components/ThreatChart';
import LiveFeed from '../components/LiveFeed';
import LiveTrace from '../components/LiveTrace';
import AttackSimulator from '../components/AttackSimulator';
import axios from 'axios';
import './Dashboard.scss';

const Dashboard = () => {
  const [metrics, setMetrics] = useState(null);
  const [systemStatus, setSystemStatus] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMetrics();
    fetchSystemStatus();
    const interval = setInterval(fetchMetrics, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchMetrics = async () => {
    try {
      const response = await axios.get('/api/v1/metrics/summary');
      setMetrics(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch metrics:', error);
      // Mock data for demo
      setMetrics({
        totalRequests: 1247,
        blockedAttacks: 89,
        sanitizedRequests: 234,
        allowedRequests: 924,
        avgConfidence: 0.78
      });
      setLoading(false);
    }
  };

  const fetchSystemStatus = () => {
    setSystemStatus([
      { layer: 'Prompt Injection Detection', status: 'operational', uptime: '99.9%' },
      { layer: 'ML Classifier', status: 'operational', uptime: '99.8%' },
      { layer: 'Hybrid Scoring Engine', status: 'operational', uptime: '100%' },
      { layer: 'Redis Policy Cache', status: 'operational', uptime: '99.7%' },
      { layer: 'MongoDB Telemetry', status: 'operational', uptime: '99.9%' },
      { layer: 'Kafka Event Streaming', status: 'operational', uptime: '99.5%' },
      { layer: 'WebSocket Live Feed', status: 'operational', uptime: '99.6%' },
      { layer: 'Tool Firewall', status: 'operational', uptime: '100%' },
      { layer: 'Policy Engine', status: 'operational', uptime: '100%' }
    ]);
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'operational':
        return <CheckmarkFilled size={16} style={{ color: '#24a148' }} />;
      case 'degraded':
        return <WarningFilled size={16} style={{ color: '#f1c21b' }} />;
      case 'down':
        return <ErrorFilled size={16} style={{ color: '#da1e28' }} />;
      default:
        return null;
    }
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
        <Loading description="Loading dashboard..." withOverlay={false} />
      </div>
    );
  }

  return (
    <div className="dashboard-page">
      <h2 className="dashboard-title">Security Operations Dashboard</h2>
      
      {/* Attack Simulator - NEW */}
      <AttackSimulator />

      <Grid fullWidth narrow>
        {/* Metrics Cards */}
        <Column lg={4} md={4} sm={4}>
          <MetricsCard
            title="Total Requests"
            value={metrics?.totalRequests || 0}
            icon={Security}
            trend="+12%"
            trendType="neutral"
          />
        </Column>
        <Column lg={4} md={4} sm={4}>
          <MetricsCard
            title="Blocked Attacks"
            value={metrics?.blockedAttacks || 0}
            icon={Security}
            trend="-8%"
            trendType="positive"
          />
        </Column>
        <Column lg={4} md={4} sm={4}>
          <MetricsCard
            title="Sanitized"
            value={metrics?.sanitizedRequests || 0}
            icon={Security}
            trend="+5%"
            trendType="neutral"
          />
        </Column>

        {/* Threat Chart */}
        <Column lg={10} md={8} sm={4}>
          <Tile className="dashboard-tile">
            <h4>Threat Activity - Last 24 Hours</h4>
            <ThreatChart />
          </Tile>
        </Column>

        {/* Live Feed */}
        <Column lg={6} md={4} sm={4}>
          <Tile className="dashboard-tile live-feed-tile">
            <h4>Live Attack Feed</h4>
            <LiveFeed />
          </Tile>
        </Column>

        {/* Execution Trace */}
        <Column lg={6} md={4} sm={4}>
          <LiveTrace />
        </Column>

        {/* System Status */}
        <Column lg={16} md={8} sm={4}>
          <Tile className="dashboard-tile">
            <h4 style={{ marginBottom: '1rem' }}>System Status</h4>
            <StructuredListWrapper>
              <StructuredListHead>
                <StructuredListRow head>
                  <StructuredListCell head>Layer</StructuredListCell>
                  <StructuredListCell head>Status</StructuredListCell>
                  <StructuredListCell head>Uptime</StructuredListCell>
                </StructuredListRow>
              </StructuredListHead>
              <StructuredListBody>
                {systemStatus.map((item, index) => (
                  <StructuredListRow key={index}>
                    <StructuredListCell>{item.layer}</StructuredListCell>
                    <StructuredListCell>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        {getStatusIcon(item.status)}
                        <Tag type={item.status === 'operational' ? 'green' : 'red'}>
                          {item.status}
                        </Tag>
                      </div>
                    </StructuredListCell>
                    <StructuredListCell>{item.uptime}</StructuredListCell>
                  </StructuredListRow>
                ))}
              </StructuredListBody>
            </StructuredListWrapper>
          </Tile>
        </Column>
      </Grid>
    </div>
  );
};

export default Dashboard;
