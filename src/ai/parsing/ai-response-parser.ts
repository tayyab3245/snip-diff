/**
 * AI Response Parser
 * Parses and validates AI responses to ensure structured JSON output
 */

export interface FileSummary {
  path: string;
  category: 'Feature Addition' | 'Bug Fix' | 'Refactoring' | 'Breaking Change' | 'Documentation' | 'Configuration';
  summary: string;
  keyChanges: string[];
  linesAdded: number;
  linesDeleted: number;
}

export interface SummaryOverview {
  summary: string;
  totalFiles: number;
  categories: string[];
}

export interface SummaryImpact {
  severity: 'minor' | 'moderate' | 'major';
  description: string;
  breaking: boolean;
  concerns: string[];
}

export interface StructuredSummary {
  overview: SummaryOverview;
  files: FileSummary[];
  impact: SummaryImpact;
}

export interface ParsedAIResponse {
  // The validated response ready for frontend display
  displayContent: string;
  
  // Raw AI output before parsing
  rawAIOutput: string;
  
  // Parsed structured JSON data
  structuredData?: StructuredSummary;
  
  // Metadata about the response
  metadata: {
    isValid: boolean;
    hasStructuredOutput: boolean;
    parseErrors?: string[];
    tokensUsed?: number;
  };
}

export class AIResponseParser {
  /**
   * Parse AI response - now handles markdown output
   */
  parseResponse(rawResponse: string, tokensUsed?: number): ParsedAIResponse {
    const result: ParsedAIResponse = {
      displayContent: '',
      rawAIOutput: rawResponse,
      metadata: {
        isValid: false,
        hasStructuredOutput: false,
        parseErrors: [],
        tokensUsed,
      },
    };

    try {
      // Check if response is empty
      if (!rawResponse || rawResponse.trim().length === 0) {
        result.metadata.parseErrors?.push('Empty response from AI');
        result.displayContent = 'Error: No response from AI';
        return result;
      }

      // Normalize markdown by removing code fence wrappers if present
      const normalized = this.normalizeMarkdown(rawResponse);
      
      // Return markdown as-is for rendering
      result.displayContent = normalized;
      result.metadata.isValid = true;
      result.metadata.hasStructuredOutput = false; // No longer parsing JSON
      result.structuredData = undefined;

    } catch (error) {
      result.metadata.parseErrors?.push(
        error instanceof Error ? error.message : 'Unknown parsing error'
      );
      result.displayContent = this.formatFallback(rawResponse);
    }

    return result;
  }

