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

    // Diff content is provided by git service via main process
    const diffContent = context.diffContent || 'No diff content available';

    // Render the template with variables
    return this.renderTemplate(template, {
      FILE_COUNT: context.selectedFiles.length.toString(),
      FILE_PATHS: filePaths,
      DIFF_CONTENT: diffContent,
      REPO_PATH: context.repoPath,
    });
  }

  /**
   * Build a complete prompt for generating commit messages
   */
  buildCommitPrompt(context: AgentContext, _conversationHistory: Message[]): string {
    const template = this.loadTemplate('commit');
    
    if (!template) {
      // Fallback inline prompt
      return this.buildCommitFallback(context);
    }

    const filePaths = context.selectedFiles.length > 0
      ? context.selectedFiles.map(f => `- ${f}`).join('\n')
      : 'No files selected';

    return this.renderTemplate(template, {
      FILE_COUNT: context.selectedFiles.length.toString(),
      FILE_PATHS: filePaths,
      DIFF_CONTENT: context.diffContent || 'No diff content available',
      REPO_PATH: context.repoPath,
    });
  }

  /**
   * Build a complete prompt for explaining changes
   */
  buildExplainPrompt(context: AgentContext, _conversationHistory: Message[]): string {
    const template = this.loadTemplate('explain');
    
    if (!template) {
      // Fallback inline prompt
      return this.buildExplainFallback(context);
    }

    const filePaths = context.selectedFiles.length > 0
      ? context.selectedFiles.map(f => `- ${f}`).join('\n')
      : 'No files selected';

    return this.renderTemplate(template, {
      FILE_COUNT: context.selectedFiles.length.toString(),
      FILE_PATHS: filePaths,
      DIFF_CONTENT: context.diffContent || 'No diff content available',
      REPO_PATH: context.repoPath,
    });
  }

  /**
   * Fallback commit message prompt (inline)
   */
  private buildCommitFallback(context: AgentContext): string {
    const gitStatusSummary = this.summarizeGitStatus(context.gitStatus);

    return `Generate a conventional commit message for these changes:

Repository: ${context.repoPath}
Files affected:
${gitStatusSummary}

${context.diffContent ? `Changes:\n${context.diffContent}\n` : ''}

Format:
<type>(<scope>): <subject>

<body>

<footer>

Types: feat, fix, docs, style, refactor, test, chore
Keep subject under 50 chars, body under 72 chars per line.`;
  }

  /**
   * Fallback explain prompt (inline)
   */
  private buildExplainFallback(context: AgentContext): string {
    return `Explain the following code changes in detail:

Repository: ${context.repoPath}
Selected files: ${context.selectedFiles.join(', ')}

${context.diffContent || 'No diff content available'}

Please explain:
1. What was changed
2. Why it might have been changed
3. How it affects the codebase
4. Any notable patterns or techniques used`;
  }

  /**
   * Summarize Git status for fallback prompts
   */
  private summarizeGitStatus(gitStatus: Map<string, string>): string {
    const statusGroups: Record<string, string[]> = {
      Modified: [],
      Added: [],
      Deleted: [],
      Renamed: [],
      Untracked: [],
    };

    gitStatus.forEach((status, path) => {
      if (statusGroups[status]) {
        statusGroups[status].push(path);
      }
    });

    const lines: string[] = [];
    Object.entries(statusGroups).forEach(([status, files]) => {
      if (files.length > 0) {
        lines.push(`${status}: ${files.length} file(s)`);
        files.slice(0, 5).forEach(file => lines.push(`  - ${file}`));
        if (files.length > 5) {
          lines.push(`  ... and ${files.length - 5} more`);
        }
      }
    });

    return lines.join('\n');
  }
}
