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
 * LLM Service for SNIP-DIFF
 * Main process service that uses the AI architecture (src/ai)
 * Pure wrapper - does not handle file I/O, caller provides all data
 */

import { aiInitializer, aiOrchestrator, AgentContext } from '../../ai';

export interface SummarizeResult {
  success: boolean;
  summary?: string;
  tokensUsed?: number;
  error?: string;
}

export class LLMService {
  private initialized = false;
  private lastRequestTime = 0;
  private readonly minRequestInterval = 2000; // 2 seconds between requests

  async initialize(apiKey: string): Promise<void> {
    if (this.initialized) {
      return;
    }

    await aiInitializer.initialize({
      provider: 'gemini',
      apiKey,
      model: 'gemini-2.0-flash',
      temperature: 0.7,
      maxTokens: 8192,
    });
    
    this.initialized = true;
  }

  isAvailable(): boolean {
    return this.initialized;
  }

  /**
   * Summarize changes based on provided context
   * Caller must provide all data (diff content, file paths, git status)
   */
  async summarizeDiff(context: AgentContext): Promise<SummarizeResult> {
    if (!this.isAvailable()) {
      return {
        success: false,
        error: 'LLM service not initialized'
      };
    }

    // Rate limiting check
    const now = Date.now();
    const timeSinceLastRequest = now - this.lastRequestTime;
    if (timeSinceLastRequest < this.minRequestInterval) {
      const waitTime = Math.ceil((this.minRequestInterval - timeSinceLastRequest) / 1000);
      return {
        success: false,
        error: `Please wait ${waitTime} second${waitTime > 1 ? 's' : ''} before making another request`
      };
    }

    this.lastRequestTime = now;

    try {
      const result = await aiOrchestrator.summarizeChanges(context);

      return {
        success: true,
        summary: result.content,
        tokensUsed: result.tokensUsed,
      };
    } catch (error: any) {
      return {
        success: false,
        error: error.message || 'Failed to summarize diff'
      };
    }
  }

  /**
   * Generate commit message based on provided context
   * Caller must provide all data (diff content, file paths, git status)
   */
}

export const llmService = new LLMService();
