/**
 * ChatPanel Component for SNIP-DIFF
 * AI Agent output panel - displays AI responses (no user input)
 */

import React from 'react';
import { useTheme } from '../theme';
import { AlertTriangle, Info } from 'lucide-react';
import { TokenSummary } from './token-badge';

// Minimal text renderer for AI responses
const renderMarkdown = (content: string): React.ReactElement => {
  const lines = content.split('\n');
  const elements: React.ReactElement[] = [];
  let currentIndex = 0;
  let inCodeBlock = false;
  let codeBlockLines: string[] = [];

  // Process inline formatting (bold and inline code)
  const processInlineFormatting = (text: string): React.ReactNode[] => {
    const parts: React.ReactNode[] = [];
    let remaining = text;
    let key = 0;

    while (remaining.length > 0) {
      // Check for inline code `...`
      const codeMatch = remaining.match(/^`([^`]+)`/);
      if (codeMatch) {
        parts.push(
          <code key={key++} style={{ 
            fontFamily: 'Monaco, Menlo, "Courier New", monospace',
            fontSize: '12px',
            backgroundColor: 'rgba(55, 65, 81, 0.5)',
            padding: '2px 6px',
            borderRadius: '3px'
          }}>
            {codeMatch[1]}
          </code>
        );
        remaining = remaining.slice(codeMatch[0].length);
        continue;
      }

      // Check for bold **...**
      const boldMatch = remaining.match(/^\*\*([^*]+)\*\*/);
      if (boldMatch) {
        parts.push(
          <strong key={key++} style={{ fontWeight: 600 }}>
            {boldMatch[1]}
          </strong>
        );
        remaining = remaining.slice(boldMatch[0].length);
        continue;
      }

      // Regular character
      const nextSpecial = remaining.search(/[`*]/);
      if (nextSpecial === -1) {
        parts.push(remaining);
        break;
      } else if (nextSpecial > 0) {
        parts.push(remaining.slice(0, nextSpecial));
        remaining = remaining.slice(nextSpecial);
      } else {
        // Special char that didn't match, include it
        parts.push(remaining[0]);
        remaining = remaining.slice(1);
      }
    }

    return parts;
  };

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    
    // Code block delimiter
    if (line.trim().startsWith('```')) {
      if (inCodeBlock) {
        // End code block
        elements.push(
          <pre key={currentIndex++} style={{ 
            margin: '8px 0',
            padding: '12px',
            backgroundColor: 'rgba(17, 24, 39, 0.6)',
            borderRadius: '6px',
            overflow: 'auto',
            border: '1px solid rgba(75, 85, 99, 0.3)'
          }}>
            <code style={{
              fontFamily: 'Monaco, Menlo, "Courier New", monospace',
              fontSize: '12px',
              lineHeight: '1.5',
              color: '#d1d5db'
            }}>
              {codeBlockLines.join('\n')}
            </code>
          </pre>
        );
        codeBlockLines = [];
        inCodeBlock = false;
      } else {
        // Start code block
        inCodeBlock = true;
      }
      continue;
    }

    // Inside code block
    if (inCodeBlock) {
      codeBlockLines.push(line);
      continue;
    }

    // List items
    if (line.startsWith('• ') || line.startsWith('- ')) {
      elements.push(
        <div key={currentIndex++} style={{ 
          margin: '2px 0',
          paddingLeft: '16px',
          fontSize: '13px',
          lineHeight: '1.6'
        }}>
          {processInlineFormatting(line)}
        </div>
      );
    }
    // Regular text
    else if (line.trim()) {
      elements.push(
        <div 
          key={currentIndex++} 
          style={{ 
            margin: '4px 0',
            lineHeight: '1.6',
            fontSize: '13px'
          }}
        >
          {processInlineFormatting(line)}
        </div>
      );
    }
    // Empty lines - paragraph spacing
    else {
      elements.push(
        <div key={currentIndex++} style={{ height: '8px' }} />
      );
    }
  }

  return <div>{elements}</div>;
};

interface Message {
  id: string;
  type: 'ai' | 'system' | 'error';
  content: string;
  timestamp: Date;
  isTyping?: boolean;
}

interface ChatPanelProps {
  messages: Message[];
  isLoading?: boolean;
  fileCount?: number;
  filePaths?: string[];
}

