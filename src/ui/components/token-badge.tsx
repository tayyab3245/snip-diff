/*
 * Copyright 2025 Tayyab
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * Token Badge Component - Shows compression stats on file tabs
 */

import React from 'react';
import { TokenTracker, FileTokenData } from '../../shared/token-tracker';
import { useTheme } from '../theme';

interface TokenBadgeProps {
  filePath: string;
  className?: string;
}

export const TokenBadge: React.FC<TokenBadgeProps> = ({ filePath, className = '' }) => {
  const { theme } = useTheme();
  const [tokenData, setTokenData] = React.useState<FileTokenData | null>(null);

  React.useEffect(() => {
    const tracker = TokenTracker.getInstance();
    const data = tracker.getFileTokenData(filePath);
    setTokenData(data || null);
  }, [filePath]);

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
          color: theme.colors.text.tertiary,
          fontWeight: 500
        }}>
          {tokenData.originalTokens}
        </span>
      </div>
    );
  }

  return (
    <div className={`token-badge compressed ${className}`} style={{
      display: 'flex',
      alignItems: 'center',
      gap: '3px',
      fontSize: '10px',
      fontWeight: 500
    }}>
      {/* Original tokens in error color */}
      <span style={{ 
        color: theme.colors.semantic.error
      }}>
        {tokenData.originalTokens}
      </span>
      
      {/* New tokens in success color */}
      <span style={{ 
        color: theme.colors.semantic.success
      }}>
        {tokenData.summaryTokens}
      </span>
    </div>
  );
};

interface TokenSummaryProps {
  filePaths: string[];
  className?: string;
}

export const TokenSummary: React.FC<TokenSummaryProps> = ({ filePaths, className = '' }) => {
  const { theme } = useTheme();
  const [stats, setStats] = React.useState<any>(null);

  React.useEffect(() => {
    const tracker = TokenTracker.getInstance();
    const summaryStats = tracker.getSummaryStats();
    setStats(summaryStats);
  }, [filePaths]);

  if (!stats || stats.totalSummaryTokens === 0) {
    return null;
  }

  const tokenDifference = stats.totalOriginalTokens - stats.totalSummaryTokens;

  return (
    <div className={`token-summary ${className}`} style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'flex-start',
      padding: '8px 12px',
      backgroundColor: theme.colors.background.secondary,
      border: `1px solid ${theme.colors.border.secondary}`,
      borderRadius: '6px',
      fontSize: '13px',
      fontWeight: 500,
      marginTop: '12px',
      marginBottom: '6px'
    }}>
      <span style={{ marginRight: '8px', color: theme.colors.text.primary }}>Token reduction:</span>
      <span style={{
        color: theme.colors.semantic.success,
        fontSize: '13px',
        fontWeight: 600
      }}>
        {tokenDifference > 0 ? `-${tokenDifference}` : tokenDifference}
      </span>
    </div>
  );
};