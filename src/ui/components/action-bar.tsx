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
 * ActionBar Component for SNIP-DIFF
 * Bottom action bar with Scan, Prompts, and Copy All buttons
 */

import React from 'react';
import { useTheme } from '../theme';
import { Sparkles } from 'lucide-react';

// Inject gradient animation styles
const styleSheet = document.createElement('style');
styleSheet.textContent = `
  @keyframes aiGradient {
    0%, 100% {
      background-position: 0% 50%;
    }
    50% {
      background-position: 100% 50%;
    }
  }
  
  @keyframes aiPulse {
    0%, 100% {
      opacity: 1;
    }
    50% {
      opacity: 0.85;
    }
  }
`;
if (!document.head.querySelector('[data-ai-gradient-action]')) {
  styleSheet.setAttribute('data-ai-gradient-action', 'true');
  document.head.appendChild(styleSheet);
}

interface ActionBarProps {
  onSummarize: () => void;
  isDisabled?: boolean;
}

export const ActionBar: React.FC<ActionBarProps> = ({ 
  onSummarize,
  isDisabled = false
}) => {
  const { theme } = useTheme();

  const containerStyle: React.CSSProperties = {
    minHeight: '80px',
    backgroundColor: theme.colors.background.secondary,
    borderTop: `1px solid ${theme.colors.border.primary}`,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: '20px 24px',
    gap: '12px',
  };

  const actionButtonStyle: React.CSSProperties = {
    padding: '12px 24px',
    backgroundColor: 'transparent',
    border: `1px solid ${theme.colors.border.secondary}`,
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '15px',
    fontWeight: 500,
    color: theme.colors.text.primary,
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
  };

  const summarizeButtonStyle: React.CSSProperties = {
    padding: '12px 24px',
    backgroundColor: 'transparent',
    border: `1px solid rgba(59, 130, 246, ${isDisabled ? '0.15' : '0.3'})`,
    borderRadius: '6px',
    cursor: isDisabled ? 'not-allowed' : 'pointer',
    fontSize: '15px',
    fontWeight: 600,
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    background: 'linear-gradient(90deg, #06b6d4, #3b82f6, #8b5cf6, #3b82f6, #06b6d4)',
    backgroundSize: '200% 100%',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    backgroundClip: 'text',
    animation: isDisabled ? 'none' : 'aiGradient 3s ease infinite, aiPulse 2s ease-in-out infinite',
    boxShadow: isDisabled ? 'none' : '0 0 20px rgba(59, 130, 246, 0.15)',
    opacity: isDisabled ? 0.5 : 1,
    pointerEvents: isDisabled ? 'none' : 'auto',
  };

  return (
    <div style={containerStyle}>
      <button
        style={summarizeButtonStyle}
        onClick={onSummarize}
        disabled={isDisabled}
        title={isDisabled ? "Processing..." : "Summarize selected files from the tree, or open files if none selected"}
      >
        <Sparkles size={18} color="white" />
        <span>{isDisabled ? 'Processing' : 'Summarize'}</span>
      </button>
    </div>
  );
};
