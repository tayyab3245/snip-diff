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

  async initialize(apiKey: string): Promise<void> {
    console.log('[LLM Service] initialize() called');
    console.log('[LLM Service] Already initialized:', this.initialized);
    console.log('[LLM Service] API key provided:', !!apiKey);
    console.log('[LLM Service] API key length:', apiKey?.length || 0);
    
    if (this.initialized) {
      console.log('[LLM Service] Skipping - already initialized');
      return;
    }

    try {
      console.log('[LLM Service] Calling aiInitializer.initialize()...');
      await aiInitializer.initialize({
        provider: 'gemini',
        apiKey,
        model: 'gemini-2.0-flash',
        temperature: 0.7,
        maxTokens: 2048,
      });
      
      this.initialized = true;
      console.log('[LLM Service] ✓ AI system initialized successfully');
    } catch (error) {
      console.error('[LLM Service] ✗ Failed to initialize:', error);
      throw error;
    }
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

    try {
      const result = await aiOrchestrator.summarizeChanges(context);

      return {
        success: true,
        summary: result.content,
        tokensUsed: result.tokensUsed,
      };
    } catch (error: any) {
      console.error('[LLM Service] Diff summarization error:', error);
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
  // DEPRECATED - generateCommitMessage removed as buildCommitPrompt was removed
  // async generateCommitMessage(context: AgentContext): Promise<SummarizeResult> {
  //   if (!this.isAvailable()) {
  //     return {
  //       success: false,
  //       error: 'LLM service not initialized'
  //     };
  //   }

  //   try {
  //     const result = await aiOrchestrator.generateCommitMessage(context);

  //     return {
  //       success: true,
  //       summary: result.content,
  //       tokensUsed: result.tokensUsed,
  //     };
  //   } catch (error: any) {
  //     console.error('[LLM Service] Generate commit error:', error);
  //     return {
  //       success: false,
  //       error: error.message || 'Failed to generate commit message'
  //     };
  //   }
  // }
}

export const llmService = new LLMService();
