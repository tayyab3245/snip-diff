# AI System Architecture

This directory contains the complete AI agent system for SNIP-DIFF.

## Structure

```
ai/
├── index.ts                 # Main export file
├── initializer.ts           # AI system initialization
├── orchestrator.ts          # Main AI coordinator
├── providers/               # LLM provider implementations
│   ├── base-provider.ts     # Abstract base class
│   ├── openai-provider.ts   # OpenAI (GPT-4, etc.)
│   ├── anthropic-provider.ts # Anthropic (Claude 3)
│   └── index.ts
├── prompts/                 # Prompt templates and management
│   ├── prompt-manager.ts    # Prompt builder and manager
│   └── index.ts
├── tools/                   # AI agent tools
│   ├── tool-registry.ts     # Tool management system
│   ├── file-analysis-tool.ts # File analysis tool
│   └── index.ts
├── services/                # AI services (future)
│   └── index.ts
├── memory/                  # Conversation memory management
│   ├── memory-manager.ts    # Memory system
│   └── index.ts
└── utils/                   # AI utilities
    └── index.ts             # Helper functions
```

## Usage

### 1. Initialize AI System

```typescript
import { aiInitializer } from './ai';

await aiInitializer.initialize({
  provider: 'gemini',  // or 'openai', 'anthropic'
  apiKey: process.env.GEMINI_API_KEY,
  model: 'gemini-pro',
  temperature: 0.7,
  maxTokens: 2000,
});
```

### 2. Use AI Orchestrator

```typescript
import { aiOrchestrator, AgentContext } from './ai';

const context: AgentContext = {
  repoPath: '/path/to/repo',
  selectedFiles: ['src/file1.ts', 'src/file2.ts'],
  gitStatus: new Map([
    ['src/file1.ts', 'Modified'],
    ['src/file2.ts', 'Added'],
  ]),
  diffContent: '... diff content ...',
};

// Summarize changes
const response = await aiOrchestrator.summarizeChanges(context);
console.log(response.content);

// Generate commit message
const commitMsg = await aiOrchestrator.generateCommitMessage(context);
console.log(commitMsg.content);
```

### 3. Direct Provider Usage

```typescript
import { OpenAIProvider } from './ai/providers';

const provider = new OpenAIProvider(apiKey, 'gpt-4-turbo-preview');

const response = await provider.complete([
  { role: 'system', content: 'You are a helpful assistant.' },
  { role: 'user', content: 'Explain this code change...' },
]);

console.log(response.content);
```

## Components

### Providers
- **BaseLLMProvider**: Abstract base class for all LLM providers
- **OpenAIProvider**: OpenAI API integration (GPT-4, GPT-3.5)
- **AnthropicProvider**: Anthropic API integration (Claude 3)
- **GeminiProvider**: Google Gemini API integration (Gemini Pro, Gemini Ultra)

### Orchestrator
Main coordinator that:
- Manages conversation flow
- Builds prompts with context
- Executes tools
- Manages memory
- Coordinates between components

### Memory Manager
- Stores conversation history
- Manages context window
- Provides recent messages for continuity
- Tracks token usage

### Tool Registry
- Registers available tools
- Executes tool functions
- Provides tool definitions to LLM

### Prompt Manager
- System prompts
- Task-specific prompt templates
- Context building
- Git status formatting

### Utilities
- Token estimation
- Text truncation
- Code formatting
- Response parsing

## Environment Variables

Create a `.env` file:

```env
# OpenAI
OPENAI_API_KEY=sk-...

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Google Gemini
GEMINI_API_KEY=...

# Default provider
AI_PROVIDER=gemini
AI_MODEL=gemini-pro
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=2000
```

## Future Enhancements

- [ ] Streaming responses
- [ ] Function calling / tool use
- [ ] Multi-turn conversations
- [ ] Conversation summarization
- [ ] Code review service
- [ ] Documentation generation
- [ ] Advanced context management
- [ ] Local model support (Ollama)
- [ ] Response caching
- [ ] Rate limiting
- [ ] Cost tracking
