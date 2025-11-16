/**
 * AI System Orchestrator
 * Main coordinator for AI agent operations - stateless, context-based only
 */

import { aiInitializer } from './initializer';
import { Message } from './providers';
import { PromptBuilder } from './prompts/prompt-builder';
import { AIResponseParser, ParsedAIResponse } from './parsing';

export interface AgentContext {
  repoPath: string;
  selectedFiles: string[];
  gitStatus: Map<string, string>;
  diffContent: string; // Always provided by caller (from git service)
  fileContents?: Map<string, string>; // Optional full file contents (from file service)
}

export interface AgentResponse {
  content: string;
  toolsUsed?: string[];
  tokensUsed?: number;
  parsed?: ParsedAIResponse; // Structured parsed response
}

export class AIOrchestrator {
  private promptBuilder: PromptBuilder;
  private responseParser: AIResponseParser;

  constructor() {
    this.promptBuilder = new PromptBuilder();
    this.responseParser = new AIResponseParser();
  }

  /**
   * Summarize repository changes (stateless)
   */
  async summarizeChanges(context: AgentContext): Promise<AgentResponse> {
    // Ensure AI is initialized
    if (!aiInitializer.isInitialized()) {
      throw new Error('AI system not initialized');
    }

    const provider = aiInitializer.getProvider();
    const config = aiInitializer.getConfig();

    // Build the complete prompt using PromptBuilder (no conversation history)
    const userPrompt = this.promptBuilder.buildSummarizePrompt(context, []);

    // Build message (single turn, no history)
    const messages: Message[] = [
      { role: 'user', content: userPrompt },
    ];

    // Execute with provider
    const response = await provider.complete(messages, {
      temperature: config.temperature,
      maxTokens: config.maxTokens,
    });

    // Parse and validate the response
    const parsed = this.responseParser.parseResponse(
      response.content,
      response.usage?.totalTokens
    );

    // Validate the parsed response
    if (!this.responseParser.validateResponse(parsed)) {
      const errorMsg = this.responseParser.extractErrorMessage(parsed);
      throw new Error(`Invalid AI response: ${errorMsg}`);
    }

    return {
      content: parsed.displayContent,
      tokensUsed: response.usage?.totalTokens,
      parsed, // Include full parsed response for frontend
    };
  }

  /**
   * Generate commit message (stateless)
   */
  async generateCommitMessage(context: AgentContext): Promise<AgentResponse> {
    // Ensure AI is initialized
    if (!aiInitializer.isInitialized()) {
      throw new Error('AI system not initialized');
    }

    const provider = aiInitializer.getProvider();
    const config = aiInitializer.getConfig();

    // Build the complete prompt using PromptBuilder (no conversation history)
    const userPrompt = this.promptBuilder.buildCommitPrompt(context, []);

    // Build message (single turn, no history)
    const messages: Message[] = [
      { role: 'user', content: userPrompt },
    ];

    // Execute with provider
    const response = await provider.complete(messages, {
      temperature: config.temperature,
      maxTokens: config.maxTokens,
    });

    // Parse and validate the response
    const parsed = this.responseParser.parseResponse(
      response.content,
      response.usage?.totalTokens
    );

    // Validate the parsed response
    if (!this.responseParser.validateResponse(parsed)) {
      const errorMsg = this.responseParser.extractErrorMessage(parsed);
      throw new Error(`Invalid AI response: ${errorMsg}`);
    }

    return {
      content: parsed.displayContent,
      tokensUsed: response.usage?.totalTokens,
      parsed, // Include full parsed response for frontend
    };
  }

  /**
   * Explain code changes (stateless)
   */
  async explainChanges(context: AgentContext): Promise<AgentResponse> {
    // Ensure AI is initialized
    if (!aiInitializer.isInitialized()) {
      throw new Error('AI system not initialized');
    }

    const provider = aiInitializer.getProvider();
    const config = aiInitializer.getConfig();

    // Build the complete prompt using PromptBuilder (no conversation history)
    const userPrompt = this.promptBuilder.buildExplainPrompt(context, []);

    // Build message (single turn, no history)
    const messages: Message[] = [
      { role: 'user', content: userPrompt },
    ];

    // Execute with provider
    const response = await provider.complete(messages, {
      temperature: config.temperature,
      maxTokens: config.maxTokens,
    });

    // Parse and validate the response
    const parsed = this.responseParser.parseResponse(
      response.content,
      response.usage?.totalTokens
    );

    // Validate the parsed response
    if (!this.responseParser.validateResponse(parsed)) {
      const errorMsg = this.responseParser.extractErrorMessage(parsed);
      throw new Error(`Invalid AI response: ${errorMsg}`);
    }

    return {
      content: parsed.displayContent,
      tokensUsed: response.usage?.totalTokens,
      parsed, // Include full parsed response for frontend
    };
  }
}

// Singleton instance
export const aiOrchestrator = new AIOrchestrator();
