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
 * Base LLM Provider Interface
 * Abstract base class for all LLM providers (OpenAI, Anthropic, etc.)
 */

export interface Message {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

export interface CompletionOptions {
  model?: string;
  temperature?: number;
  maxTokens?: number;
  stream?: boolean;
  stopSequences?: string[];
}

export interface CompletionResponse {
  content: string;
  usage?: {
    promptTokens: number;
    completionTokens: number;
    totalTokens: number;
  };
  finishReason?: string;
}

export interface StreamChunk {
  delta: string;
  done: boolean;
}

export abstract class BaseLLMProvider {
  protected apiKey: string;
  protected baseURL?: string;
  protected defaultModel: string;

  constructor(apiKey: string, defaultModel: string, baseURL?: string) {
    this.apiKey = apiKey;
    this.defaultModel = defaultModel;
    this.baseURL = baseURL;
  }

  /**
   * Generate a completion from messages
   */
  abstract complete(
    _messages: Message[],
    _options?: CompletionOptions
  ): Promise<CompletionResponse>;

  /**
   * Stream a completion from messages
   */
  abstract stream(
    _messages: Message[],
    _options?: CompletionOptions
  ): AsyncGenerator<StreamChunk, void, unknown>;

  /**
   * Validate API key and connection
   */
  abstract validate(): Promise<boolean>;

  /**
   * Get provider name
   */
  abstract getProviderName(): string;
}
