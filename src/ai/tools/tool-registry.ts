/**
 * Tool Registry
 * Manages available tools that the AI agent can use
 */

export interface Tool {
  name: string;
  description: string;
  parameters: Record<string, unknown>;
  execute: (args: Record<string, unknown>) => Promise<unknown>;
}

export class ToolRegistry {
  private tools: Map<string, Tool> = new Map();

  /**
   * Register a new tool
   */
  register(tool: Tool): void {
    this.tools.set(tool.name, tool);
    console.log(`[AI Tools] Registered tool: ${tool.name}`);
  }

  /**
   * Unregister a tool
   */
  unregister(toolName: string): void {
    this.tools.delete(toolName);
    console.log(`[AI Tools] Unregistered tool: ${toolName}`);
  }

  /**
   * Get a tool by name
   */
  getTool(toolName: string): Tool | undefined {
    return this.tools.get(toolName);
  }

  /**
   * Execute a tool
   */
  async execute(toolName: string, args: Record<string, unknown>): Promise<unknown> {
    const tool = this.tools.get(toolName);
    if (!tool) {
      throw new Error(`Tool not found: ${toolName}`);
    }

    console.log(`[AI Tools] Executing tool: ${toolName}`);
    return tool.execute(args);
  }

  /**
   * Get all registered tools
   */
  getAllTools(): Tool[] {
    return Array.from(this.tools.values());
  }

  /**
   * Get tool definitions for LLM
   */
  getToolDefinitions(): Array<{ name: string; description: string; parameters: Record<string, unknown> }> {
    return this.getAllTools().map(tool => ({
      name: tool.name,
      description: tool.description,
      parameters: tool.parameters,
    }));
  }
}
