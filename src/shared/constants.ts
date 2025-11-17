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
