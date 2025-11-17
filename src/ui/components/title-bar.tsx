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
 * TitleBar Component for SNIP-DIFF
 * Provides custom title bar with window controls for frameless window
 */

import React from 'react';
import { useTheme } from '../theme';
import { useWindowControls } from '../hooks/use-window-controls';

const AppTitle: React.FC = () => {
  const { theme } = useTheme();
  return (
    <span style={{
      fontSize: '13px',
      fontWeight: 600,
      letterSpacing: '0.5px',
      color: theme.colors.text.primary,
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    }}>
      SNIP-DIFF
    </span>
  );
};

export const TitleBar: React.FC = () => {
  const { theme } = useTheme();
  const windowControls = useWindowControls();

  const titleBarStyle: React.CSSProperties = {
    height: '32px',
    background: theme.colors.background.secondary,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '0 16px 0 8px',
    borderBottom: `1px solid ${theme.colors.border.secondary}`,
    userSelect: 'none',
    boxShadow: theme.colors.shadows.neumorphic.raised,
    // @ts-ignore - Electron specific property
    WebkitAppRegion: 'drag',
  };

  const titleSectionStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
  };

  const appTitleStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
  };

  const windowControlsStyle: React.CSSProperties = {
    display: 'flex',
    gap: '0',
    // @ts-ignore - Electron specific property
    WebkitAppRegion: 'no-drag',
  };

  const controlButtonBaseStyle: React.CSSProperties = {
    width: '46px',
    height: '32px',
    border: 'none',
    borderRadius: '0',
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '16px',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, sans-serif',
    background: 'transparent',
    color: theme.colors.text.secondary,
    transition: 'background 0.1s',
  };

  const minimizeButtonStyle: React.CSSProperties = {
    ...controlButtonBaseStyle,
  };

  const maximizeButtonStyle: React.CSSProperties = {
    ...controlButtonBaseStyle,
  };

  const closeButtonStyle: React.CSSProperties = {
    ...controlButtonBaseStyle,
  };

  return (
    <div style={titleBarStyle}>
      <div style={titleSectionStyle}>
        <div style={appTitleStyle}>
          <AppTitle />
        </div>
      </div>

      <div style={windowControlsStyle}>
        <button 
          style={minimizeButtonStyle} 
          onClick={windowControls.minimize} 
          title="Minimize"
          onMouseEnter={(e) => e.currentTarget.style.background = theme.colors.background.tertiary}
          onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
        >
          −
        </button>
        <button 
          style={maximizeButtonStyle} 
          onClick={windowControls.maximize} 
          title="Maximize"
          onMouseEnter={(e) => e.currentTarget.style.background = theme.colors.background.tertiary}
          onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
        >
          □
        </button>
        <button 
          style={closeButtonStyle} 
          onClick={windowControls.close} 
          title="Close"
          onMouseEnter={(e) => {
            e.currentTarget.style.background = '#e81123';
            e.currentTarget.style.color = '#ffffff';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = 'transparent';
            e.currentTarget.style.color = theme.colors.text.secondary;
          }}
        >
          ×
        </button>
      </div>
    </div>
  );
};
