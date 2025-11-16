/**
 * Window Controls Hook
 * Handles window management operations (minimize, maximize, close)
 */

import { useCallback } from 'react';

export const useWindowControls = () => {
  const minimize = useCallback(async () => {
    try {
      await window.electronAPI.windowMinimize();
    } catch (error) {
      console.error('Failed to minimize window:', error);
    }
  }, []);

  const maximize = useCallback(async () => {
    try {
      await window.electronAPI.windowMaximize();
    } catch (error) {
      console.error('Failed to maximize window:', error);
    }
  }, []);

  const close = useCallback(async () => {
    try {
      await window.electronAPI.windowClose();
    } catch (error) {
      console.error('Failed to close window:', error);
    }
  }, []);

  return {
    minimize,
    maximize,
    close
  };
};