  /**
   * Normalize markdown by extracting only Summary section content
   */
  private normalizeMarkdown(content: string): string {
    const trimmed = content.trim();
    
    // Remove code fence wrappers if present
    const markdownFenceRegex = /^```(?:markdown)?\s*\n([\s\S]*?)\n```$/;
    const fenceMatch = trimmed.match(markdownFenceRegex);
    const cleanContent = fenceMatch ? fenceMatch[1].trim() : trimmed;
    
    // Extract content from Summary section only
    const summaryMatch = cleanContent.match(/##\s*Summary\s*\n([\s\S]*?)(?=\n##|$)/i);
    if (summaryMatch && summaryMatch[1]) {
      return summaryMatch[1].trim();
    }
    
    // If no Summary section found, look for content after any heading
    const anyHeadingMatch = cleanContent.match(/##\s*[^\n]*\s*\n([\s\S]*)/i);
    if (anyHeadingMatch && anyHeadingMatch[1]) {
      return anyHeadingMatch[1].trim();
    }
    
    // Fallback: return content as-is but remove any leading commentary
    return cleanContent
      .replace(/^(okay let's|let me|here's|i'll|alright)\s*/i, '')
      .trim();
  }

  /**
   * Extract JSON from response (DEPRECATED - kept for compatibility)
   */
  private extractJSON(response: string): StructuredSummary | null {
    try {
      // Try to find JSON in markdown code blocks first
      const codeBlockMatch = response.match(/```(?:json)?\s*(\{[\s\S]*?\})\s*```/);
      if (codeBlockMatch) {
        return JSON.parse(codeBlockMatch[1]);
      }

      // Try to find raw JSON
      const jsonMatch = response.match(/\{[\s\S]*"overview"[\s\S]*\}/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]);
      }

      // Try parsing the entire response as JSON
      return JSON.parse(response.trim());
    } catch {
      return null;
    }
  }

  /**
   * Validate the JSON structure (DEPRECATED - kept for compatibility)
   */
  private validateStructure(data: any): string[] {
    const errors: string[] = [];

    // Check required top-level fields
    if (!data.overview) errors.push('Missing "overview" field');
    if (!data.files || !Array.isArray(data.files)) errors.push('Missing or invalid "files" array');
    if (!data.impact) errors.push('Missing "impact" field');

    // Validate overview
    if (data.overview) {
      if (!data.overview.summary) errors.push('Missing "overview.summary"');
      if (typeof data.overview.totalFiles !== 'number') errors.push('Invalid "overview.totalFiles"');
      if (!Array.isArray(data.overview.categories)) errors.push('Invalid "overview.categories"');
    }

    // Validate files array
    if (Array.isArray(data.files)) {
      data.files.forEach((file: any, index: number) => {
        if (!file.path) errors.push(`Missing "path" in files[${index}]`);
        if (!file.category) errors.push(`Missing "category" in files[${index}]`);
        if (!file.summary) errors.push(`Missing "summary" in files[${index}]`);
        if (!Array.isArray(file.keyChanges)) errors.push(`Invalid "keyChanges" in files[${index}]`);
        if (typeof file.linesAdded !== 'number') errors.push(`Invalid "linesAdded" in files[${index}]`);
        if (typeof file.linesDeleted !== 'number') errors.push(`Invalid "linesDeleted" in files[${index}]`);
      });
    }

    // Validate impact
    if (data.impact) {
      if (!['minor', 'moderate', 'major'].includes(data.impact.severity)) {
        errors.push('Invalid "impact.severity"');
      }
      if (!data.impact.description) errors.push('Missing "impact.description"');
      if (typeof data.impact.breaking !== 'boolean') errors.push('Invalid "impact.breaking"');
      if (!Array.isArray(data.impact.concerns)) errors.push('Invalid "impact.concerns"');
    }

    return errors;
  }

  /**
   * Format structured data for frontend display (DEPRECATED - kept for compatibility)
   */
  private formatStructuredData(data: StructuredSummary): string {
    let formatted = '';

    // Overview
    formatted += `**${data.overview.summary}**\n\n`;
    formatted += `**${data.overview.totalFiles} files** changed across categories: ${data.overview.categories.join(', ')}\n\n`;

    // Files
    formatted += `## Changes by File\n\n`;
    data.files.forEach(file => {
      formatted += `### ${file.path}\n`;
      formatted += `**${file.category}** | `;
      formatted += `+${file.linesAdded} −${file.linesDeleted}\n\n`;
      formatted += `${file.summary}\n\n`;
      if (file.keyChanges.length > 0) {
        formatted += `**Key changes:**\n`;
        file.keyChanges.forEach(change => {
          formatted += `• ${change}\n`;
        });
        formatted += '\n';
      }
    });

    // Impact
    formatted += `## Impact\n`;
    formatted += `**Severity:** ${data.impact.severity.toUpperCase()}`;
    if (data.impact.breaking) {
      formatted += ` - **BREAKING CHANGE**`;
    }
    formatted += `\n\n${data.impact.description}\n`;

    if (data.impact.concerns.length > 0) {
      formatted += `\n**Concerns:**\n`;
      data.impact.concerns.forEach(concern => {
        formatted += `• ${concern}\n`;
      });
    }

    return formatted.trim();
  }

  /**
   * Fallback formatting for error responses
   */
  private formatFallback(rawResponse: string): string {
    return `**Response Error**\n\nAn error occurred while processing the AI response. Raw output:\n\n${rawResponse}`;
  }

  /**
   * Validate that AI response meets minimum requirements
   */
  validateResponse(parsed: ParsedAIResponse): boolean {
    // Must have valid display content
    if (!parsed.metadata.isValid || !parsed.displayContent) {
      return false;
    }

    // Must not have critical parse errors
    if (parsed.metadata.parseErrors && parsed.metadata.parseErrors.length > 0) {
      return false;
    }

    // Display content must meet minimum length (at least some text)
    if (parsed.displayContent.trim().length < 10) {
      return false;
    }

    return true;
  }

  /**
   * Extract error message from failed response
   */
  extractErrorMessage(parsed: ParsedAIResponse): string {
    if (parsed.metadata.parseErrors && parsed.metadata.parseErrors.length > 0) {
      return parsed.metadata.parseErrors.join('; ');
    }

    if (!parsed.metadata.isValid) {
      return 'Invalid AI response';
    }

    return 'Unknown error';
  }
}
