/**
 * TitleBar Component for SNIP-DIFF
 * Provides custom title bar with window controls for frameless window
 */

import React from 'react';
import styled from 'styled-components';

const TitleBarContainer = styled.div`
  height: 32px;
  background: #e0e5ec;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  border-bottom: 1px solid #c5c5c5;
  -webkit-app-region: drag;
  user-select: none;
  box-shadow: inset 2px 2px 5px #bebebe, inset -2px -2px 5px #ffffff;
`;

const TitleSection = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
`;

const AppIcon = styled.div`
  width: 20px;
  height: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 12px;
  box-shadow: 2px 2px 5px #bebebe, -2px -2px 5px #ffffff;
`;

const AppTitle = styled.span`
  font-size: 14px;
  font-weight: 500;
  color: #333;
`;

const WindowControls = styled.div`
  display: flex;
  gap: 8px;
  -webkit-app-region: no-drag;
`;

const ControlButton = styled.button`
  width: 20px;
  height: 20px;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  transition: all 0.2s ease;
  background: #e0e5ec;
  box-shadow: 2px 2px 5px #bebebe, -2px -2px 5px #ffffff;

  &:hover {
    transform: translateY(-1px);
    box-shadow: 3px 3px 8px #bebebe, -3px -3px 8px #ffffff;
  }

  &:active {
    transform: translateY(0);
    box-shadow: inset 2px 2px 5px #bebebe, inset -2px -2px 5px #ffffff;
  }

  &.minimize {
    color: #f39c12;
  }

  &.maximize {
    color: #27ae60;
  }

  &.close {
    color: #e74c3c;
  }
`;

export const TitleBar: React.FC = () => {
  const handleMinimize = async () => {
    try {
      await window.electronAPI.windowMinimize();
    } catch (error) {
      console.error('Failed to minimize window:', error);
    }
  };

  const handleMaximize = async () => {
    try {
      await window.electronAPI.windowMaximize();
    } catch (error) {
      console.error('Failed to maximize window:', error);
    }
  };

  const handleClose = async () => {
    try {
      await window.electronAPI.windowClose();
    } catch (error) {
      console.error('Failed to close window:', error);
    }
  };

  return (
    <TitleBarContainer>
      <TitleSection>
        <AppIcon>S</AppIcon>
        <AppTitle>SNIP-DIFF</AppTitle>
      </TitleSection>

      <WindowControls>
        <ControlButton className="minimize" onClick={handleMinimize} title="Minimize">
          −
        </ControlButton>
        <ControlButton className="maximize" onClick={handleMaximize} title="Maximize">
          □
        </ControlButton>
        <ControlButton className="close" onClick={handleClose} title="Close">
          ×
        </ControlButton>
      </WindowControls>
    </TitleBarContainer>
  );
};
