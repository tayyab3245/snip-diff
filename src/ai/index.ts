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
  GeminiProvider,
} from './providers';
export type {
  Message,
  CompletionOptions,
  CompletionResponse,
  StreamChunk,
} from './providers';

// Prompts
export { PromptBuilder } from './prompts/prompt-builder';

// Parsing
export { AIResponseParser } from './parsing';
export type { ParsedAIResponse } from './parsing';

// Utils
export * as AIUtils from './utils';
