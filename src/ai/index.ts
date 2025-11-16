/**
 * AI System Main Index
 * Central export for all AI components
 */

// Core system
export { aiInitializer, AIInitializer } from './initializer';
export { aiOrchestrator, AIOrchestrator } from './orchestrator';
export type { AIConfig } from './initializer';
export type { AgentContext, AgentResponse } from './orchestrator';

// Providers
export {
  BaseLLMProvider,
  OpenAIProvider,
  AnthropicProvider,
  GeminiProvider,
} from './providers';
export type {
  Message,
  CompletionOptions,
  CompletionResponse,
  StreamChunk,
} from './providers';

// Memory
export { MemoryManager } from './memory';
export type { MemoryStats } from './memory';

// Tools
export { ToolRegistry, fileAnalysisTool } from './tools';
export type { Tool } from './tools';

// Prompts
export { PromptManager } from './prompts';

// Utils
export * as AIUtils from './utils';
