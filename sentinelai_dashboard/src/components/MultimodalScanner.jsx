import React, { useState, useRef } from 'react';
import {
  Button,
  TextArea,
  FileUploaderButton,
  Tile,
  InlineLoading,
  Tag,
} from '@carbon/react';
import { Send, Close } from '@carbon/icons-react';
import TextHeatmap from './TextHeatmap';
import LiveFeed from './LiveFeed';
import LiveTrace from './LiveTrace';
import AttackLogs from '../pages/AttackLogs';
import './MultimodalScanner.scss';

export default function MultimodalScanner() {
  const [text, setText] = useState('');
  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleImageSelect = (files) => {
    if (files && files.length > 0) {
      const file = files[0];
      setImage(file);
      
      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const clearImage = () => {
    setImage(null);
    setImagePreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const removeImage = () => {
    clearImage();
  };

  const handleScan = async () => {
    if (!text.trim() && !image) {
      setError('Please enter text or upload an image');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      if (text.trim()) {
        formData.append('text', text);
      }
      if (image) {
        formData.append('file', image);
      }

      const apiBase = import.meta.env.VITE_API_BASE_URL || '';
      const buildApiUrl = (path) => (apiBase ? `${apiBase}${path}` : path);

      const response = await fetch(buildApiUrl('/api/v1/security/full-scan'), {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(`Error: ${err.message}`);
      console.error('Scan error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getDecisionColor = (decision) => {
    switch (decision?.toLowerCase()) {
      case 'block':
        return 'red';
      case 'sanitize':
        return 'orange';
      case 'allow':
        return 'green';
      default:
        return 'gray';
    }
  };

  const getRiskBadge = (risk) => {
    if (risk >= 0.85) return { label: 'CRITICAL', color: 'red' };
    if (risk >= 0.75) return { label: 'HIGH', color: 'orange' };
    if (risk >= 0.5) return { label: 'MEDIUM', color: 'blue' };
    return { label: 'SAFE', color: 'green' };
  };

  return (
    <div className="multimodal-scanner">
      <Tile className="scanner-header">
        <div className="header-content">
          <h2>🔍 Multimodal Security Scanner</h2>
          <p>Comprehensive threat detection with AI & Vision Analysis</p>
        </div>
      </Tile>

      <div className="scanner-grid">
        {/* Input Panel */}
        <Tile className="input-panel">
          <div className="section-title">📝 Input Analysis</div>
          
          <div className="input-section">
            <label className="section-label">Text Prompt</label>
            <TextArea
              id="prompt-input"
              placeholder="Enter your prompt here... (e.g., 'Explain ethical AI')"
              value={text}
              onChange={(e) => setText(e.target.value)}
              rows={5}
              disabled={loading}
              maxCount={2000}
            />
          </div>

          <div className="divider">OR</div>

          <div className="image-upload-section">
            <label className="section-label">Image for Deepfake Detection</label>
            
            {imagePreview ? (
              <div className="image-preview-container">
                <img src={imagePreview} alt="Preview" className="image-preview" />
                <Button
                  kind="ghost"
                  size="sm"
                  icon={Close}
                  onClick={removeImage}
                  className="remove-image-btn"
                >
                  Remove
                </Button>
              </div>
            ) : (
              <FileUploaderButton
                ref={fileInputRef}
                buttonKind="primary"
                accept={['.jpg', '.jpeg', '.png', '.webp']}
                onChange={(e) => handleImageSelect(e.target.files)}
                disabled={loading}
                multiple={false}
              />
            )}
          </div>

          <Button
            onClick={handleScan}
            disabled={loading || (!text.trim() && !image)}
            size="lg"
            renderIcon={Send}
            className="scan-button"
          >
            {loading ? 'Scanning...' : 'Run Full Scan'}
          </Button>
        </Tile>

        {/* Results Panel */}
        {result && (
          <div className="results-section">
            {/* Heatmap Visualization */}
            {result.heatmap && text && (
              <TextHeatmap heatmapData={result.heatmap} riskScore={result.hybrid_analysis?.risk} />
            )}

            {/* Decision Badge */}
            <Tile className="decision-tile">
              <div className="decision-header">
                <h3>Final Decision</h3>
                <Tag
                  type={getDecisionColor(result.hybrid_analysis?.decision)}
                  size="lg"
                >
                  {result.hybrid_analysis?.decision?.toUpperCase() || 'UNKNOWN'}
                </Tag>
              </div>
              <div className="risk-score">
                <span className="label">Risk Score:</span>
                <span className={`score ${getRiskBadge(result.hybrid_analysis?.risk)?.color}`}>
                  {(result.hybrid_analysis?.risk * 100).toFixed(1)}%
                </span>
              </div>
              <div className="risk-badge">
                <Tag type={getRiskBadge(result.hybrid_analysis?.risk)?.color} size="md">
                  {getRiskBadge(result.hybrid_analysis?.risk)?.label}
                </Tag>
              </div>
            </Tile>

            {/* Risk Analysis Grid */}
            <Tile className="risk-grid">
              <div className="section-title">📊 Risk Analysis Breakdown</div>
              
              <div className="risk-items">
                {/* Text Risk */}
                {result.text_analysis && (
                  <div className="risk-item">
                    <div className="risk-item-header">
                      <span className="icon">💬</span>
                      <span className="label">Text Injection Risk</span>
                    </div>
                    <div className="risk-item-body">
                      <div className="confidence">{(result.text_analysis.confidence * 100).toFixed(1)}%</div>
                      {result.text_analysis.malicious && (
                        <Tag type="red" size="sm">MALICIOUS</Tag>
                      )}
                    </div>
                  </div>
                )}

                {/* Ethics Risk */}
                {result.ethics_analysis && (
                  <div className="risk-item">
                    <div className="risk-item-header">
                      <span className="icon">⚖️</span>
                      <span className="label">Ethics Guardian</span>
                    </div>
                    <div className="risk-item-body">
                      <div className="confidence">{(result.ethics_analysis.score * 100).toFixed(1)}%</div>
                      {result.ethics_analysis.ethical_risk && (
                        <Tag type="red" size="sm">ETHICAL VIOLATION</Tag>
                      )}
                    </div>
                  </div>
                )}

                {/* Vision Risk */}
                {result.vision_analysis && (
                  <div className="risk-item">
                    <div className="risk-item-header">
                      <span className="icon">👁️</span>
                      <span className="label">Deepfake Detection</span>
                    </div>
                    <div className="risk-item-body">
                      <div className="confidence">{(result.vision_analysis.deepfake_score * 100).toFixed(1)}%</div>
                      {result.vision_analysis.face_detected && (
                        <Tag type="blue" size="sm">FACE DETECTED</Tag>
                      )}
                    </div>
                  </div>
                )}

                {/* Intent/Narrative Risk */}
                {result.text_analysis?.narrative && (
                  <div className="risk-item">
                    <div className="risk-item-header">
                      <span className="icon">🧠</span>
                      <span className="label">Intent Analysis</span>
                    </div>
                    <div className="risk-item-body">
                      <div className="confidence">{(result.text_analysis.narrative.confidence * 100).toFixed(1)}%</div>
                      {result.text_analysis.narrative.malicious && (
                        <Tag type="orange" size="sm">DECEPTIVE</Tag>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </Tile>

            {/* Intent Reasoning */}
            {(result.ethics_analysis?.ethical_risk || result.text_analysis?.narrative?.signals?.length > 0) && (
              <Tile className="reasoning-tile">
                <div className="section-title">🔍 Threat Analysis</div>
                
                {result.ethics_analysis?.ethical_risk && (
                  <div className="reasoning-block">
                    <div className="reasoning-label">⚠️ Ethical Violation Detected:</div>
                    <div className="reasoning-content">
                      {result.ethics_analysis.reason ? (
                        <Tag type="red">{result.ethics_analysis.reason}</Tag>
                      ) : (
                        <p>Unethical content detected in prompt</p>
                      )}
                    </div>
                  </div>
                )}

                {result.text_analysis?.narrative?.signals?.length > 0 && (
                  <div className="reasoning-block">
                    <div className="reasoning-label">📋 Detected Patterns:</div>
                    <div className="signals-list">
                      {result.text_analysis.narrative.signals.map((signal, idx) => (
                        <Tag key={idx} type="blue" size="sm">
                          {signal}
                        </Tag>
                      ))}
                    </div>
                  </div>
                )}

                {result.text_analysis?.injection && (
                  <div className="reasoning-block">
                    <div className="reasoning-label">🎯 Triggered By:</div>
                    <div className="triggered-list">
                      {result.text_analysis.injection.triggered_by?.map((trigger, idx) => (
                        <Tag key={idx} type="orange" size="sm">
                          {trigger} attack
                        </Tag>
                      ))}
                    </div>
                  </div>
                )}
              </Tile>
            )}

            {/* Policy & Vision Details */}
            {(result.policy_analysis || result.vision_analysis?.artifacts) && (
              <Tile className="details-tile">
                <div className="section-title">📋 Additional Details</div>
                
                {result.policy_analysis && (
                  <div className="detail-block">
                    <div className="detail-label">Policy Check:</div>
                    <Tag type={result.policy_analysis.compliant ? 'green' : 'red'} size="md">
                      {result.policy_analysis.compliant ? 'COMPLIANT' : 'POLICY VIOLATION'}
                    </Tag>
                  </div>
                )}

                {result.vision_analysis?.artifacts && (
                  <div className="detail-block">
                    <div className="detail-label">Image Analysis:</div>
                    <div style={{display: 'table', width: '100%', borderCollapse: 'collapse'}}>
                      <div style={{display: 'table-header-group', fontWeight: 'bold'}}>
                        <div style={{display: 'table-row', borderBottom: '1px solid rgba(0, 150, 255, 0.3)'}}>
                          <div style={{display: 'table-cell', padding: '0.5rem', textAlign: 'left'}}>Metric</div>
                          <div style={{display: 'table-cell', padding: '0.5rem', textAlign: 'left'}}>Value</div>
                        </div>
                      </div>
                      <div style={{display: 'table-row-group'}}>
                        {result.vision_analysis.artifacts.blur_score !== undefined && (
                          <div style={{display: 'table-row', borderBottom: '1px solid rgba(0, 150, 255, 0.1)'}}>
                            <div style={{display: 'table-cell', padding: '0.5rem'}}>Blur Score</div>
                            <div style={{display: 'table-cell', padding: '0.5rem'}}>{(result.vision_analysis.artifacts.blur_score).toFixed(3)}</div>
                          </div>
                        )}
                        {result.vision_analysis.artifacts.laplacian !== undefined && (
                          <div style={{display: 'table-row', borderBottom: '1px solid rgba(0, 150, 255, 0.1)'}}>
                            <div style={{display: 'table-cell', padding: '0.5rem'}}>Laplacian</div>
                            <div style={{display: 'table-cell', padding: '0.5rem'}}>{(result.vision_analysis.artifacts.laplacian).toFixed(2)}</div>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                )}
              </Tile>
            )}
          </div>
        )}

        {/* Error State */}
        {error && (
          <Tile className="error-tile">
            <div className="error-content">
              <span className="error-icon">❌</span>
              <span className="error-message">{error}</span>
            </div>
          </Tile>
        )}

        {/* Loading State */}
        {loading && (
          <Tile className="loading-tile">
            <InlineLoading description="Scanning with AI & Vision Models..." status="active" />
          </Tile>
        )}
      </div>

      <div className="telemetry-section">
        <div className="telemetry-grid">
          <Tile className="telemetry-tile live-feed-tile">
            <h4>📡 Live Attack Stream</h4>
            <LiveFeed />
          </Tile>

          <LiveTrace />
        </div>

        <Tile className="telemetry-tile logs-tile">
          <h4>🧾 Attack Logs</h4>
          <AttackLogs showTitle={false} />
        </Tile>
      </div>
    </div>
  );
}
