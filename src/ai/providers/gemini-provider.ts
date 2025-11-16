/**
 * Google Gemini LLM Provider
 * Implementation for Google Gemini API (Gemini Pro, Gemini Ultra, etc.)
 */

import {
  BaseLLMProvider,
  Message,
  CompletionOptions,
  CompletionResponse,
  StreamChunk,
} from './base-provider';

export class GeminiProvider extends BaseLLMProvider {
  private readonly apiEndpoint = 'https://generativelanguage.googleapis.com/v1';

  constructor(apiKey: string, model: string = 'gemini-2.0-flash') {
    super(apiKey, model);
  }

  private convertMessages(messages: Message[]): { role: string; parts: { text: string }[] }[] {
    // Gemini uses 'user' and 'model' roles, system messages go into first user message
    const systemMessage = messages.find(m => m.role === 'system');
    const conversationMessages = messages.filter(m => m.role !== 'system');

    const geminiMessages = conversationMessages.map(msg => ({
      role: msg.role === 'assistant' ? 'model' : 'user',
      parts: [{ text: msg.content }],
    }));

    // Prepend system message to first user message if exists
    if (systemMessage && geminiMessages.length > 0 && geminiMessages[0].role === 'user') {
      geminiMessages[0].parts[0].text = `${systemMessage.content}\n\n${geminiMessages[0].parts[0].text}`;
    }

    return geminiMessages;
  }

  async complete(
    messages: Message[],
    options?: CompletionOptions
  ): Promise<CompletionResponse> {
    const geminiMessages = this.convertMessages(messages);
    const model = options?.model || this.defaultModel;
    const url = `${this.apiEndpoint}/models/${model}:generateContent?key=${this.apiKey}`;

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        contents: geminiMessages,
        generationConfig: {
          temperature: options?.temperature ?? 0.7,
          maxOutputTokens: options?.maxTokens,
          stopSequences: options?.stopSequences,
        },
      }),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: { message: response.statusText } }));
      throw new Error(`Gemini API error: ${(error as any).error?.message || response.statusText}`);
    }

    const data = await response.json() as any;
    
    if (!data.candidates || data.candidates.length === 0) {
      throw new Error('No response from Gemini API');
    }

    const candidate = data.candidates[0];
    const content = candidate.content?.parts?.[0]?.text || '';

    return {
      content,
      usage: data.usageMetadata ? {
        promptTokens: data.usageMetadata.promptTokenCount,
        completionTokens: data.usageMetadata.candidatesTokenCount,
        totalTokens: data.usageMetadata.totalTokenCount,
      } : undefined,
      finishReason: candidate.finishReason,
    };
  }

  async *stream(
    messages: Message[],
    options?: CompletionOptions
  ): AsyncGenerator<StreamChunk, void, unknown> {
    const geminiMessages = this.convertMessages(messages);
    const model = options?.model || this.defaultModel;
    const url = `${this.apiEndpoint}/models/${model}:streamGenerateContent?key=${this.apiKey}`;

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        contents: geminiMessages,
        generationConfig: {
          temperature: options?.temperature ?? 0.7,
          maxOutputTokens: options?.maxTokens,
          stopSequences: options?.stopSequences,
        },
      }),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: { message: response.statusText } }));
      throw new Error(`Gemini API error: ${(error as any).error?.message || response.statusText}`);
    }

    const reader = response.body?.getReader();
    if (!reader) throw new Error('No response body');

    const decoder = new TextDecoder();
    let buffer = '';

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.trim() === '' || line.trim() === '[{' || line.trim() === '}]') continue;
          
          try {
            // Remove trailing comma if present
            const cleanLine = line.trim().replace(/,\s*$/, '');
            if (!cleanLine || cleanLine === '{' || cleanLine === '}') continue;

            const data = JSON.parse(cleanLine);
            
            if (data.candidates && data.candidates[0]?.content?.parts) {
              const delta = data.candidates[0].content.parts[0]?.text || '';
              
              if (delta) {
                yield { delta, done: false };
              }

              if (data.candidates[0].finishReason && data.candidates[0].finishReason !== 'STOP') {
                yield { delta: '', done: true };
                return;
              }
            }
          } catch (err) {
            // Skip malformed JSON lines
            continue;
          }
        }
      }
    } finally {
      reader.releaseLock();
    }

    yield { delta: '', done: true };
  }

  async validate(): Promise<boolean> {
    console.log('[Gemini Provider] validate() called');
    console.log('[Gemini Provider] API key available:', !!this.apiKey);
    console.log('[Gemini Provider] API key length:', this.apiKey?.length || 0);
    console.log('[Gemini Provider] Model:', this.defaultModel);
    
    try {
      const url = `${this.apiEndpoint}/models/${this.defaultModel}?key=${this.apiKey}`;
      console.log('[Gemini Provider] Validation URL:', url.replace(this.apiKey, '***KEY***'));
      
      const response = await fetch(url);
      console.log('[Gemini Provider] Response status:', response.status);
      console.log('[Gemini Provider] Response OK:', response.ok);
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('[Gemini Provider] Validation failed:', errorText);
      }
      
      return response.ok;
    } catch (error) {
      console.error('[Gemini Provider] Validation error:', error);
      return false;
    }
  }

  getProviderName(): string {
    return 'Google Gemini';
  }
}
