# SNIP-DIFF Electron Frontend

Modern Electron + React + TypeScript frontend for SNIP-DIFF file comparison tool.

## Features

- **Modern UI**: React 18 with TypeScript and neumorphic design
- **File Tree**: Interactive file browser with selection
- **Real-time Diff**: Live diff visualization with API backend
- **Cross-platform**: Windows, macOS, Linux support
- **Frameless Window**: Custom title bar with window controls

## Setup

1. **Install Dependencies**
```bash
cd snip-diff-electron
npm install
```

2. **Development Mode**
```bash
# Start both renderer and main processes
npm run dev

# Or start individually:
npm run dev:renderer  # Vite dev server
npm run dev:main      # Compile and run Electron
```

3. **Build for Production**
```bash
npm run build        # Build both renderer and main
npm run dist         # Create distributable packages
```

## Project Structure

```
src/
├── main/              # Electron main process
│   ├── main.ts       # Entry point & window management
│   └── preload.ts    # IPC bridge (secure)
├── renderer/         # React frontend
│   ├── components/   # UI components
│   ├── hooks/        # Custom React hooks
│   ├── store/        # State management (Zustand)
│   ├── App.tsx       # Main app component
│   └── main.tsx      # React entry point
└── shared/           # Shared types & constants
    ├── types.ts      # TypeScript definitions
    └── constants.ts  # App constants
```

## Architecture

### Main Process (Electron)
- Window management and lifecycle
- FastAPI backend integration
- IPC handlers for secure communication
- File system access (dialogs)

### Renderer Process (React)
- Modern React 18 with hooks
- Zustand for state management
- Styled Components for neumorphic design
- TypeScript for type safety

### IPC Bridge (Preload)
- Secure communication between main and renderer
- Exposes limited API via `window.electronAPI`
- Context isolation enabled for security

## API Integration

The frontend communicates with the FastAPI backend via:

1. **File Operations**: Browse project files and directories
2. **Diff Scanning**: Start background diff operations
3. **Real-time Updates**: Poll scan status and retrieve results

## Development Notes

- **Security**: `nodeIntegration: false` and `contextIsolation: true`
- **Performance**: Lazy loading and efficient state updates
- **UX**: Smooth animations and responsive design
- **Testing**: Component tests with React Testing Library

## Distribution

The app can be packaged for multiple platforms:

```bash
npm run dist:win     # Windows (NSIS installer)
npm run dist:mac     # macOS (DMG)
npm run dist:linux   # Linux (AppImage)
```

## Technology Stack

- **Electron**: Desktop app framework
- **React 18**: UI library with modern hooks
- **TypeScript**: Type safety and better DX  
- **Styled Components**: CSS-in-JS with neumorphic design
- **Zustand**: Lightweight state management
- **Vite**: Fast build tool and dev server
