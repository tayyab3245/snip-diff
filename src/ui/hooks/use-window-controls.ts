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
