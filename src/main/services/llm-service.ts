/**
 * LLM Service for SNIP-DIFF
 * Uses Google Gemini for file/diff summarization
 */

import { GoogleGenerativeAI } from '@google/generative-ai';
import * as dotenv from 'dotenv';
import * as path from 'path';

// Load environment variables
dotenv.config({ path: path.join(__dirname, '../../.env') });

export interface SummarizeRequest {
  content: string;
  type: 'file' | 'diff';
  maxTokens?: number;
}

export interface SummarizeResult {
  success: boolean;
  summary?: string;
  tokensUsed?: number;
  error?: string;
}

export class LLMService {
  private genAI: GoogleGenerativeAI | null = null;
  private model: any = null;

  constructor() {
    const apiKey = process.env.GEMINI_API_KEY;
    
    if (apiKey) {
      try {
        this.genAI = new GoogleGenerativeAI(apiKey);
        this.model = this.genAI.getGenerativeModel({ model: 'gemini-1.5-flash' });
        console.log('[LLM] Gemini initialized successfully');
      } catch (error) {
        console.error('[LLM] Failed to initialize Gemini:', error);
      }
    } else {
      console.warn('[LLM] GEMINI_API_KEY not found in environment');
    }
  }

  isAvailable(): boolean {
    return this.model !== null;
  }

  async summarizeFile(content: string, filePath: string): Promise<SummarizeResult> {
    if (!this.isAvailable()) {
      return {
        success: false,
        error: 'LLM service not available. Please set GEMINI_API_KEY in .env file'
      };
    }

    try {
      const prompt = `You are a code summarization expert. Summarize the following code file concisely for LLM consumption (reduce tokens while preserving key information).

File: ${filePath}

Code:
\`\`\`
${content}
\`\`\`

Provide a concise summary that captures:
1. Main purpose/functionality
2. Key functions/classes/components
3. Important dependencies
4. Notable patterns or architecture

Keep it under 500 words.`;

      const result = await this.model.generateContent(prompt);
      const response = await result.response;
      const summary = response.text();

      return {
        success: true,
        summary,
        tokensUsed: response.usageMetadata?.totalTokenCount
      };
    } catch (error: any) {
      console.error('[LLM] Summarization error:', error);
      return {
        success: false,
        error: error.message || 'Failed to summarize file'
      };
    }
  }

  async summarizeDiff(diffContent: string, files: string[]): Promise<SummarizeResult> {
    if (!this.isAvailable()) {
      return {
        success: false,
        error: 'LLM service not available. Please set GEMINI_API_KEY in .env file'
      };
    }

    try {
      const prompt = `You are a git diff summarization expert. Analyze and summarize the following git diff concisely for LLM consumption.

Files changed: ${files.join(', ')}

Diff:
\`\`\`diff
${diffContent}
\`\`\`

Provide a structured summary:
1. **Overview**: What changed and why (infer from changes)
2. **Key Changes**: List major modifications by file
3. **Impact**: What functionality is affected
4. **Notable**: Any breaking changes, new features, or important refactors

Keep it concise and focused on what matters for understanding the changes.`;

      const result = await this.model.generateContent(prompt);
      const response = await result.response;
      const summary = response.text();

      return {
        success: true,
        summary,
        tokensUsed: response.usageMetadata?.totalTokenCount
      };
    } catch (error: any) {
      console.error('[LLM] Diff summarization error:', error);
      return {
        success: false,
        error: error.message || 'Failed to summarize diff'
      };
    }
  }

  async summarizeMultipleFiles(files: Array<{ path: string; content: string }>): Promise<SummarizeResult> {
    if (!this.isAvailable()) {
      return {
        success: false,
        error: 'LLM service not available. Please set GEMINI_API_KEY in .env file'
      };
    }

    try {
      const filesContent = files.map(f => 
        `### File: ${f.path}\n\`\`\`\n${f.content.substring(0, 5000)}\n\`\`\`\n`
      ).join('\n\n');

      const prompt = `You are a codebase summarization expert. Summarize these ${files.length} files as a cohesive overview for LLM consumption.

${filesContent}

Provide:
1. **Project Overview**: What these files accomplish together
2. **Architecture**: How components/modules relate
3. **Key Functionality**: Main features by file
4. **Dependencies**: Important libraries/frameworks
5. **Patterns**: Notable design patterns or approaches

Be concise but comprehensive. Focus on understanding the system.`;

      const result = await this.model.generateContent(prompt);
      const response = await result.response;
      const summary = response.text();

      return {
        success: true,
        summary,
        tokensUsed: response.usageMetadata?.totalTokenCount
      };
    } catch (error: any) {
      console.error('[LLM] Multi-file summarization error:', error);
      return {
        success: false,
        error: error.message || 'Failed to summarize files'
      };
    }
  }
}

export const llmService = new LLMService();
