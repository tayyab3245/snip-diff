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
  AnthropicProvider,
  OpenAIProvider,
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
