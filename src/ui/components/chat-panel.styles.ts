/**
 * Chat Panel Style Utilities
 * Complete styles for all chat panel elements - NO inline styles should remain in component
 */

import React from 'react';
import { type DarkTheme } from '../theme/dark-theme';

export const createChatPanelStyles = (theme: DarkTheme) => ({
  container: {
    height: '100%',
    display: 'flex',
    flexDirection: 'column' as const,
    backgroundColor: theme.components.chatPanel.background,
    overflow: 'hidden' as const,
  },

  messagesContainer: {
    flex: 1,
    overflowY: 'auto' as const,
    padding: '20px',
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '16px',
    background: theme.components.chatPanel.messagesBackground,
  },

  emptyState: {
    display: 'flex',
    flexDirection: 'column' as const,
    alignItems: 'center',
    justifyContent: 'center',
    height: '100%',
    color: theme.components.chatPanel.emptyStateText,
    fontSize: '13px',
    opacity: 0.7,
  },

  getMessage: (type: 'ai' | 'system' | 'error') => ({
    padding: type === 'ai' ? '0' : '16px 20px',
    borderRadius: type === 'ai' ? '0' : '12px',
    backgroundColor: type === 'error'
      ? theme.components.chatPanel.errorMessage.background
      : type === 'system'
      ? theme.components.chatPanel.systemMessage.background
      : theme.components.chatPanel.aiMessage.background,
    border: type === 'error'
      ? theme.components.chatPanel.errorMessage.border
      : type === 'system'
      ? theme.components.chatPanel.systemMessage.border
      : theme.components.chatPanel.aiMessage.border,
    fontSize: '13px',
    lineHeight: '1.6',
    color: type === 'error' 
      ? theme.components.chatPanel.errorMessage.text
      : type === 'system'
      ? theme.components.chatPanel.systemMessage.text
      : theme.components.chatPanel.aiMessage.text,
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  }),

  // Non-AI message header styles
  messageHeader: {
    display: 'flex',
    justifyContent: 'space-between' as const,
    alignItems: 'flex-start' as const,
    marginBottom: '8px',
  },

  statusHeader: {
    fontSize: '11px',
    fontWeight: 600 as const,
    textTransform: 'uppercase' as const,
    letterSpacing: '0.5px',
    display: 'flex',
    alignItems: 'center',
    gap: '6px',
  },

  // AI message analyzing container
  analyzingContainer: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    marginBottom: '16px',
    justifyContent: 'flex-start' as const,
    padding: '0',
  },

  // Loading dots animation container
  loadingDots: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    padding: '16px 0',
    lineHeight: '1',
  },

  // Animation SVG container
  animationSvgContainer: {
    position: 'relative' as const,
    width: '32px',
    height: '32px',
  },

  // SVG gooey filter styles
  animationSvg: {
    filter: 'url(#gooey)',
  },

  // Status text (Summarizing/Summarized)
  statusText: {
    fontSize: '13px',
    color: theme.components.chatPanel.statusText,
    fontWeight: 500 as const,
  },

  // Loading text (during initial load)
  loadingText: {
    fontSize: '13px',
    color: theme.components.chatPanel.statusText,
  },

  // Message content with animation support
  getMessageContent: (type: 'ai' | 'system' | 'error', isAnimating: boolean, isMasked: boolean) => ({
    color: type === 'ai' 
      ? theme.components.chatPanel.aiMessage.text
      : type === 'error' 
      ? theme.components.chatPanel.errorMessage.text 
      : theme.components.chatPanel.systemMessage.text,
    position: 'relative' as const,
    // Hide content completely during masked state, show with animation when animating
    opacity: type === 'ai' ? (isMasked ? 0 : 1) : 1,
    animation: type === 'ai' && isAnimating 
      ? 'revealText 1.5s ease-out forwards' 
      : 'none',
    // Ensure no transition during mask application for instant hiding
    transition: type === 'ai' && isMasked ? 'none' : 'opacity 0.2s ease-out',
  }),

  // Timestamp styles
  timestamp: {
    fontSize: '11px',
    color: theme.text.secondary,
    opacity: 0.7,
    marginTop: '6px',
  },

  // Markdown rendering styles
  markdown: {
    inlineCode: {
      fontFamily: 'Monaco, Menlo, "Courier New", monospace',
      fontSize: '12px',
      backgroundColor: 'rgba(55, 65, 81, 0.5)',
      padding: '2px 6px',
      borderRadius: '3px',
    } as React.CSSProperties,

    bold: {
      fontWeight: 600,
    } as React.CSSProperties,

    codeBlock: {
      margin: '8px 0',
      padding: '12px',
      backgroundColor: 'rgba(17, 24, 39, 0.6)',
      borderRadius: '6px',
      overflow: 'auto' as const,
      border: '1px solid rgba(75, 85, 99, 0.3)',
    } as React.CSSProperties,

    codeBlockText: {
      fontFamily: 'Monaco, Menlo, "Courier New", monospace',
      fontSize: '12px',
      lineHeight: '1.5',
      color: '#d1d5db'
    } as React.CSSProperties,

    listItem: {
      margin: '2px 0',
      paddingLeft: '16px',
      fontSize: '13px',
      lineHeight: '1.6',
    } as React.CSSProperties,

    paragraph: {
      margin: '4px 0',
      lineHeight: '1.6',
      fontSize: '13px',
    } as React.CSSProperties,

    emptyLine: {
      height: '8px',
    } as React.CSSProperties,
  },
});