export const ChatPanel: React.FC<ChatPanelProps> = ({ messages, isLoading, fileCount = 0, filePaths = [] }) => {
  const { theme } = useTheme();
  const messagesEndRef = React.useRef<HTMLDivElement>(null);
  const [typingMessages, setTypingMessages] = React.useState<Record<string, string>>({});

  // Auto-scroll to bottom when new messages arrive
  React.useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, typingMessages]);

  // Fade mask effect for AI messages
  React.useEffect(() => {
    const aiMessages = messages.filter(m => m.type === 'ai' && m.isTyping);
    
    aiMessages.forEach(message => {
      if (!typingMessages[message.id]) {
        // Immediately show the mask
        setTypingMessages(prev => ({ ...prev, [message.id]: 'masked' }));
        
        // Start the fade animation after a brief delay
        setTimeout(() => {
          setTypingMessages(prev => ({ ...prev, [message.id]: 'animating' }));
        }, 100);
        
        // Remove mask after animation completes
        setTimeout(() => {
          setTypingMessages(prev => {
            const newState = { ...prev };
            delete newState[message.id];
            return newState;
          });
        }, 1600); // 100ms delay + 1500ms animation
      }
    });
  }, [messages]);

  const containerStyle: React.CSSProperties = {
    height: '100%',
    display: 'flex',
    flexDirection: 'column',
    backgroundColor: theme.colors.background.primary,
    overflow: 'hidden',
  };

  const messagesContainerStyle: React.CSSProperties = {
    flex: 1,
    overflowY: 'auto',
    padding: '20px',
    display: 'flex',
    flexDirection: 'column',
    gap: '16px',
    background: 'linear-gradient(135deg, rgba(17, 24, 39, 0.1) 0%, rgba(31, 41, 55, 0.05) 100%)',
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

  const messageStyle = (type: 'ai' | 'system' | 'error'): React.CSSProperties => ({
    padding: type === 'ai' ? '0' : '16px 20px',
    borderRadius: type === 'ai' ? '0' : '12px',
    backgroundColor: type === 'error'
      ? 'rgba(220, 38, 38, 0.1)'
      : type === 'system'
      ? 'rgba(56, 139, 253, 0.1)'
      : 'transparent',
    border: type === 'error'
      ? '1px solid rgba(220, 38, 38, 0.3)'
      : type === 'system'
      ? `1px solid ${theme.colors.border.secondary}`
      : 'none',
    fontSize: '13px',
    lineHeight: '1.6',
    color: type === 'error' ? '#fca5a5' : theme.colors.text.primary,
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  });

  const timestampStyle: React.CSSProperties = {
    fontSize: '11px',
    color: theme.colors.text.secondary,
    opacity: 0.7,
    marginTop: '6px',
  };

  const loadingDotsStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    padding: '16px 0',
  };



  return (
    <div style={containerStyle}>

      <div style={messagesContainerStyle} className="chat-messages">
        {messages.length === 0 && !isLoading ? (
          <div style={emptyStateStyle}>
            <div>Select files to analyze</div>
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <div key={message.id} style={messageStyle(message.type)}>
                {message.type !== 'ai' && (
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '8px' }}>
                    <div style={{
                      fontSize: '11px',
                      fontWeight: 600,
                      textTransform: 'uppercase',
                      letterSpacing: '0.5px',
                      color: message.type === 'error' ? '#f87171' : '#60a5fa',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '6px'
                    }}>
                      {message.type === 'error' && <AlertTriangle size={12} color="#f87171" />}
                      {message.type === 'system' && <Info size={12} color="#60a5fa" />}
                      {message.type === 'error' ? 'Error' : 'System'}
                    </div>
                  </div>
                )}
                <div style={{ 
                  color: message.type === 'ai' ? '#e5e7eb' : message.type === 'error' ? '#fca5a5' : '#d1d5db',
                  position: 'relative',
                  clipPath: message.type === 'ai' && typingMessages[message.id] 
                    ? (typingMessages[message.id] === 'masked' 
                        ? 'inset(0 0 100% 0)' 
                        : 'inset(0 0 0% 0)')
                    : 'none',
                  animation: message.type === 'ai' && typingMessages[message.id] === 'animating' 
                    ? 'revealText 1.5s ease-out forwards' 
                    : 'none'
                }}>
                  {message.type === 'ai' ? renderMarkdown(message.content) : message.content}
                </div>
                {message.type !== 'ai' && (
                  <div style={timestampStyle}>
                    {message.timestamp.toLocaleTimeString()}
                  </div>
                )}
              </div>
            ))}
            {isLoading && (
              <div style={loadingDotsStyle}>
                <div className="relative w-12 h-12">
                  <svg
                    width="48"
                    height="48"
                    viewBox="0 0 48 48"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                    style={{ filter: 'url(#gooey)' }}
                  >
                    <defs>
                      <filter id="gooey" colorInterpolationFilters="sRGB">
                        <feGaussianBlur in="SourceGraphic" stdDeviation="2.5" result="blur" />
                        <feColorMatrix
                          in="blur"
                          mode="matrix"
                          values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 22 -9"
                          result="goo"
                        />
                        <feComposite in="SourceGraphic" in2="goo" operator="atop" />
                      </filter>
                    </defs>
                    
                    <circle
                      cx="24"
                      cy="24"
                      r="6.5"
                      fill="#ffffff"
                      className="dot-white"
                    />
                    
                    <circle
                      cx="24"
                      cy="24"
                      r="6.5"
                      fill="#60a5fa"
                      className="dot-blue"
                    />
                  </svg>
                </div>
                <span style={{ 
                  fontSize: '13px', 
                  color: '#9ca3af'
                }}>
                  Analyzing {fileCount} file{fileCount !== 1 ? 's' : ''}...
                </span>
              </div>
            )}
            <div ref={messagesEndRef} />
            {filePaths.length > 0 && (
              <TokenSummary filePaths={filePaths} className="token-summary-display" />
            )}
          </>
        )}
      </div>

      <style>{`
        @keyframes revealText {
          0% {
            clip-path: inset(0 0 100% 0);
          }
          100% {
            clip-path: inset(0 0 0% 0);
          }
        }

        @keyframes dotWhite {
          0% {
            transform: translate(0, 0) scale(1, 1);
          }
          8% {
            transform: translate(-1px, 0) scale(0.95, 1.05);
          }
          15% {
            transform: translate(-6px, 0) scale(1, 1);
          }
          22% {
            transform: translate(-12px, 0.5px) scale(1, 1);
          }
          25% {
            transform: translate(-14px, 0) scale(1, 1);
          }
          50% {
            transform: translate(-14px, 0) scale(1, 1);
          }
          57% {
            transform: translate(-12px, -0.5px) scale(1, 1);
          }
          64% {
            transform: translate(-6px, 0) scale(1, 1);
          }
          72% {
            transform: translate(-1px, 0) scale(0.95, 1.05);
          }
          78% {
            transform: translate(0.5px, 0) scale(1.15, 0.92);
          }
          82% {
            transform: translate(0, 0) scale(0.98, 1.08);
          }
          86% {
            transform: translate(0, 0) scale(1.05, 0.98);
          }
          92% {
            transform: translate(0, 0) scale(0.99, 1.02);
          }
          100% {
            transform: translate(0, 0) scale(1, 1);
          }
        }

        @keyframes dotBlue {
          0% {
            transform: translate(0, 0) scale(1, 1);
          }
          8% {
            transform: translate(1px, 0) scale(0.95, 1.05);
          }
          15% {
            transform: translate(6px, 0) scale(1, 1);
          }
          22% {
            transform: translate(12px, -0.5px) scale(1, 1);
          }
          25% {
            transform: translate(14px, 0) scale(1, 1);
          }
          50% {
            transform: translate(14px, 0) scale(1, 1);
          }
          57% {
            transform: translate(12px, 0.5px) scale(1, 1);
          }
          64% {
            transform: translate(6px, 0) scale(1, 1);
          }
          72% {
            transform: translate(1px, 0) scale(0.95, 1.05);
          }
          78% {
            transform: translate(-0.5px, 0) scale(1.15, 0.92);
          }
          82% {
            transform: translate(0, 0) scale(0.98, 1.08);
          }
          86% {
            transform: translate(0, 0) scale(1.05, 0.98);
          }
          92% {
            transform: translate(0, 0) scale(0.99, 1.02);
          }
          100% {
            transform: translate(0, 0) scale(1, 1);
          }
        }

        .dot-white {
          animation: dotWhite 1.2s cubic-bezier(0.34, 1.56, 0.64, 1) infinite;
          transform-origin: center;
          will-change: transform;
          backface-visibility: hidden;
          transform: translateZ(0);
        }

        .dot-blue {
          animation: dotBlue 1.2s cubic-bezier(0.34, 1.56, 0.64, 1) infinite;
          transform-origin: center;
          will-change: transform;
          backface-visibility: hidden;
          transform: translateZ(0);
        }
        
        /* Custom scrollbar for chat */
        .chat-messages::-webkit-scrollbar {
          width: 6px;
        }
        .chat-messages::-webkit-scrollbar-track {
          background: rgba(0, 0, 0, 0.1);
          border-radius: 3px;
        }
        .chat-messages::-webkit-scrollbar-thumb {
          background: rgba(156, 163, 175, 0.5);
          border-radius: 3px;
        }
        .chat-messages::-webkit-scrollbar-thumb:hover {
          background: rgba(156, 163, 175, 0.7);
        }
      `}</style>
    </div>
  );
};
