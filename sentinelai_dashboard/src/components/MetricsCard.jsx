import React from 'react';
import { Tile } from '@carbon/react';
import { ArrowUp, ArrowDown } from '@carbon/icons-react';
import './MetricsCard.scss';

const MetricsCard = ({ title, value, icon: Icon, trend, trendType }) => {
  const getTrendColor = () => {
    switch (trendType) {
      case 'positive':
        return '#24a148';
      case 'negative':
        return '#da1e28';
      default:
        return '#8d8d8d';
    }
  };

  const TrendIcon = trend?.startsWith('+') ? ArrowUp : ArrowDown;

  return (
    <Tile className="metrics-card">
      <div className="metrics-card-header">
        <span className="metrics-card-title">{title}</span>
        {Icon && <Icon size={24} className="metrics-card-icon" />}
      </div>
      <div className="metrics-card-value">{value.toLocaleString()}</div>
      {trend && (
        <div className="metrics-card-trend" style={{ color: getTrendColor() }}>
          <TrendIcon size={16} />
          <span>{trend}</span>
        </div>
      )}
    </Tile>
  );
};

export default MetricsCard;
