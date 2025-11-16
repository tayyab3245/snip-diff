/**
 * Prompt Builder
 * Builds complete prompts by loading templates and combining with context data
 * Context data (diffs, file contents) is provided by main process services
 */

import * as fs from 'fs';
import * as path from 'path';
import { AgentContext } from '../orchestrator';
import { Message } from '../providers';

export class PromptBuilder {
  private promptsDir: string;
  private templateCache: Map<string, string> = new Map();

  constructor() {
    // Prompts are in src/ai/prompts/
    // After compilation, __dirname is dist/ai/prompts, go back to project root then into src
    this.promptsDir = path.join(__dirname, '..', '..', '..', '..', 'src', 'ai', 'prompts');
    console.log('[PromptBuilder] __dirname:', __dirname);
    console.log('[PromptBuilder] Prompts directory:', this.promptsDir);
  }

  /**
   * Load a prompt template from a markdown file
   */
  private loadTemplate(name: string): string {
    // Check cache first
    if (this.templateCache.has(name)) {
      console.log('[PromptBuilder] Loading template from cache:', name);
      return this.templateCache.get(name)!;
    }

    // Load from file
    const filePath = path.join(this.promptsDir, `${name}.md`);
    console.log('[PromptBuilder] Loading template from file:', filePath);
    
    if (!fs.existsSync(filePath)) {
      console.error('[PromptBuilder] Template not found:', filePath);
      throw new Error(`Prompt template not found: ${name}.md`);
    }

    const template = fs.readFileSync(filePath, 'utf-8');
    
    // Cache it
    this.templateCache.set(name, template);
    
    return template;
  }

  /**
   * Render a template with variables
   * Replaces {{VARIABLE_NAME}} with values from the variables object
   */
  private renderTemplate(template: string, variables: Record<string, any>): string {
    let rendered = template;

    for (const [key, value] of Object.entries(variables)) {
      const placeholder = `{{${key}}}`;
      const replacement = String(value);
      rendered = rendered.split(placeholder).join(replacement);
    }

    return rendered;
  }

  /**
   * Build a complete prompt for summarizing changes
   */
  buildSummarizePrompt(context: AgentContext, _conversationHistory: Message[]): string {
    const template = this.loadTemplate('summarize');
    
    if (!template) {
      throw new Error('Summarize prompt template not found');
    }

    // Build file paths list
    const filePaths = context.selectedFiles.length > 0
      ? context.selectedFiles.map(f => `- ${f}`).join('\n')
      : 'No files selected';

    // Get diff content or file contents
    let diffContent = '';
    
    if (context.diffContent) {
      // We have git diff content
      diffContent = context.diffContent;
    } else if (context.fileContents) {
      // We have full file contents (no git diff available)
      diffContent = Array.from(context.fileContents.entries())
        .map(([path, content]) => `=== ${path} ===\n${content}`)
        .join('\n\n');
    } else {
      diffContent = 'No content available';
    }

    // Render the template with variables
    return this.renderTemplate(template, {
      FILE_COUNT: context.selectedFiles.length.toString(),
      FILE_PATHS: filePaths,
      DIFF_CONTENT: diffContent,
    });
  }


}
