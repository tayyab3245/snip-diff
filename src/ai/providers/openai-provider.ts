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
 * OpenAI Provider for SNIP-DIFF AI
 * Implements the BaseLLMProvider interface for OpenAI's GPT models
 */

import { BaseLLMProvider, Message, CompletionOptions, CompletionResponse, StreamChunk } from './base-provider';

export class OpenAIProvider extends BaseLLMProvider {
  constructor(apiKey: string, defaultModel: string = 'gpt-4o') {
    super(apiKey, defaultModel, 'https://api.openai.com');
  }

  async complete(messages: Message[], options?: CompletionOptions): Promise<CompletionResponse> {
    try {
      const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`
        },
        body: JSON.stringify({
          model: options?.model || this.defaultModel,
          messages: messages.map(m => ({
            role: m.role,
            content: m.content
          })),
          max_tokens: options?.maxTokens || 4096,
          temperature: options?.temperature || 0.7,
          stop: options?.stopSequences
        })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(`OpenAI API error: ${response.status} ${response.statusText} - ${JSON.stringify(errorData)}`);
      }

      const data = await response.json() as any;
      const choice = data.choices[0];
      
      return {
        content: choice.message.content || '',
        usage: {
          promptTokens: data.usage?.prompt_tokens || 0,
          completionTokens: data.usage?.completion_tokens || 0,
          totalTokens: data.usage?.total_tokens || 0
        },
        finishReason: choice.finish_reason || 'stop'
      };
    } catch (error) {
      throw new Error(`OpenAI provider error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  async* stream(messages: Message[], options?: CompletionOptions): AsyncGenerator<StreamChunk, void, unknown> {
    try {
      const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`
        },
        body: JSON.stringify({
          model: options?.model || this.defaultModel,
          messages: messages.map(m => ({
            role: m.role,
            content: m.content
          })),
          max_tokens: options?.maxTokens || 4096,
          temperature: options?.temperature || 0.7,
          stop: options?.stopSequences,
          stream: true
        })
      });

      if (!response.ok) {
        throw new Error(`OpenAI API error: ${response.status} ${response.statusText}`);
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
                const delta = parsed.choices[0]?.delta?.content;
                if (delta) {
                  yield { delta, done: false };
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
      throw new Error(`OpenAI stream error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  async validate(): Promise<boolean> {
    try {
      const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`
        },
        body: JSON.stringify({
          model: this.defaultModel,
          messages: [{ role: 'user', content: 'Test' }],
          max_tokens: 1
        })
      });

      return response.ok;
    } catch {
      return false;
    }
  }

  getProviderName(): string {
    return 'openai';
  }
}