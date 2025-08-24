/**
 * DiffView Component for SNIP-DIFF - Themed Version
 * Displays diff results and provides scan controls with theme support
 */

import React, { useState } from 'react';
import { useApiClient } from '../hooks/useApiClient';
import { useAppStore } from '../store/appStore';
import { useTheme } from '../theme';

interface StatusIndicatorProps {
  status: 'idle' | 'running' | 'completed' | 'failed';
}

const StatusIndicator: React.FC<StatusIndicatorProps> = ({ status }) => {
  const { theme } = useTheme();

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return theme.colors.semantic.success;
      case 'running': return theme.colors.semantic.warning;
      case 'failed': return theme.colors.semantic.error;
      default: return theme.colors.text.tertiary;
    }
  };

  const statusStyle: React.CSSProperties = {
    padding: '4px 12px',
    borderRadius: '12px',
    fontSize: '12px',
    fontWeight: 600,
    color: 'white',
    background: getStatusColor(status),
  };

  return <div style={statusStyle}>{status.toUpperCase()}</div>;
};

interface ProgressBarProps {
  percentage: number;
}

const ProgressBar: React.FC<ProgressBarProps> = ({ percentage }) => {
  const { theme } = useTheme();

  const containerStyle: React.CSSProperties = {
    height: '8px',
    background: theme.colors.surface.pressed,
    borderRadius: '999px',
    boxShadow: theme.colors.shadows.neumorphic.pressed,
    overflow: 'hidden',
    width: '220px',
  };

  const fillStyle: React.CSSProperties = {
    height: '100%',
    width: `${Math.max(0, Math.min(100, percentage))}%`,
    background: theme.colors.gradients.primary,
    transition: 'width 0.2s ease',
  };

  return (
    <div style={containerStyle}>
      <div style={fillStyle} />
    </div>
  );
};

