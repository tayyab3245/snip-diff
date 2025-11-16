/**
 * AI Utilities
 * Helper functions for AI operations
 */

/**
 * Estimate token count for text (rough approximation)
 */
export function estimateTokens(text: string): number {
  // Rough estimate: 1 token ≈ 4 characters
  return Math.ceil(text.length / 4);
}

/**
 * Truncate text to fit token limit
 */
export function truncateToTokens(text: string, maxTokens: number): string {
  const estimatedTokens = estimateTokens(text);
  
  if (estimatedTokens <= maxTokens) {
    return text;
  }

  const ratio = maxTokens / estimatedTokens;
  const targetLength = Math.floor(text.length * ratio);
  
  return text.slice(0, targetLength) + '...';
}

/**
 * Format code for AI context
 */
export function formatCodeForAI(code: string, language: string): string {
  return `\`\`\`${language}\n${code}\n\`\`\``;
}

/**
 * Extract code blocks from AI response
 */
export function extractCodeBlocks(response: string): Array<{ language: string; code: string }> {
  const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
  const blocks: Array<{ language: string; code: string }> = [];
  
  let match;
  while ((match = codeBlockRegex.exec(response)) !== null) {
    blocks.push({
      language: match[1] || 'plaintext',
      code: match[2].trim(),
    });
  }
  
  return blocks;
}

/**
 * Sanitize input for AI prompt
 */
export function sanitizeInput(input: string): string {
  // Remove potentially problematic characters
  return input
    .replace(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/g, '') // Control characters
    .trim();
}

/**
 * Build context summary from multiple sources
 */
export function buildContextSummary(data: {
  files?: string[];
  changes?: number;
  additions?: number;
  deletions?: number;
}): string {
  const parts: string[] = [];
  
  if (data.files && data.files.length > 0) {
    parts.push(`${data.files.length} file(s)`);
  }
  
  if (data.changes !== undefined) {
    parts.push(`${data.changes} change(s)`);
  }
  
  if (data.additions !== undefined) {
    parts.push(`+${data.additions}`);
  }
  
  if (data.deletions !== undefined) {
    parts.push(`-${data.deletions}`);
  }
  
  return parts.join(', ');
}

/**
 * Parse AI response for structured data
 */
export function parseStructuredResponse<T>(response: string): T | null {
  try {
    // Look for JSON in response
    const jsonMatch = response.match(/```json\n([\s\S]*?)```/);
    if (jsonMatch) {
      return JSON.parse(jsonMatch[1]) as T;
    }
    
    // Try parsing entire response
    return JSON.parse(response) as T;
  } catch {
    return null;
  }
}
