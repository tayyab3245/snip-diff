/**
 * Anthropic LLM Provider
 * Implementation for Anthropic API (Claude 3, etc.)
 */

import {
  BaseLLMProvider,
  Message,
  CompletionOptions,
  CompletionResponse,
  StreamChunk,
} from './base-provider';

export class AnthropicProvider extends BaseLLMProvider {
  private readonly apiEndpoint = 'https://api.anthropic.com/v1/messages';
  private readonly apiVersion = '2023-06-01';

  constructor(apiKey: string, model: string = 'claude-3-opus-20240229') {
    super(apiKey, model);
  }

  async complete(
    messages: Message[],
    options?: CompletionOptions
  ): Promise<CompletionResponse> {
    // Anthropic requires system message to be separate
    const systemMessage = messages.find(m => m.role === 'system');
    const conversationMessages = messages.filter(m => m.role !== 'system');

    const response = await fetch(this.apiEndpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': this.apiKey,
        'anthropic-version': this.apiVersion,
      },
      body: JSON.stringify({
        model: options?.model || this.defaultModel,
        messages: conversationMessages,
        system: systemMessage?.content,
        max_tokens: options?.maxTokens || 4096,
        temperature: options?.temperature ?? 0.7,
        stop_sequences: options?.stopSequences,
        stream: false,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(`Anthropic API error: ${error.error?.message || response.statusText}`);
    }

    const data = await response.json();
    
    return {
      content: data.content[0].text,
      usage: data.usage ? {
        promptTokens: data.usage.input_tokens,
        completionTokens: data.usage.output_tokens,
        totalTokens: data.usage.input_tokens + data.usage.output_tokens,
      } : undefined,
      finishReason: data.stop_reason,
    };
  }

  async *stream(
    messages: Message[],
    options?: CompletionOptions
  ): AsyncGenerator<StreamChunk, void, unknown> {
    const systemMessage = messages.find(m => m.role === 'system');
    const conversationMessages = messages.filter(m => m.role !== 'system');

    const response = await fetch(this.apiEndpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': this.apiKey,
        'anthropic-version': this.apiVersion,
      },
      body: JSON.stringify({
        model: options?.model || this.defaultModel,
        messages: conversationMessages,
        system: systemMessage?.content,
        max_tokens: options?.maxTokens || 4096,
        temperature: options?.temperature ?? 0.7,
        stop_sequences: options?.stopSequences,
        stream: true,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(`Anthropic API error: ${error.error?.message || response.statusText}`);
    }

    const reader = response.body?.getReader();
    if (!reader) throw new Error('No response body');

    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (line.trim() === '' || !line.startsWith('data: ')) continue;
        
        try {
          const data = JSON.parse(line.slice(6));
          
          if (data.type === 'content_block_delta') {
            const delta = data.delta.text || '';
            if (delta) {
              yield { delta, done: false };
            }
          }

          if (data.type === 'message_stop') {
            yield { delta: '', done: true };
            return;
          }
        } catch (err) {
          console.error('Error parsing SSE:', err);
        }
      }
    }

    yield { delta: '', done: true };
  }

  async validate(): Promise<boolean> {
    try {
      const response = await fetch(this.apiEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': this.apiKey,
          'anthropic-version': this.apiVersion,
        },
        body: JSON.stringify({
          model: this.defaultModel,
          messages: [{ role: 'user', content: 'Hi' }],
          max_tokens: 10,
        }),
      });
      return response.ok;
    } catch {
      return false;
    }
  }

  getProviderName(): string {
    return 'Anthropic';
  }
}
