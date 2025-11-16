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
    messages: Message[],
    options?: CompletionOptions
  ): Promise<CompletionResponse>;

  /**
   * Stream a completion from messages
   */
  abstract stream(
    messages: Message[],
    options?: CompletionOptions
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
