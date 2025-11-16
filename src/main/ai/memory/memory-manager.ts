/**
 * Memory Manager
 * Manages conversation history and context for the AI agent
 */

import { Message } from '../providers';

export interface MemoryStats {
  messageCount: number;
  totalTokens: number;
  oldestMessage?: Date;
  newestMessage?: Date;
}

export class MemoryManager {
  private messages: Array<Message & { timestamp: Date }> = [];
  private maxMessages = 50; // Keep last 50 messages
  private estimatedTokens = 0;

  /**
   * Add a message to memory
   */
  addMessage(message: Message): void {
    this.messages.push({
      ...message,
      timestamp: new Date(),
    });

    // Estimate tokens (rough approximation: 1 token ≈ 4 chars)
    this.estimatedTokens += Math.ceil(message.content.length / 4);

    // Trim if exceeds max
    if (this.messages.length > this.maxMessages) {
      const removed = this.messages.shift();
      if (removed) {
        this.estimatedTokens -= Math.ceil(removed.content.length / 4);
      }
    }
  }

  /**
   * Get recent messages
   */
  getRecentMessages(count = 10): Message[] {
    return this.messages
      .slice(-count)
      .map(({ role, content }) => ({ role, content }));
  }

  /**
   * Get all messages
   */
  getAllMessages(): Message[] {
    return this.messages.map(({ role, content }) => ({ role, content }));
  }

  /**
   * Clear all memory
   */
  clear(): void {
    this.messages = [];
    this.estimatedTokens = 0;
    console.log('[AI Memory] Cleared conversation history');
  }

  /**
   * Get memory statistics
   */
  getStats(): MemoryStats {
    return {
      messageCount: this.messages.length,
      totalTokens: this.estimatedTokens,
      oldestMessage: this.messages[0]?.timestamp,
      newestMessage: this.messages[this.messages.length - 1]?.timestamp,
    };
  }

  /**
   * Summarize memory for long conversations
   */
  async summarize(): Promise<string> {
    // TODO: Use AI to summarize old messages
    const messages = this.getAllMessages();
    return `Conversation history: ${messages.length} messages`;
  }

  /**
   * Set maximum messages to keep
   */
  setMaxMessages(max: number): void {
    this.maxMessages = max;
    
    // Trim if necessary
    while (this.messages.length > this.maxMessages) {
      this.messages.shift();
    }
  }
}
