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

  const cancelScan = useCallback(async (scanId: string) => {
    return apiRequest({
      method: 'DELETE',
      endpoint: `/api/diff/scan/${scanId}`
    });
  }, [apiRequest]);

  const listScans = useCallback(async (limit: number = 50) => {
    return apiRequest({
      method: 'GET',
      endpoint: `/api/diff/scans`,
      params: { limit: String(limit) }
    });
  }, [apiRequest]);

  const getFileContent = useCallback(async (basePath: string, filePath: string) => {
    return apiRequest({
      method: 'GET',
      endpoint: '/api/files/content',
      params: { 
        base_path: basePath,
        path: filePath 
      }
    });
  }, [apiRequest]);

  const startLiveWatch = useCallback(async (directory: string, includePaths: string[]) => {
    return apiRequest({
      method: 'POST',
      endpoint: '/api/live/start',
      data: {
        directory,
        include_paths: includePaths
      }
    });
  }, [apiRequest]);

  const stopLiveWatch = useCallback(async () => {
    return apiRequest({
      method: 'POST',
      endpoint: '/api/live/stop'
    });
  }, [apiRequest]);

  const getLiveStatus = useCallback(async () => {
    return apiRequest({
      method: 'GET',
      endpoint: '/api/live/status'
    });
  }, [apiRequest]);

  const getLiveFiles = useCallback(async () => {
    return apiRequest({
      method: 'GET',
      endpoint: '/api/live/files'
    });
  }, [apiRequest]);

  const getLiveAggregate = useCallback(async (format: 'unified' | 'sections' = 'sections') => {
    return apiRequest({
      method: 'GET',
      endpoint: '/api/live/aggregate',
      params: { format }
    });
  }, [apiRequest]);

  return {
    apiRequest,
    getFileTree,
    startScan,
    getScanStatus,
    getScanResults,
    cancelScan,
    listScans,
    getFileContent,
    startLiveWatch,
    stopLiveWatch,
    getLiveStatus,
    getLiveFiles,
    getLiveAggregate
  };
};
