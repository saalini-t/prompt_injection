import React from 'react';
import './TextHeatmap.scss';

export default function TextHeatmap({ heatmapData, riskScore }) {
  if (!heatmapData || !heatmapData.segments) {
    return null;
  }

  const getColorClass = (color) => {
    switch (color) {
      case 'red':
        return 'heatmap-critical';
      case 'orange':
        return 'heatmap-high';
      case 'yellow':
        return 'heatmap-medium';
      case 'green':
        return 'heatmap-safe';
      default:
        return 'heatmap-neutral';
    }
  };

  return (
    <div className="text-heatmap">
      <div className="heatmap-header">
        <h4>Text Analysis Heatmap</h4>
        <div className="heatmap-legend">
          <span className="legend-item critical">Critical</span>
          <span className="legend-item high">High Risk</span>
          <span className="legend-item medium">Medium</span>
          <span className="legend-item safe">Safe</span>
        </div>
      </div>

      <div className="heatmap-display">
        <div className="heatmap-container">
          {heatmapData.segments.map((segment, idx) => (
            <span
              key={idx}
              className={`heatmap-segment ${getColorClass(segment.color)}`}
              title={segment.reason || ''}
            >
              {segment.text}
            </span>
          ))}
        </div>
      </div>

      {heatmapData.highlighted_words && heatmapData.highlighted_words.length > 0 && (
        <div className="highlighted-terms">
          <h5>Detected Trigger Words:</h5>
          <div className="terms-list">
            {heatmapData.highlighted_words.map((word, idx) => (
              <span key={idx} className="trigger-tag">
                {word}
              </span>
            ))}
          </div>
        </div>
      )}

      <div className="risk-gauge">
        <div className="gauge-label">Risk Heat Level: {(heatmapData.risk_heat * 100).toFixed(1)}%</div>
        <div className="gauge-bar">
          <div
            className="gauge-fill"
            style={{
              width: `${heatmapData.risk_heat * 100}%`,
              backgroundColor: heatmapData.risk_heat >= 0.85 ? '#ff5050' :
                                heatmapData.risk_heat >= 0.75 ? '#f1c21b' :
                                heatmapData.risk_heat >= 0.5 ? '#0096ff' : '#42be65'
            }}
          />
        </div>
      </div>
    </div>
  );
}
