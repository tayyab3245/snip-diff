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
 * AI System Initializer
 * Initializes and configures the AI system with providers and settings
 */

import { BaseLLMProvider, GeminiProvider } from './providers';

export interface AIConfig {
  provider: 'openai' | 'anthropic' | 'gemini';
  apiKey: string;
  model?: string;
  temperature?: number;
  maxTokens?: number;
}

export class AIInitializer {
  private provider: BaseLLMProvider | null = null;
  private config: AIConfig | null = null;

  /**
   * Initialize AI system with configuration
   */
  async initialize(config: AIConfig): Promise<void> {
    console.log('[AI Initializer] initialize() called');
    console.log('[AI Initializer] Provider:', config.provider);
    console.log('[AI Initializer] Model:', config.model || 'gemini-2.0-flash');
    console.log('[AI Initializer] API key provided:', !!config.apiKey);
    console.log('[AI Initializer] API key length:', config.apiKey?.length || 0);
    
    this.config = config;

    // Create provider instance
    console.log('[AI Initializer] Creating provider instance...');
    switch (config.provider) {
      case 'gemini':
        this.provider = new GeminiProvider(
          config.apiKey,
          config.model || 'gemini-2.0-flash'
        );
        console.log('[AI Initializer] ✓ GeminiProvider created');
        break;
      default:
        throw new Error(`Unknown provider: ${config.provider}. Only 'gemini' is supported.`);
    }

    // Validate API key
    console.log('[AI Initializer] Validating API key...');
    const isValid = await this.provider.validate();
    console.log('[AI Initializer] Validation result:', isValid);
    
    if (!isValid) {
      throw new Error(`Failed to validate API key for ${config.provider}`);
    }

    console.log(`[AI Initializer] ✓ Initialized ${this.provider.getProviderName()} provider`);
  }

  /**
   * Get the current provider instance
   */
  getProvider(): BaseLLMProvider {
    if (!this.provider) {
      throw new Error('AI system not initialized. Call initialize() first.');
    }
    return this.provider;
  }

  /**
   * Get current configuration
   */
  getConfig(): AIConfig {
    if (!this.config) {
      throw new Error('AI system not initialized. Call initialize() first.');
    }
    return this.config;
  }

  /**
   * Check if AI system is initialized
   */
  isInitialized(): boolean {
    return this.provider !== null && this.config !== null;
  }

  /**
   * Shutdown AI system
   */
  shutdown(): void {
    this.provider = null;
    this.config = null;
    console.log('[AI] System shutdown');
  }
}

// Singleton instance
export const aiInitializer = new AIInitializer();