export const DiffView: React.FC = () => {
  const [isScanning, setIsScanning] = useState(false);
  const { theme } = useTheme();

  const { startScan, getScanResults } = useApiClient();
  const { 
    selectedPath, 
    selectedFiles, 
    diffSections,
    scanStatus,
    scanProgress,
    setDiffSections,
    setScanStatus,
    setScanProgress
  } = useAppStore();

  const handleStartScan = async () => {
    if (!selectedPath || selectedFiles.size === 0) return;

    setIsScanning(true);
    setScanStatus('running');
    setScanProgress(0);

    try {
      const response = await startScan(selectedPath);

      if (response.success) {
        // Simulate progress for demo - use direct updates instead of function
        let currentProgress = 0;
        const progressInterval = setInterval(() => {
          currentProgress += 10;
          if (currentProgress >= 100) {
            clearInterval(progressInterval);
            setScanStatus('completed');
            setIsScanning(false);
            setScanProgress(100);
          } else {
            setScanProgress(currentProgress);
          }
        }, 200);

        // Fetch results if scan has an ID
        if (response.data?.scanId) {
          const resultsResponse = await getScanResults(response.data.scanId);
          if (resultsResponse.success && resultsResponse.data) {
            setDiffSections(resultsResponse.data.sections || []);
          }
        }
      } else {
        setScanStatus('failed');
        setIsScanning(false);
      }
    } catch (error) {
      console.error('Diff scan failed:', error);
      setScanStatus('failed');
      setIsScanning(false);
    }
  };

  const handleClearResults = () => {
    setDiffSections([]);
    setScanProgress(0);
    setScanStatus('idle');
  };

  const scanButtonDisabled = !selectedPath || selectedFiles.size === 0 || isScanning;

  const containerStyle: React.CSSProperties = {
    height: '100%',
    display: 'flex',
    flexDirection: 'column',
    background: theme.colors.components.diffViewer.background,
  };

  const controlsPanelStyle: React.CSSProperties = {
    padding: '16px',
    borderBottom: `1px solid ${theme.colors.border.secondary}`,
    background: theme.colors.surface.base,
    boxShadow: theme.colors.shadows.neumorphic.pressed,
  };

  const controlsRowStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    marginBottom: '8px',
  };

  const scanButtonStyle: React.CSSProperties = {
    padding: '8px 16px',
    background: scanButtonDisabled 
      ? theme.colors.surface.pressed
      : theme.colors.gradients.primary,
    border: 'none',
    borderRadius: '8px',
    cursor: scanButtonDisabled ? 'not-allowed' : 'pointer',
    fontSize: '14px',
    color: scanButtonDisabled ? theme.colors.text.disabled : 'white',
    boxShadow: theme.colors.shadows.neumorphic.raised,
    transition: 'all 0.2s ease',
    opacity: scanButtonDisabled ? 0.6 : 1,
  };

  const secondaryButtonStyle: React.CSSProperties = {
    padding: '8px 16px',
    background: theme.colors.surface.base,
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '14px',
    color: theme.colors.text.primary,
    boxShadow: theme.colors.shadows.neumorphic.raised,
    transition: 'all 0.2s ease',
  };

  const contentStyle: React.CSSProperties = {
    flex: 1,
    overflow: 'auto',
    padding: '16px',
  };

  const emptyStateStyle: React.CSSProperties = {
    textAlign: 'center',
    color: theme.colors.text.secondary,
    fontSize: '14px',
    padding: '40px',
  };

  const diffItemStyle: React.CSSProperties = {
    padding: '12px',
    marginBottom: '8px',
    background: theme.colors.background.card,
    borderRadius: '8px',
    boxShadow: theme.colors.shadows.neumorphic.raised,
    borderLeft: `4px solid ${theme.colors.components.diffViewer.modified}`,
  };

  return (
    <div style={containerStyle}>
      <div style={controlsPanelStyle}>
        <div style={controlsRowStyle}>
          <button
            style={scanButtonStyle}
            onClick={handleStartScan}
            disabled={scanButtonDisabled}
            onMouseEnter={(e) => {
              if (!scanButtonDisabled) {
                e.currentTarget.style.transform = 'translateY(-1px)';
                e.currentTarget.style.boxShadow = theme.colors.shadows.neumorphic.float;
              }
            }}
            onMouseLeave={(e) => {
              if (!scanButtonDisabled) {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = theme.colors.shadows.neumorphic.raised;
              }
            }}
          >
            {isScanning ? '⏸ Scanning...' : '🔍 Start Scan'}
          </button>

          <button
            style={secondaryButtonStyle}
            onClick={handleClearResults}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-1px)';
              e.currentTarget.style.boxShadow = theme.colors.shadows.neumorphic.float;
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = theme.colors.shadows.neumorphic.raised;
            }}
          >
            🗑 Clear
          </button>

          <StatusIndicator status={(scanStatus as 'idle' | 'running' | 'completed' | 'failed') || 'idle'} />
        </div>

        {isScanning && (
          <div style={{ ...controlsRowStyle, marginBottom: 0 }}>
            <ProgressBar percentage={scanProgress || 0} />
            <span style={{ fontSize: '12px', color: theme.colors.text.secondary }}>
              {scanProgress || 0}% Complete
            </span>
          </div>
        )}
      </div>

      <div style={contentStyle}>
        {diffSections.length === 0 && !isScanning && (
          <div style={emptyStateStyle}>
            {!selectedPath 
              ? 'Select a folder to begin scanning for changes'
              : selectedFiles.size === 0
                ? 'Select files from the tree to scan for differences'
                : 'Click "Start Scan" to analyze selected files'
            }
          </div>
        )}

        {diffSections.map((section, index) => (
          <div key={index} style={diffItemStyle}>
            <div style={{ 
              fontSize: '14px', 
              fontWeight: 600, 
              color: theme.colors.text.primary,
              marginBottom: '4px'
            }}>
              {section.title || `Section ${index + 1}`}
            </div>
            <div style={{ 
              fontSize: '12px', 
              color: theme.colors.text.secondary 
            }}>
              {section.files?.length || 0} files • Multiple modifications
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
