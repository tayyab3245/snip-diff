/**
 * Token Badge Component - Shows compression stats on file tabs
 */

import React from 'react';
import { TokenTracker, FileTokenData } from '../../shared/token-tracker';

interface TokenBadgeProps {
  filePath: string;
  className?: string;
}

export const TokenBadge: React.FC<TokenBadgeProps> = ({ filePath, className = '' }) => {
  const [tokenData, setTokenData] = React.useState<FileTokenData | null>(null);

  React.useEffect(() => {
    const tracker = TokenTracker.getInstance();
    const data = tracker.getFileTokenData(filePath);
    setTokenData(data || null);

    // Set up polling to update when summary is completed
    const interval = setInterval(() => {
      const updatedData = tracker.getFileTokenData(filePath);
      if (updatedData?.summaryTokens !== undefined && updatedData !== tokenData) {
        setTokenData(updatedData);
        clearInterval(interval);
      }
    }, 500);

    return () => clearInterval(interval);
  }, [filePath, tokenData]);

  if (!tokenData) {
    return null;
  }

  const hasCompressionData = tokenData.summaryTokens !== undefined;
  
  if (!hasCompressionData) {
    // Show only original tokens in gray
    return (
      <div className={`token-badge original-only ${className}`}>
        <span style={{ 
          fontSize: '10px', 
          color: '#6b7280',
          fontWeight: 500
        }}>
          {tokenData.originalTokens}
        </span>
      </div>
    );
  }

  const compressionRatio = tokenData.compressionRatio || 0;

  return (
    <div className={`token-badge compressed ${className}`} style={{
      display: 'flex',
      alignItems: 'center',
      gap: '4px',
      fontSize: '10px',
      fontWeight: 500
    }}>
      {/* Original tokens in red */}
      <span style={{ 
        color: '#ef4444',
        textDecoration: 'line-through'
      }}>
        {tokenData.originalTokens}
      </span>
      
      {/* Arrow or divider */}
      <span style={{ color: '#6b7280' }}>→</span>
      
      {/* New tokens in green */}
      <span style={{ 
        color: '#10b981'
      }}>
        {tokenData.summaryTokens}
      </span>
      
      {/* Compression ratio badge */}
      <span style={{
        backgroundColor: TokenTracker.getInstance().getCompressionColor(compressionRatio),
        color: 'white',
        padding: '1px 4px',
        borderRadius: '3px',
        fontSize: '9px'
      }}>
        -{Math.round(compressionRatio * 100)}%
      </span>
    </div>
  );
};

interface TokenSummaryProps {
  filePaths: string[];
  className?: string;
}

export const TokenSummary: React.FC<TokenSummaryProps> = ({ filePaths, className = '' }) => {
  const [stats, setStats] = React.useState<any>(null);

  React.useEffect(() => {
    const tracker = TokenTracker.getInstance();
    const updateStats = () => {
      const summaryStats = tracker.getSummaryStats();
      setStats(summaryStats);
    };

    updateStats();
    
    // Update periodically while summaries are being generated
    const interval = setInterval(updateStats, 1000);
    
    // Clean up after 30 seconds (summaries should be done by then)
    setTimeout(() => clearInterval(interval), 30000);

    return () => clearInterval(interval);
  }, [filePaths]);

  if (!stats || stats.totalSummaryTokens === 0) {
    return null;
  }

  return (
    <div className={`token-summary ${className}`} style={{
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      padding: '4px 8px',
      backgroundColor: 'rgba(0, 0, 0, 0.05)',
      borderRadius: '6px',
      fontSize: '11px',
      color: '#6b7280'
    }}>
      <span>Total compression:</span>
      <span style={{ color: '#ef4444', textDecoration: 'line-through' }}>
        {stats.totalOriginalTokens}
      </span>
      <span>→</span>
      <span style={{ color: '#10b981' }}>
        {stats.totalSummaryTokens}
      </span>
      <span style={{
        backgroundColor: TokenTracker.getInstance().getCompressionColor(stats.overallCompressionRatio),
        color: 'white',
        padding: '2px 6px',
        borderRadius: '4px',
        fontWeight: 500
      }}>
        -{Math.round(stats.overallCompressionRatio * 100)}%
      </span>
    </div>
  );
};