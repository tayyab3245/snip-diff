/**
 * DiffView Component for SNIP-DIFF
 * Displays diff results and provides scan controls
 */

import React, { useState } from 'react';
import styled from 'styled-components';
import { useApiClient } from '../hooks/useApiClient';
import { useAppStore } from '../store/appStore';

const DiffViewContainer = styled.div`
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #e0e5ec;
`;

const ControlsPanel = styled.div`
  padding: 16px;
  border-bottom: 1px solid #c5c5c5;
  background: #e0e5ec;
  box-shadow: inset 2px 2px 5px #bebebe, inset -2px -2px 5px #ffffff;
`;

const ControlsRow = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;

  &:last-child {
    margin-bottom: 0;
  }
`;

const ScanButton = styled.button<{ variant?: 'primary' | 'secondary' }>`
  padding: 8px 16px;
  background: #e0e5ec;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  color: #333;
  box-shadow: 2px 2px 5px #bebebe, -2px -2px 5px #ffffff;
  transition: all 0.2s ease;

  ${props => props.variant === 'primary' && `
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    box-shadow: 2px 2px 8px #bebebe, -2px -2px 8px #ffffff;
  `}

  &:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 3px 3px 8px #bebebe, -3px -3px 8px #ffffff;
  }

  &:active:not(:disabled) {
    transform: translateY(0);
    box-shadow: inset 2px 2px 5px #bebebe, inset -2px -2px 5px #ffffff;
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`;

const StatusIndicator = styled.div<{ status: string }>`
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  color: white;
  background: ${props => {
    switch (props.status) {
      case 'completed': return '#27ae60';
      case 'running': return '#f39c12';
      case 'failed': return '#e74c3c';
      default: return '#95a5a6';
    }
  }};
`;

const DiffContent = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 16px;
`;

const PlaceholderMessage = styled.div`
  text-align: center;
  color: #666;
  font-style: italic;
  padding: 40px 20px;
  background: #f8f9fa;
  border-radius: 8px;
  margin: 20px;
  box-shadow: inset 2px 2px 5px #bebebe, inset -2px -2px 5px #ffffff;
`;

const DiffSection = styled.div`
  margin-bottom: 16px;
  background: #f5f6f8;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 2px 2px 5px #bebebe, -2px -2px 5px #ffffff;
`;

const SectionHeader = styled.div`
  padding: 12px 16px;
  background: #e9ecef;
  border-bottom: 1px solid #dee2e6;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  user-select: none;

  &:hover {
    background: #dee2e6;
  }
`;

const SectionTitle = styled.span`
  font-weight: 600;
  color: #333;
`;

const SectionContent = styled.div`
  padding: 16px;
  background: #ffffff;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 13px;
  line-height: 1.4;
  white-space: pre-wrap;
  overflow-x: auto;
`;

const LoadingSpinner = styled.div`
  width: 24px;
  height: 24px;
  border: 2px solid #e0e5ec;
  border-top: 2px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;

export const DiffView: React.FC = () => {
  const [isScanning, setIsScanning] = useState(false);
  const [expandedSections, setExpandedSections] = useState<Set<number>>(new Set());
  
  const { startScan, getScanStatus, getScanResults } = useApiClient();
  const { 
    selectedPath, 
    selectedFiles, 
    currentScanId, 
    scanStatus,
    diffSections,
    setCurrentScanId,
    setScanStatus,
    setDiffSections 
  } = useAppStore();

  const handleStartScan = async () => {
    if (!selectedPath) {
      alert('Please select a project folder first');
      return;
    }

    if (selectedFiles.size === 0) {
      alert('Please select at least one file to scan');
      return;
    }

    setIsScanning(true);
    setScanStatus('starting');

    try {
      const response = await startScan(selectedPath, Array.from(selectedFiles));
      
      if (response.success && response.data?.scan_id) {
        setCurrentScanId(response.data.scan_id);
        setScanStatus('started');
        
        // Poll for scan completion
        pollScanStatus(response.data.scan_id);
      } else {
        setScanStatus('failed');
        alert(`Scan failed: ${response.error || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('Scan error:', error);
      setScanStatus('failed');
      alert('Failed to start scan');
    } finally {
      setIsScanning(false);
    }
  };

  const pollScanStatus = async (scanId: string) => {
    const poll = async () => {
      try {
        const statusResponse = await getScanStatus(scanId);
        
        if (statusResponse.success && statusResponse.data) {
          const status = statusResponse.data.status;
          setScanStatus(status);
          
          if (status === 'completed') {
            // Get scan results
            const resultsResponse = await getScanResults(scanId);
            
            if (resultsResponse.success && resultsResponse.data) {
              setDiffSections(resultsResponse.data.sections || []);
            }
          } else if (status === 'running') {
            // Continue polling
            setTimeout(poll, 1000);
          }
        }
      } catch (error) {
        console.error('Error polling scan status:', error);
        setScanStatus('failed');
      }
    };

    poll();
  };

  const toggleSection = (index: number) => {
    const newExpanded = new Set(expandedSections);
    if (newExpanded.has(index)) {
      newExpanded.delete(index);
    } else {
      newExpanded.add(index);
    }
    setExpandedSections(newExpanded);
  };

  const hasSelection = selectedFiles.size > 0;
  const canScan = selectedPath && hasSelection && !isScanning;

  return (
    <DiffViewContainer>
      <ControlsPanel>
        <ControlsRow>
          <ScanButton 
            variant="primary" 
            onClick={handleStartScan}
            disabled={!canScan}
          >
            {isScanning ? (
              <>
                <LoadingSpinner style={{ width: '16px', height: '16px', marginRight: '8px' }} />
                Scanning...
              </>
            ) : (
              '🔍 Start Scan'
            )}
          </ScanButton>
          
          {scanStatus && (
            <StatusIndicator status={scanStatus}>
              {scanStatus.toUpperCase()}
            </StatusIndicator>
          )}
          
          <div style={{ flex: 1 }} />
          
          <span style={{ fontSize: '14px', color: '#666' }}>
            {selectedFiles.size} file{selectedFiles.size !== 1 ? 's' : ''} selected
          </span>
        </ControlsRow>
      </ControlsPanel>

      <DiffContent>
        {!selectedPath && (
          <PlaceholderMessage>
            👋 Welcome to SNIP-DIFF!<br /><br />
            To get started:<br />
            1. Select a project folder using the "Choose Folder" button<br />
            2. Select files you want to analyze<br />
            3. Click "Start Scan" to generate diff results
          </PlaceholderMessage>
        )}

        {selectedPath && !hasSelection && (
          <PlaceholderMessage>
            📁 Project folder selected!<br /><br />
            Now select the files you want to analyze from the file tree on the left.
          </PlaceholderMessage>
        )}

        {hasSelection && diffSections.length === 0 && scanStatus !== 'completed' && (
          <PlaceholderMessage>
            ✅ Files selected!<br /><br />
            Click "Start Scan" to analyze changes and generate diff results.
          </PlaceholderMessage>
        )}

        {diffSections.map((section, index) => (
          <DiffSection key={index}>
            <SectionHeader onClick={() => toggleSection(index)}>
              <SectionTitle>
                {expandedSections.has(index) ? '📂' : '📁'} {section.title}
              </SectionTitle>
              <span style={{ fontSize: '12px', color: '#666' }}>
                {section.files.length} file{section.files.length !== 1 ? 's' : ''}
              </span>
            </SectionHeader>
            
            {expandedSections.has(index) && (
              <SectionContent>
                {section.files.map((file, fileIndex) => (
                  <div key={fileIndex}>
                    <strong>{file.change_type.toUpperCase()}: {file.path}</strong>
                    <br />
                    {file.content}
                    {fileIndex < section.files.length - 1 && <hr style={{ margin: '16px 0' }} />}
                  </div>
                ))}
              </SectionContent>
            )}
          </DiffSection>
        ))}
      </DiffContent>
    </DiffViewContainer>
  );
};
