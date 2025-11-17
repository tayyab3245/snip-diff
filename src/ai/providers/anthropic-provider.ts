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
 * Anthropic Claude Provider for SNIP-DIFF AI
 * Implements the BaseLLMProvider interface for Anthropic's Claude models
 */

import { BaseLLMProvider, Message, CompletionOptions, CompletionResponse, StreamChunk } from './base-provider';

export class AnthropicProvider extends BaseLLMProvider {
  constructor(apiKey: string, defaultModel: string = 'claude-3-5-sonnet-20241022') {
    super(apiKey, defaultModel, 'https://api.anthropic.com');
  }

  async complete(messages: Message[], options?: CompletionOptions): Promise<CompletionResponse> {
    try {
      const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': this.apiKey,
          'anthropic-version': '2023-06-01'
        },
        body: JSON.stringify({
          model: options?.model || this.defaultModel,
          max_tokens: options?.maxTokens || 4096,
          temperature: options?.temperature || 0.7,
          stop_sequences: options?.stopSequences,
          messages: messages.filter(m => m.role !== 'system').map(m => ({
            role: m.role === 'assistant' ? 'assistant' : 'user',
            content: m.content
          })),
          // Add system message as a parameter if present
          ...(messages.find(m => m.role === 'system') && {
            system: messages.find(m => m.role === 'system')?.content
          })
        })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(`Anthropic API error: ${response.status} ${response.statusText} - ${JSON.stringify(errorData)}`);
      }

      const data = await response.json() as any;
      
      return {
        content: data.content[0]?.text || '',
        usage: {
          promptTokens: data.usage?.input_tokens || 0,
          completionTokens: data.usage?.output_tokens || 0,
          totalTokens: (data.usage?.input_tokens || 0) + (data.usage?.output_tokens || 0)
        },
        finishReason: data.stop_reason || 'stop'
      };
    } catch (error) {
      throw new Error(`Anthropic provider error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  async* stream(messages: Message[], options?: CompletionOptions): AsyncGenerator<StreamChunk, void, unknown> {
    try {
      const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': this.apiKey,
          'anthropic-version': '2023-06-01'
        },
        body: JSON.stringify({
          model: options?.model || this.defaultModel,
          max_tokens: options?.maxTokens || 4096,
          temperature: options?.temperature || 0.7,
          stop_sequences: options?.stopSequences,
          stream: true,
          messages: messages.filter(m => m.role !== 'system').map(m => ({
            role: m.role === 'assistant' ? 'assistant' : 'user',
            content: m.content
          })),
          ...(messages.find(m => m.role === 'system') && {
            system: messages.find(m => m.role === 'system')?.content
          })
        })
      });

      if (!response.ok) {
        throw new Error(`Anthropic API error: ${response.status} ${response.statusText}`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('No response body');
      }

      const decoder = new TextDecoder();
      let buffer = '';

      try {
        while (true) {
          const { done, value } = await reader.read();
          
          if (done) {
            yield { delta: '', done: true };
            break;
          }

          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split('\n');
          buffer = lines.pop() || '';

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const data = line.slice(6);
              if (data === '[DONE]') {
                yield { delta: '', done: true };
                return;
              }

              try {
                const parsed = JSON.parse(data);
                if (parsed.type === 'content_block_delta') {
                  yield { delta: parsed.delta?.text || '', done: false };
                }
              } catch {
                // Skip invalid JSON
              }
            }
          }
        }
      } finally {
        reader.releaseLock();
      }
    } catch (error) {
      throw new Error(`Anthropic stream error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  async validate(): Promise<boolean> {
    try {
      const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': this.apiKey,
          'anthropic-version': '2023-06-01'
        },
        body: JSON.stringify({
          model: this.defaultModel,
          max_tokens: 1,
          messages: [{ role: 'user', content: 'Test' }]
        })
      });

      return response.ok;
    } catch {
      return false;
    }
  }

  getProviderName(): string {
    return 'anthropic';
  }
}