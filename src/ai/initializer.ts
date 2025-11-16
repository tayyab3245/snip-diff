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
    this.config = config;

    // Create provider instance
    switch (config.provider) {
      case 'gemini':
        this.provider = new GeminiProvider(
          config.apiKey,
          config.model || 'gemini-pro'
        );
        break;
      default:
        throw new Error(`Unknown provider: ${config.provider}. Only 'gemini' is supported.`);
    }

    // Validate API key
    const isValid = await this.provider.validate();
    if (!isValid) {
      throw new Error(`Failed to validate API key for ${config.provider}`);
    }

    console.log(`[AI] Initialized ${this.provider.getProviderName()} provider`);
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
