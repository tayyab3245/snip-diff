/**
 * React hook for WebSocket live diff updates
 * Provides real-time file change notifications with subscription management
 */

import { useEffect, useRef, useState, useCallback } from 'react';
import { FileDiff, ChangeType } from '../../shared/types';

export interface DiffEvent {
  type: 'file_diff' | 'ping' | 'subscription_confirmed' | 'subscription_updated' | 'error';
  seq?: number;
  path?: string;
  change_type?: ChangeType;
  timestamp: number;
  diff?: FileDiff;
  modes?: Record<string, any>;
  message?: string;
  paths?: string[];
}

export interface LiveDiffOptions {
  autoReconnect?: boolean;
  reconnectInterval?: number;
  maxReconnectAttempts?: number;
  heartbeatTimeout?: number;
}

export interface LiveDiffState {
  connected: boolean;
  connecting: boolean;
  error: string | null;
  lastEvent: DiffEvent | null;
  connectionId: string | null;
  reconnectAttempts: number;
}

const DEFAULT_OPTIONS: LiveDiffOptions = {
  autoReconnect: true,
  reconnectInterval: 3000,
  maxReconnectAttempts: 10,
  heartbeatTimeout: 45000 // 45 seconds (server sends ping every 30s)
};

export function useLiveDiff(
  clientId: string,
  options: LiveDiffOptions = DEFAULT_OPTIONS
) {
  const [state, setState] = useState<LiveDiffState>({
    connected: false,
    connecting: false,
    error: null,
    lastEvent: null,
    connectionId: null,
    reconnectAttempts: 0
  });

  const wsRef = useRef<WebSocket | null>(null);
  const subscribedPathsRef = useRef<Set<string>>(new Set());
  const eventListenersRef = useRef<Map<string, (event: DiffEvent) => void>>(new Map());
  const heartbeatTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const reconnectTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      return; // Already connected
    }

    setState(prev => ({ ...prev, connecting: true, error: null }));

    const wsUrl = `ws://localhost:8000/api/ws/diff?client_id=${encodeURIComponent(clientId)}`;
    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      console.log('WebSocket connected');
      wsRef.current = ws;
      setState(prev => ({
        ...prev,
        connected: true,
        connecting: false,
        error: null,
        connectionId: clientId,
        reconnectAttempts: 0
      }));

      // Re-subscribe to previous paths
      if (subscribedPathsRef.current.size > 0) {
        const message = {
          action: 'subscribe',
          paths: Array.from(subscribedPathsRef.current)
        };
        ws.send(JSON.stringify(message));
      }

      // Start heartbeat monitoring
      resetHeartbeatTimeout();
    };

    ws.onmessage = (event) => {
      try {
        const data: DiffEvent = JSON.parse(event.data);
        
        setState(prev => ({ ...prev, lastEvent: data }));

        // Handle different message types
        switch (data.type) {
          case 'ping':
            // Respond to server ping
            ws.send(JSON.stringify({ action: 'pong', timestamp: Date.now() }));
            resetHeartbeatTimeout();
            break;
            
          case 'file_diff':
            // Notify file diff listeners
            if (data.path) {
              const listener = eventListenersRef.current.get(data.path);
              if (listener) {
                listener(data);
              }
              // Also notify wildcard listeners
              const wildcardListener = eventListenersRef.current.get('*');
              if (wildcardListener) {
                wildcardListener(data);
              }
            }
            break;
            
          case 'subscription_confirmed':
          case 'subscription_updated':
            console.log('Subscription updated:', data.paths);
            break;
            
          case 'error':
            console.error('WebSocket error:', data.message);
            setState(prev => ({ ...prev, error: data.message || 'Unknown error' }));
            break;
        }
      } catch (err) {
        console.error('Failed to parse WebSocket message:', err);
      }
    };

    ws.onclose = (event) => {
      console.log('WebSocket closed:', event.code, event.reason);
      wsRef.current = null;
      clearHeartbeatTimeout();
      
      setState(prev => ({
        ...prev,
        connected: false,
        connecting: false,
        connectionId: null
      }));

      // Auto-reconnect if enabled and not intentionally closed
      if (options.autoReconnect && event.code !== 1000) {
        attemptReconnect();
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setState(prev => ({
        ...prev,
        error: 'Connection error',
        connecting: false
      }));
    };

  }, [clientId, options.autoReconnect]);

  const disconnect = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.close(1000, 'Client disconnect');
      wsRef.current = null;
    }
    clearHeartbeatTimeout();
    clearReconnectTimeout();
  }, []);

  const subscribe = useCallback((paths: string[]) => {
    // Add to local tracking
    paths.forEach(path => subscribedPathsRef.current.add(path));

    // Send subscription message if connected
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      const message = {
        action: 'subscribe',
        paths: paths
      };
      wsRef.current.send(JSON.stringify(message));
    }
  }, []);

  const unsubscribe = useCallback((paths: string[]) => {
    // Remove from local tracking
    paths.forEach(path => subscribedPathsRef.current.delete(path));

    // Send unsubscription message if connected
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      const message = {
        action: 'unsubscribe',
        paths: paths
      };
      wsRef.current.send(JSON.stringify(message));
    }
  }, []);

  const onDiffEvent = useCallback((path: string, listener: (event: DiffEvent) => void) => {
    eventListenersRef.current.set(path, listener);
    
    // Return cleanup function
    return () => {
      eventListenersRef.current.delete(path);
    };
  }, []);

  const resetHeartbeatTimeout = useCallback(() => {
    clearHeartbeatTimeout();
    
    if (options.heartbeatTimeout) {
      heartbeatTimeoutRef.current = setTimeout(() => {
        console.warn('Heartbeat timeout - connection may be stale');
        setState(prev => ({ ...prev, error: 'Heartbeat timeout' }));
        
        // Attempt reconnection
        if (options.autoReconnect) {
          disconnect();
          attemptReconnect();
        }
      }, options.heartbeatTimeout);
    }
  }, [options.heartbeatTimeout, options.autoReconnect, disconnect]);

  const clearHeartbeatTimeout = useCallback(() => {
    if (heartbeatTimeoutRef.current) {
      clearTimeout(heartbeatTimeoutRef.current);
      heartbeatTimeoutRef.current = null;
    }
  }, []);

  const clearReconnectTimeout = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }
  }, []);

  const attemptReconnect = useCallback(() => {
    setState(prev => {
      const newAttempts = prev.reconnectAttempts + 1;
      
      if (options.maxReconnectAttempts && newAttempts > options.maxReconnectAttempts) {
        return {
          ...prev,
          error: 'Max reconnection attempts reached'
        };
      }

      // Schedule reconnection
      clearReconnectTimeout();
      reconnectTimeoutRef.current = setTimeout(() => {
        console.log(`Reconnection attempt ${newAttempts}`);
        connect();
      }, options.reconnectInterval || 3000);

      return {
        ...prev,
        reconnectAttempts: newAttempts,
        error: `Reconnecting... (attempt ${newAttempts})`
      };
    });
  }, [connect, options.maxReconnectAttempts, options.reconnectInterval, clearReconnectTimeout]);

  // Connect on mount, disconnect on unmount
  useEffect(() => {
    connect();
    
    return () => {
      disconnect();
    };
  }, [connect, disconnect]);

  // Cleanup timeouts on unmount
  useEffect(() => {
    return () => {
      clearHeartbeatTimeout();
      clearReconnectTimeout();
    };
  }, [clearHeartbeatTimeout, clearReconnectTimeout]);

  return {
    ...state,
    connect,
    disconnect,
    subscribe,
    unsubscribe,
    onDiffEvent,
    isConnected: state.connected,
    subscribedPaths: Array.from(subscribedPathsRef.current)
  };
}

// Convenience hook for single file watching
export function useFileDiff(filePath: string, clientId: string = 'default') {
  const [fileDiff, setFileDiff] = useState<FileDiff | null>(null);
  const [lastChange, setLastChange] = useState<ChangeType | null>(null);
  
  const liveDiff = useLiveDiff(clientId);

  useEffect(() => {
    if (filePath) {
      // Subscribe to the file
      liveDiff.subscribe([filePath]);
      
      // Listen for changes
      const cleanup = liveDiff.onDiffEvent(filePath, (_event) => {
        if (_event.type === 'file_diff' && _event.diff) {
          setFileDiff(_event.diff);
          setLastChange(_event.change_type || null);
        }
      });

      return () => {
        cleanup();
        liveDiff.unsubscribe([filePath]);
      };
    }
  }, [filePath, liveDiff]);

  return {
    fileDiff,
    lastChange,
    connectionState: liveDiff,
    isWatching: liveDiff.subscribedPaths.includes(filePath)
  };
}
