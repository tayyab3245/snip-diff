/**
 * Token Tracker - Monitors file content and AI summary compression
 */

export interface FileTokenData {
  filePath: string;
  originalTokens: number;
  originalCharacters: number;
  summaryTokens?: number;
  summaryCharacters?: number;
  compressionRatio?: number;
  timestamp: number;
}

export interface TokenTrackingState {
  files: Map<string, FileTokenData>;
  totalOriginalTokens: number;
  totalSummaryTokens: number;
}

export class TokenTracker {
  private static instance: TokenTracker;
  private state: TokenTrackingState = {
    files: new Map(),
    totalOriginalTokens: 0,
    totalSummaryTokens: 0,
  };

  static getInstance(): TokenTracker {
    if (!TokenTracker.instance) {
      TokenTracker.instance = new TokenTracker();
    }
    return TokenTracker.instance;
  }

  /**
   * Estimate token count using character-based approximation
   * GPT models typically use ~4 characters per token for English text
   */
  private estimateTokens(text: string): number {
    // More accurate estimation: consider whitespace, punctuation, code structure
    const words = text.split(/\s+/).filter(word => word.length > 0);
    const codeTokens = text.match(/[{}();,.[\]]/g)?.length || 0;
    const whitespace = text.match(/\s/g)?.length || 0;
    
    // Rough estimation: words + code tokens + whitespace/4
    return Math.ceil(words.length + codeTokens + whitespace / 4);
  }

  /**
   * Track original file content before analysis
   */
  trackOriginalFile(filePath: string, content: string): void {
    const tokens = this.estimateTokens(content);
    const characters = content.length;

    this.state.files.set(filePath, {
      filePath,
      originalTokens: tokens,
      originalCharacters: characters,
      timestamp: Date.now(),
    });

    this.updateTotals();
  }

  /**
   * Track AI summary for a file
   */
  trackSummary(filePath: string, summaryContent: string): void {
    const existing = this.state.files.get(filePath);
    if (!existing) {
      console.warn(`No original data found for file: ${filePath}`);
      return;
    }

    const summaryTokens = this.estimateTokens(summaryContent);
    const summaryCharacters = summaryContent.length;
    const compressionRatio = existing.originalTokens > 0 
      ? (existing.originalTokens - summaryTokens) / existing.originalTokens 
      : 0;

    const updated: FileTokenData = {
      ...existing,
      summaryTokens,
      summaryCharacters,
      compressionRatio,
    };

    this.state.files.set(filePath, updated);
    this.updateTotals();
  }

  /**
   * Get token data for a specific file
   */
  getFileTokenData(filePath: string): FileTokenData | undefined {
    return this.state.files.get(filePath);
  }

  /**
   * Get token data for multiple files
   */
  getFilesTokenData(filePaths: string[]): FileTokenData[] {
    return filePaths
      .map(path => this.state.files.get(path))
      .filter((data): data is FileTokenData => data !== undefined);
  }

  /**
   * Get summary statistics
   */
  getSummaryStats(): {
    totalFiles: number;
    totalOriginalTokens: number;
    totalSummaryTokens: number;
    overallCompressionRatio: number;
    averageCompressionRatio: number;
  } {
    const filesWithSummaries = Array.from(this.state.files.values())
      .filter(file => file.summaryTokens !== undefined);

    const totalSummaryTokens = filesWithSummaries
      .reduce((sum, file) => sum + (file.summaryTokens || 0), 0);

    const totalOriginalTokens = filesWithSummaries
      .reduce((sum, file) => sum + file.originalTokens, 0);

    const overallCompressionRatio = totalOriginalTokens > 0
      ? (totalOriginalTokens - totalSummaryTokens) / totalOriginalTokens
      : 0;

    const averageCompressionRatio = filesWithSummaries.length > 0
      ? filesWithSummaries.reduce((sum, file) => sum + (file.compressionRatio || 0), 0) / filesWithSummaries.length
      : 0;

    return {
      totalFiles: this.state.files.size,
      totalOriginalTokens,
      totalSummaryTokens,
      overallCompressionRatio,
      averageCompressionRatio,
    };
  }

  /**
   * Clear tracking data for files
   */
  clearFiles(filePaths?: string[]): void {
    if (filePaths) {
      filePaths.forEach(path => this.state.files.delete(path));
    } else {
      this.state.files.clear();
    }
    this.updateTotals();
  }

  /**
   * Reset all tracking data
   */
  reset(): void {
    this.state.files.clear();
    this.state.totalOriginalTokens = 0;
    this.state.totalSummaryTokens = 0;
  }

  /**
   * Format compression ratio for display
   */
  formatCompressionRatio(ratio: number): string {
    return `${Math.round(ratio * 100)}%`;
  }

  /**
   * Get color for compression ratio display
   */
  getCompressionColor(ratio: number): string {
    if (ratio >= 0.7) return '#10b981'; // Green - excellent compression
    if (ratio >= 0.5) return '#f59e0b'; // Yellow - good compression
    if (ratio >= 0.3) return '#ef4444'; // Red - poor compression
    return '#6b7280'; // Gray - very poor compression
  }

  private updateTotals(): void {
    const files = Array.from(this.state.files.values());
    
    this.state.totalOriginalTokens = files
      .reduce((sum, file) => sum + file.originalTokens, 0);
    
    this.state.totalSummaryTokens = files
      .reduce((sum, file) => sum + (file.summaryTokens || 0), 0);
  }
}