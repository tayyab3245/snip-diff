# SNIP-DIFF Architecture

## Overview

SNIP-DIFF is a desktop application that helps developers work with code files and Git diffs. It provides an intuitive interface for browsing files, viewing differences, and preparing code snippets for AI assistants.

## System Components

### Desktop Application
A cross-platform Electron app that runs on Windows, macOS, and Linux.

### File Browser
Navigate and select files from your local file system with a tree view interface.

### Git Integration
Automatically detect Git repositories and show file changes with diff visualization.

### AI Summarization
Generate concise summaries of code files and diffs using Google Gemini AI.

### Code Snippet Management
Copy selected files or diffs to clipboard for easy sharing with AI assistants.

## Technology Stack

Desktop Framework: Electron
Frontend: React with TypeScript
Backend: Node.js with TypeScript
AI: Google Gemini
Version Control: Git
Build Tool: Vite

## Key Features

### File Operations
Browse local file systems, select multiple files, view file contents, and copy files to clipboard.

### Git Integration
Auto-detect Git repositories, show modified files, display diff views, and track file changes in real-time.

### AI Assistance
Summarize code files, explain code changes, generate documentation, and optimize code snippets.

### User Interface
Dark theme design, responsive layout, custom window controls, and intuitive navigation.

## Data Flow

User browses and selects files through the tree interface. Application reads file contents and Git status. Selected content is sent to Gemini AI for summarization. Summaries and snippets are formatted for clipboard.

## Use Cases

Code Review: Quickly understand changes in pull requests.
Documentation: Generate summaries of complex codebases.
AI Prompting: Prepare optimized code snippets for LLM conversations.
Learning: Explore unfamiliar codebases with AI explanations.

## Environment Requirements

Node.js 18+, Git (for repository features), and Google Gemini API key (for AI features).

## Distribution

Available as native desktop applications for Windows (.exe installer), macOS (.dmg), and Linux (.AppImage).

---