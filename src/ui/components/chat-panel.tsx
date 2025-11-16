/**
 * ChatPanel Component for SNIP-DIFF
 * AI Agent output panel - displays AI responses (no user input)
 */

import React from 'react';
import { useTheme } from '../theme';

interface Message {
  id: string;
  type: 'ai' | 'system';
  content: string;
  timestamp: Date;
}

interface ChatPanelProps {
  messages: Message[];
  isLoading?: boolean;
}

export const ChatPanel: React.FC<ChatPanelProps> = ({ messages, isLoading }) => {
  const { theme } = useTheme();
  const messagesEndRef = React.useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  React.useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const containerStyle: React.CSSProperties = {
    height: '100%',
    display: 'flex',
    flexDirection: 'column',
    backgroundColor: theme.colors.background.primary,
    overflow: 'hidden',
  };

  const headerStyle: React.CSSProperties = {
    padding: '12px 16px',
    backgroundColor: theme.colors.background.secondary,
    borderBottom: `1px solid ${theme.colors.border.primary}`,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    fontSize: '13px',
    fontWeight: 600,
    color: theme.colors.text.primary,
  };

  const messagesContainerStyle: React.CSSProperties = {
    flex: 1,
    overflowY: 'auto',
    padding: '16px',
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
  };

  const emptyStateStyle: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100%',
    color: theme.colors.text.secondary,
    fontSize: '13px',
    opacity: 0.7,
  };

  const messageStyle = (type: 'ai' | 'system'): React.CSSProperties => ({
    padding: '12px 16px',
    borderRadius: '8px',
    backgroundColor: type === 'ai' 
      ? theme.colors.background.secondary 
      : 'rgba(56, 139, 253, 0.1)',
    border: `1px solid ${theme.colors.border.secondary}`,
    fontSize: '13px',
    lineHeight: '1.6',
    color: theme.colors.text.primary,
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  });

  const timestampStyle: React.CSSProperties = {
    fontSize: '11px',
    color: theme.colors.text.secondary,
    opacity: 0.7,
    marginTop: '6px',
  };

  const loadingDotsStyle: React.CSSProperties = {
    display: 'inline-flex',
    gap: '4px',
    padding: '12px 16px',
  };

  const dotStyle: React.CSSProperties = {
    width: '6px',
    height: '6px',
    borderRadius: '50%',
    backgroundColor: theme.colors.text.secondary,
    animation: 'pulse 1.4s ease-in-out infinite',
  };

  return (
    <div style={containerStyle}>
      <div style={headerStyle}>
        <span>AI Agent</span>
        {isLoading && (
          <span style={{ fontSize: '11px', color: theme.colors.text.secondary }}>
            Thinking...
          </span>
        )}
      </div>

      <div style={messagesContainerStyle}>
        {messages.length === 0 && !isLoading ? (
          <div style={emptyStateStyle}>
            <div style={{ fontSize: '24px', marginBottom: '8px' }}>🤖</div>
            <div>Select files in the tree and click "Smart Summarize" to get AI insights</div>
            <div style={{ fontSize: '11px', marginTop: '8px', opacity: 0.7 }}>
              Tip: Click files in the tree to select them for AI analysis
            </div>
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <div key={message.id} style={messageStyle(message.type)}>
                <div>{message.content}</div>
                <div style={timestampStyle}>
                  {message.timestamp.toLocaleTimeString()}
                </div>
              </div>
            ))}
            {isLoading && (
              <div style={loadingDotsStyle}>
                <div style={dotStyle} />
                <div style={{ ...dotStyle, animationDelay: '0.2s' }} />
                <div style={{ ...dotStyle, animationDelay: '0.4s' }} />
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      <style>{`
        @keyframes pulse {
          0%, 60%, 100% {
            opacity: 0.3;
            transform: scale(0.8);
          }
          30% {
            opacity: 1;
            transform: scale(1);
          }
        }
      `}</style>
    </div>
  );
};
