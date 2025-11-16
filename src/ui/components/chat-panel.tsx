/**
 * ChatPanel Component for SNIP-DIFF
 * AI Agent output panel - displays AI responses (no user input)
 */

import React from 'react';
import { useTheme } from '../theme';
import { AlertTriangle, Info } from 'lucide-react';
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
}

export const ChatPanel: React.FC<ChatPanelProps> = ({ messages, isLoading, fileCount = 0, filePaths = [] }) => {
  const { theme } = useTheme();
  const styles = createChatPanelStyles(theme.colors);
  const messagesEndRef = React.useRef<HTMLDivElement>(null);
  const [typingMessages, setTypingMessages] = React.useState<Record<string, string>>({});

  // Auto-scroll to bottom when new messages arrive
  React.useEffect(() => {
    if (messagesEndRef.current) {
      // Use auto behavior for instant, non-erratic scroll
      messagesEndRef.current.scrollIntoView({ behavior: 'auto', block: 'end' });
    }
  }, [messages, typingMessages]);

  // Fade mask effect for AI messages
  React.useEffect(() => {
    const aiMessages = messages.filter(m => m.type === 'ai' && m.isTyping);
    
    aiMessages.forEach(message => {
      if (!typingMessages[message.id]) {
        // Immediately show the mask (content hidden)
        setTypingMessages(prev => ({ ...prev, [message.id]: 'masked' }));
        
        // Start the fade animation after a delay
        setTimeout(() => {
          setTypingMessages(prev => ({ ...prev, [message.id]: 'animating' }));
        }, 500); // Increased delay to ensure loading animation is visible first
        
        // Remove mask after animation completes
        setTimeout(() => {
          setTypingMessages(prev => {
            const newState = { ...prev };
            delete newState[message.id];
            return newState;
          });
        }, 2000); // 500ms delay + 1500ms animation
      }
    });
  }, [messages]);

  return (
    <div style={styles.container}>

      <div style={styles.messagesContainer} className="chat-messages">
        {messages.length === 0 && !isLoading ? (
          <div style={styles.emptyState}>
            <div>Select files to analyze</div>
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <div key={message.id} style={styles.getMessage(message.type)}>
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
                  <div style={styles.analyzingContainer}>
                    {typingMessages[message.id] && (
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
                      {typingMessages[message.id] ? 'Summarizing' : 'Summarized'} {fileCount} file{fileCount !== 1 ? 's' : ''}
                    </span>
                  </div>
                )}
                
                <div style={styles.getMessageContent(
                  message.type,
                  typingMessages[message.id] === 'animating',
                  typingMessages[message.id] === 'masked'
                )}>
                  {/* Only show content when not masked or when animation has started */}
                  {!typingMessages[message.id] || typingMessages[message.id] === 'animating' ? (
                    message.type === 'ai' ? renderMarkdown(message.content, styles) : message.content
                  ) : null}
                </div>
                {message.type !== 'ai' && (
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
                  Summarizing {fileCount} file{fileCount !== 1 ? 's' : ''}...
                </span>
              </div>
            )}
            <div ref={messagesEndRef} />
            {filePaths.length > 0 && !Object.keys(typingMessages).some(id => typingMessages[id]) && (
              <TokenSummary filePaths={filePaths} className="token-summary-display" />
            )}
          </>
        )}
      </div>

    </div>
  );
};
