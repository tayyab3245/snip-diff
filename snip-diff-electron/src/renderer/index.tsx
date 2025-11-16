/**
 * Renderer main entry point for SNIP-DIFF
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import { App } from './app';

// Ensure the DOM is loaded
const rootElement = document.getElementById('root');

if (!rootElement) {
  throw new Error('Root element not found');
}

// Render the React app
const root = ReactDOM.createRoot(rootElement);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
