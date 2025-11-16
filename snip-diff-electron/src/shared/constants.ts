/**
 * App constants for SNIP-DIFF
 */

export const APP_CONFIG = {
  name: 'SNIP-DIFF',
  version: '1.0.0',
  description: 'AI workflow tool for preparing code context',
};

export const WINDOW_CONFIG = {
  defaultWidth: 1400,
  defaultHeight: 900,
  minWidth: 1000,
  minHeight: 700,
};

export const FILE_EXTENSIONS = {
  code: ['.js', '.ts', '.jsx', '.tsx', '.py', '.java', '.cpp', '.c', '.cs', '.php'],
  web: ['.html', '.css', '.scss', '.sass', '.less'],
  config: ['.json', '.yaml', '.yml', '.toml', '.ini', '.conf'],
  docs: ['.md', '.txt', '.rst', '.adoc'],
  data: ['.csv', '.xml', '.sql'],
} as const;
