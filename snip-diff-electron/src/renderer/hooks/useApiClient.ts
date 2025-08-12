/**
 * API Client Hook for SNIP-DIFF
 * Provides unified interface for communicating with FastAPI backend
 */

import { useCallback } from 'react';

interface ApiRequestOptions {
  method: string;
  endpoint: string;
  data?: any;
  params?: Record<string, string>;
}

interface ApiResponse {
  success: boolean;
  status?: number;
  data?: any;
  error?: string;
}

export const useApiClient = () => {
  const apiRequest = useCallback(async (options: ApiRequestOptions): Promise<ApiResponse> => {
    try {
      if (!window.electronAPI) {
        throw new Error('Electron API not available');
      }

      const response = await window.electronAPI.apiRequest(options);
      return response;
    } catch (error) {
      console.error('API request failed:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }, []);

  // Convenience methods for common operations
  const getFileTree = useCallback(async (path: string) => {
    return apiRequest({
      method: 'GET',
      endpoint: '/api/files/tree',
      params: { path }
    });
  }, [apiRequest]);

  const startScan = useCallback(async (directory: string, includePaths?: string[]) => {
    return apiRequest({
      method: 'POST',
      endpoint: '/api/diff/scan',
      data: {
        directory,
        include_paths: includePaths,
        scan_mode: 'visual'
      }
    });
  }, [apiRequest]);

  const getScanStatus = useCallback(async (scanId: string) => {
    return apiRequest({
      method: 'GET',
      endpoint: `/api/diff/status/${scanId}`
    });
  }, [apiRequest]);

  const getScanResults = useCallback(async (scanId: string) => {
    return apiRequest({
      method: 'GET',
      endpoint: `/api/diff/results/${scanId}`
    });
  }, [apiRequest]);

  return {
    apiRequest,
    getFileTree,
    startScan,
    getScanStatus,
    getScanResults
  };
};
