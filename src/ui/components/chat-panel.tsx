/**
 * ChatPanel Component for SNIP-DIFF
 * AI Agent output panel - displays AI responses (no user input)
 */

import React from 'react';
import { useTheme } from '../theme';
import { AlertTriangle, Info, Copy, Check } from 'lucide-react';
import { TokenSummary } from './token-badge';
import { createChatPanelStyles } from './chat-panel.styles';
import './chat-animations.css';

// Minimal text renderer for AI responses
const renderMarkdown = (content: string, styles: ReturnType<typeof createChatPanelStyles>): React.ReactElement => {
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
          <code key={key++} style={styles.markdown.inlineCode}>
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
          <strong key={key++} style={styles.markdown.bold}>
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
          <pre key={currentIndex++} style={styles.markdown.codeBlock}>
            <code style={styles.markdown.codeBlockText}>
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
        <div key={currentIndex++} style={styles.markdown.listItem}>
          {processInlineFormatting(line)}
        </div>
      );
    }
    // Regular text
    else if (line.trim()) {
      elements.push(
        <div key={currentIndex++} style={styles.markdown.paragraph}>
          {processInlineFormatting(line)}
        </div>
      );
    }
    // Empty lines - paragraph spacing
    else {
      elements.push(
        <div key={currentIndex++} style={styles.markdown.emptyLine} />
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
  onCopyAll?: () => void;
}

export const ChatPanel: React.FC<ChatPanelProps> = ({ messages, isLoading, fileCount = 0, filePaths = [] }) => {
  const { theme } = useTheme();
  const styles = createChatPanelStyles(theme.colors);
  const messagesEndRef = React.useRef<HTMLDivElement>(null);
  const [typingMessages, setTypingMessages] = React.useState<Record<string, string>>({});
  const [copiedMessageId, setCopiedMessageId] = React.useState<string | null>(null);

  const handleCopyMessage = async (messageId: string, content: string) => {
    try {
      // Copy the entire AI message content
      await navigator.clipboard.writeText(content);
      setCopiedMessageId(messageId);
      setTimeout(() => setCopiedMessageId(null), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  // Auto-scroll to bottom when new messages arrive
  React.useEffect(() => {
    if (messagesEndRef.current) {
      // Use auto behavior for instant, non-erratic scroll
      messagesEndRef.current.scrollIntoView({ behavior: 'auto', block: 'end' });
    }
  }, [messages, typingMessages]);

  // Fade mask effect for AI messages - use useLayoutEffect to run synchronously before paint
  React.useLayoutEffect(() => {
    const aiMessages = messages.filter(m => m.type === 'ai' && m.isTyping);
    
    aiMessages.forEach(message => {
      setTypingMessages(prev => {
        // Only set to masked if not already in state
        if (!prev[message.id]) {
          return { ...prev, [message.id]: 'masked' };
        }
        return prev;
      });
    });
  }, [messages]);

  // Handle animation transitions after initial mask
  React.useEffect(() => {
    const aiMessages = messages.filter(m => m.type === 'ai' && m.isTyping);
    
    const timers: ReturnType<typeof setTimeout>[] = [];
    
    aiMessages.forEach(message => {
      if (typingMessages[message.id] === 'masked') {
        // Start the fade animation after a delay
        const animationTimer = setTimeout(() => {
          setTypingMessages(prev => {
            if (prev[message.id] === 'masked') {
              return { ...prev, [message.id]: 'animating' };
            }
            return prev;
          });
        }, 800);
        
        // Remove mask after animation completes
        const removeTimer = setTimeout(() => {
          setTypingMessages(prev => {
            const newState = { ...prev };
            delete newState[message.id];
            return newState;
          });
        }, 2300);
        
        timers.push(animationTimer, removeTimer);
      }
    });
    
    return () => {
      timers.forEach(timer => clearTimeout(timer));
    };
  }, [messages, typingMessages]);

  return (
    <div style={styles.container}>
      {/* Floating Copy Button for Latest AI Message */}
      {messages.length > 0 && messages[messages.length - 1]?.type === 'ai' && (
        <button
          onClick={() => handleCopyMessage(messages[messages.length - 1].id, messages[messages.length - 1].content)}
          style={{
            position: 'absolute',
            top: '16px',
            right: '16px',
            zIndex: 100,
            padding: '8px 14px',
            backgroundColor: theme.colors.background.secondary,
            border: 'none',
            borderRadius: '6px',
            cursor: 'pointer',
            fontSize: '13px',
            fontWeight: 500,
            color: theme.colors.text.primary,
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            transition: 'all 0.15s',
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.3)',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = theme.colors.background.tertiary;
            e.currentTarget.style.transform = 'translateY(-1px)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = theme.colors.background.secondary;
            e.currentTarget.style.transform = 'translateY(0)';
          }}
          title="Copy AI response"
        >
          {copiedMessageId === messages[messages.length - 1].id ? (
            <Check size={15} color="#10b981" style={{ transition: 'all 0.3s ease' }} />
          ) : (
            <Copy size={15} style={{ transition: 'all 0.3s ease' }} />
          )}
          <span>{copiedMessageId === messages[messages.length - 1].id ? 'Copied!' : 'Copy'}</span>
        </button>
      )}

      <div style={styles.messagesContainer} className="chat-messages">
        {messages.length === 0 && !isLoading ? (
          <div style={styles.emptyState}>
            <div>Select files to analyze</div>
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <div key={message.id} style={{
                ...styles.getMessage(message.type),
                paddingTop: message.type === 'ai' ? '16px' : undefined,
              }}>
                {message.type !== 'ai' && (
                  <div style={styles.messageHeader}>
                    <div style={{
                      ...styles.statusHeader,
                      color: message.type === 'error' ? '#f87171' : '#60a5fa'
                    }}>
                      {message.type === 'error' && <AlertTriangle size={12} color="#f87171" />}
                      {message.type === 'system' && <Info size={12} color="#60a5fa" />}
                      {message.type === 'error' ? 'Error' : 'System'}
                    </div>
                  </div>
                )}
                
                {/* Show analyzing status for AI messages */}
                {message.type === 'ai' && (
                  <div style={{ display: 'flex', justifyContent: 'flex-start', alignItems: 'center', marginBottom: '16px', paddingLeft: '20px', paddingRight: '20px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    {typingMessages[message.id] === 'masked' && (
                      <div style={styles.animationSvgContainer}>
                        <svg
                          width="32"
                          height="32"
                          viewBox="0 0 32 32"
                          fill="none"
                          xmlns="http://www.w3.org/2000/svg"
                          style={styles.animationSvg}
                        >
                          <circle
                            cx="16"
                            cy="16"
                            r="4"
                            fill="#ffffff"
                            className="dot-white"
                          />
                          
                          <circle
                            cx="16"
                            cy="16"
                            r="4"
                            fill="#ffffff"
                            className="dot-blue"
                          />
                        </svg>
                        
                        {/* SVG Filter Definition */}
                        <svg className="chat-svg-filters">
                          <defs>
                            <filter id="gooey" colorInterpolationFilters="sRGB">
                              <feGaussianBlur in="SourceGraphic" stdDeviation="1.5" result="blur" />
                              <feColorMatrix
                                in="blur"
                                mode="matrix"
                                values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 22 -9"
                                result="goo"
                              />
                              <feComposite in="SourceGraphic" in2="goo" operator="atop" />
                            </filter>
                          </defs>
                        </svg>
                      </div>
                    )}
                    <span style={styles.statusText}>
                      {typingMessages[message.id] === 'masked' ? 'Summarizing' : 'Summarized'} {fileCount} file{fileCount !== 1 ? 's' : ''}
                    </span>
                    </div>
                  </div>
                )}
                
                {/* Only render content container when ready */}
                {(!typingMessages[message.id] || typingMessages[message.id] === 'animating') && (
                  <div style={styles.getMessageContent(
                    message.type,
                    typingMessages[message.id] === 'animating',
                    false
                  )}>
                    {message.type === 'ai' ? renderMarkdown(message.content, styles) : message.content}
                  </div>
                )}
                {message.type !== 'ai' && message.timestamp && (
                  <div style={styles.timestamp}>
                    {message.timestamp.toLocaleTimeString()}
                  </div>
                )}  
              </div>
            ))}
            {isLoading && messages.length === 0 && (
              <div style={styles.loadingDots}>
                <div style={styles.animationSvgContainer}>
                  <svg
                    width="32"
                    height="32"
                    viewBox="0 0 32 32"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                    style={styles.animationSvg}
                  >
                    <circle
                      cx="16"
                      cy="16"
                      r="4"
                      fill="#ffffff"
                      className="dot-white"
                    />
                    
                    <circle
                      cx="16"
                      cy="16"
                      r="4"
                      fill="#ffffff"
                      className="dot-blue"
                    />
                  </svg>
                  
                  {/* SVG Filter Definition */}
                  <svg className="chat-svg-filters">
                    <defs>
                      <filter id="gooey" colorInterpolationFilters="sRGB">
                        <feGaussianBlur in="SourceGraphic" stdDeviation="1.5" result="blur" />
                        <feColorMatrix
                          in="blur"
                          mode="matrix"
                          values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 22 -9"
                          result="goo"
                        />
                        <feComposite in="SourceGraphic" in2="goo" operator="atop" />
                      </filter>
                    </defs>
                  </svg>
                </div>
                <span style={styles.loadingText}>
                  Summarizing {fileCount} file{fileCount !== 1 ? 's' : ''}
                </span>
              </div>
            )}
            <div ref={messagesEndRef} />
            {filePaths.length > 0 && !Object.keys(typingMessages).some(id => typingMessages[id] === 'masked') && (
              <TokenSummary filePaths={filePaths} className="token-summary-display" />
            )}
          </>
        )}
      </div>

    </div>
  );
};
