/**
 * File Analysis Tool
 * Analyzes files and provides insights
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import { Tool } from './tool-registry';

export const fileAnalysisTool: Tool = {
  name: 'analyze_file',
  description: 'Analyze a file and return its content, size, and metadata',
  parameters: {
    type: 'object',
    properties: {
      filePath: {
        type: 'string',
        description: 'Absolute path to the file to analyze',
      },
    },
    required: ['filePath'],
  },
  execute: async (args: Record<string, unknown>) => {
    const filePath = args.filePath as string;

    try {
      const stats = await fs.stat(filePath);
      const content = await fs.readFile(filePath, 'utf-8');
      const ext = path.extname(filePath);

      return {
        path: filePath,
        size: stats.size,
        extension: ext,
        lines: content.split('\n').length,
        modified: stats.mtime,
        contentPreview: content.slice(0, 500),
      };
    } catch (error) {
      return {
        error: `Failed to analyze file: ${(error as Error).message}`,
      };
    }
  },
};
