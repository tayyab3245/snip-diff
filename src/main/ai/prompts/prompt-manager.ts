/**
 * Prompt Manager
 * Manages system prompts and task-specific prompt templates
 */

import { AgentContext } from '../orchestrator';

export class PromptManager {
  /**
   * Get base system prompt for the AI agent
   */
  getSystemPrompt(): string {
    return `You are an expert code analysis assistant for SNIP-DIFF, a Git diff visualization tool.

Your role is to:
- Analyze code changes and provide insightful summaries
- Generate meaningful commit messages
- Explain complex diffs in simple terms
- Identify patterns and potential issues in changes
- Provide context-aware suggestions

Guidelines:
- Be concise and clear
- Focus on what changed and why it matters
- Use technical terms appropriately
- Highlight important changes
- Be objective and factual

You have access to:
- Repository file structure
- Git status and diffs
- Selected files and changes
- Conversation history`;
  }

  /**
   * Build task-specific prompt
   */
  buildTaskPrompt(task: string, context: AgentContext): string {
    switch (task) {
      case 'summarize_changes':
        return this.buildSummarizePrompt(context);
      case 'generate_commit_message':
        return this.buildCommitMessagePrompt(context);
      case 'explain_changes':
        return this.buildExplainPrompt(context);
      default:
        return `Task: ${task}\n\nContext: ${JSON.stringify(context, null, 2)}`;
    }
  }

  private buildSummarizePrompt(context: AgentContext): string {
    const filesCount = context.selectedFiles.length;
    const gitStatusSummary = this.summarizeGitStatus(context.gitStatus);

    return `Analyze the following repository changes and provide a comprehensive summary:

Repository: ${context.repoPath}
Files affected: ${filesCount}
Git Status:
${gitStatusSummary}

${context.diffContent ? `Diff Content:\n${context.diffContent}\n` : ''}

Please provide:
1. **Overview**: What changed overall?
2. **Key Changes**: Main modifications by category
3. **Impact**: Potential effects of these changes
4. **Concerns**: Any issues or risks to note

Keep it concise but informative.`;
  }

  private buildCommitMessagePrompt(context: AgentContext): string {
    const gitStatusSummary = this.summarizeGitStatus(context.gitStatus);

    return `Generate a conventional commit message for these changes:

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

  private buildExplainPrompt(context: AgentContext): string {
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
