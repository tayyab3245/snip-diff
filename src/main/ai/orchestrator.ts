/**
 * AI System Orchestrator
 * Main coordinator for AI agent operations, tool execution, and memory management
 */

import { aiInitializer } from './initializer';
import { Message } from './providers';
import { MemoryManager } from './memory/memory-manager';
import { ToolRegistry } from './tools/tool-registry';
import { PromptManager } from './prompts/prompt-manager';

export interface AgentContext {
  repoPath: string;
  selectedFiles: string[];
  gitStatus: Map<string, string>;
  diffContent?: string;
}

export interface AgentResponse {
  content: string;
  toolsUsed?: string[];
  tokensUsed?: number;
}

export class AIOrchestrator {
  private memory: MemoryManager;
  private toolRegistry: ToolRegistry;
  private promptManager: PromptManager;

  constructor() {
    this.memory = new MemoryManager();
    this.toolRegistry = new ToolRegistry();
    this.promptManager = new PromptManager();
  }

  /**
   * Execute an AI task with given context
   */
  async execute(
    task: string,
    context: AgentContext,
    stream = false
  ): Promise<AgentResponse> {
    // Ensure AI is initialized
    if (!aiInitializer.isInitialized()) {
      throw new Error('AI system not initialized');
    }

    const provider = aiInitializer.getProvider();
    const config = aiInitializer.getConfig();

    // Build system prompt
    const systemPrompt = this.promptManager.getSystemPrompt();
    
    // Build task-specific prompt
    const taskPrompt = this.promptManager.buildTaskPrompt(task, context);

    // Get conversation history
    const history = this.memory.getRecentMessages(5);

    // Combine messages
    const messages: Message[] = [
      { role: 'system', content: systemPrompt },
      ...history,
      { role: 'user', content: taskPrompt },
    ];

    // Execute with provider
    if (stream) {
      // TODO: Implement streaming response
      throw new Error('Streaming not yet implemented');
    } else {
      const response = await provider.complete(messages, {
        temperature: config.temperature,
        maxTokens: config.maxTokens,
      });

      // Store in memory
      this.memory.addMessage({ role: 'user', content: taskPrompt });
      this.memory.addMessage({ role: 'assistant', content: response.content });

      return {
        content: response.content,
        tokensUsed: response.usage?.totalTokens,
      };
    }
  }

  /**
   * Summarize repository changes
   */
  async summarizeChanges(context: AgentContext): Promise<AgentResponse> {
    return this.execute('summarize_changes', context);
  }

  /**
   * Generate commit message
   */
  async generateCommitMessage(context: AgentContext): Promise<AgentResponse> {
    return this.execute('generate_commit_message', context);
  }

  /**
   * Explain code changes
   */
  async explainChanges(context: AgentContext): Promise<AgentResponse> {
    return this.execute('explain_changes', context);
  }

  /**
   * Clear conversation memory
   */
  clearMemory(): void {
    this.memory.clear();
  }

  /**
   * Get memory stats
   */
  getMemoryStats() {
    return this.memory.getStats();
  }
}

// Singleton instance
export const aiOrchestrator = new AIOrchestrator();
