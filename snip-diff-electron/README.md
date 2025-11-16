# SNIP-DIFF

AI workflow tool for preparing code context for LLMs.

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## Setup

Create `.env` file:
```env
GEMINI_API_KEY=your_api_key_here
```

Get API key: https://aistudio.google.com/app/apikey

## Project Structure

```
src/
├── main/       # Backend (Electron main process)
├── renderer/   # Frontend (React UI)
└── shared/     # Shared types & constants

config/         # Build configuration files
```

See [ARCHITECTURE.md](../ARCHITECTURE.md) for detailed documentation.

## Features

- 📁 Multi-file selection with click-to-toggle
- 🔍 Git-based diff detection
- 🤖 AI summarization (Gemini 1.5 Flash)
- 👁️ Live file watching with Chokidar
- 📋 Copy files/diffs to clipboard for LLM context

## Tech Stack

- **Desktop:** Electron 28
- **Frontend:** React 18 + TypeScript + Vite
- **Backend:** Node.js + TypeScript
- **State:** Zustand
- **Styling:** Framer Motion
