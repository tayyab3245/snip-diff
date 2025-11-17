## Design Philosophy

The AI system in SNIP-DIFF is intentionally designed around a simple, deterministic architecture. The core principle is straightforward: gather all necessary context upfront, then execute a single summarization operation when the user clicks the summarize button. This design choice eliminates complexity while ensuring consistent, reproducible results.

The AI operates in a completely stateless manner by design. There is no conversation memory, no tool execution, and no multi-turn interactions. Instead, the system follows a pre-gather and execute pattern. Before the AI ever receives a prompt, the main process collects everything needed: file contents, git diffs, repository structure, and change metadata. This comprehensive context gathering happens entirely outside the AI layer.

Once the user triggers summarization, the system packages all this pre-gathered context into the summarize.md template file. The template contains placeholders that get replaced with the actual file paths, diff content, and change statistics. The AI receives this fully-baked prompt with all context embedded directly in the markdown structure. There are no follow-up questions, no tool calls to fetch additional data, and no iterative refinement loops.

The AI's task is singular and well-defined: read the provided context and output a structured summary. Because the same input always produces the same output, summarization is deterministic and predictable. Users can re-run summarization on identical changes and expect consistent results.

After the AI generates its response, the system streams the output back to the user interface in real-time. The response parser validates the markdown output and extracts the summary content, which is then displayed in the chat panel. This streaming approach provides immediate feedback while maintaining the simplicity of the stateless architecture.

This design deliberately avoids the complexity of agentic AI systems with memory, tools, and planning capabilities. By keeping the AI purely functional - input goes in, summary comes out - the system remains predictable, debuggable, and maintainable. The stateless approach also prevents context pollution across different summarization sessions and eliminates the need for complex state management.



# Current Implementation Structure

```
ai/
├── index.ts                    # Main export file - central hub for all AI components
├── initializer.ts              # AI system initialization and provider management
├── orchestrator.ts             # Main AI coordinator for stateless operations
├── verify-providers.ts         # Provider verification and testing utilities
├── parsing/                    # AI response parsing and validation
│   ├── ai-response-parser.ts   # Markdown response parser with fallback handling
│   └── index.ts                # Parsing exports
├── prompts/                    # Prompt template management
│   ├── index.ts                # Prompt exports
│   ├── prompt-builder.ts       # Template loading and variable substitution
│   └── summarize.md            # Summarize prompt template
├── providers/                  # LLM provider implementations
│   ├── base-provider.ts        # Abstract BaseLLMProvider class
│   ├── gemini-provider.ts      # Google Gemini API integration
│   ├── anthropic-provider.ts   # Anthropic Claude API integration
│   ├── openai-provider.ts      # OpenAI GPT API integration
│   └── index.ts                # Provider exports
└── utils/                      # AI utility functions
    └── index.ts                # Helper functions (token estimation, text processing)
```

## Core Components

### AI Initializer

The AI Initializer manages the entire lifecycle of the AI system using a singleton pattern. A single instance controls all provider management, currently supporting Google Gemini with OpenAI and Anthropic implementations ready for use. It handles critical configuration aspects including API keys, model selection, temperature settings, and token limits. Upon initialization, the system validates the provided API key to ensure connectivity before allowing any operations.

### AI Orchestrator

The AI Orchestrator serves as a stateless coordinator for all AI operations. It operates on a single-turn basis without maintaining conversation history, instead relying on an AgentContext object that contains all necessary information for each operation. The orchestrator integrates tightly with the AIResponseParser to validate and format responses, implementing comprehensive error handling to catch and report issues throughout the processing pipeline.

### Provider System

The provider system implements a multi-provider architecture through abstraction. The BaseLLMProvider abstract class defines a unified interface that all providers must implement. Currently, three providers are available: GeminiProvider for Google Gemini 2.0 Flash (the primary provider), AnthropicProvider for Claude 3.5 Sonnet, and OpenAIProvider for GPT-4o. Each provider implements both complete and stream methods while maintaining type safety through strong TypeScript interfaces.

### Response Parser

The Response Parser handles all AI output processing and validation. It specializes in extracting meaningful content from markdown-formatted AI responses while providing fallback mechanisms for malformed outputs. Although it maintains legacy JSON parsing support, this functionality is deprecated in favor of the current markdown approach. The parser validates responses against minimum quality standards to ensure reliable output for the frontend.

### Prompt Builder

The Prompt Builder constructs prompts using a template-based system. It loads markdown template files from the prompts directory and performs variable substitution by replacing placeholders with actual values from the context. Templates are cached in memory for performance optimization, and the builder seamlessly integrates repository data with template structure to create complete prompts.

### Utilities

The utilities module provides essential helper functions that support AI operations throughout the system. It offers rough token counting for estimating API usage, text processing capabilities including truncation and sanitization, code block extraction from AI responses, and context summarization for file changes and metadata.







