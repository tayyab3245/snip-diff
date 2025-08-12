# SNIP-DIFF FastAPI Backend

A modern FastAPI backend that exposes the core SNIP-DIFF functionality as RESTful APIs.

## Setup

1. **Install Dependencies**
```bash
cd snip-diff-api
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux  
source venv/bin/activate

pip install -r requirements.txt
```

2. **Run Development Server**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

3. **View API Documentation**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
snip-diff-api/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── files.py     # File operations endpoints
│   │       └── diff.py      # Diff and scan endpoints
│   ├── core/                # Extracted business logic
│   │   ├── __init__.py
│   │   ├── diff_engine.py   # Core diff functionality
│   │   ├── cached_diff_engine.py
│   │   ├── snapshot.py      # File snapshot utilities
│   │   └── fast_diff_worker.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py      # Configuration
│   └── utils/
│       ├── __init__.py
│       └── helpers.py       # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_files.py        # File endpoint tests
│   └── test_diff.py         # Diff endpoint tests
├── requirements.txt
└── README.md
```

## API Endpoints

### Files
- `GET /api/files/tree?path=<path>` - Get file tree structure
- `POST /api/files/validate` - Validate file paths

### Diff Operations
- `POST /api/diff/scan` - Start diff scan operation
- `GET /api/diff/results/{scan_id}` - Get scan results
- `GET /api/diff/status/{scan_id}` - Get scan status

## Development

The backend extracts and exposes the existing Python core logic from the original SNIP-DIFF desktop application:

- **Core Business Logic**: Imported from `../nip/core/` modules
- **RESTful APIs**: Clean HTTP interface for frontend consumption
- **CORS Enabled**: Allows Electron frontend communication
- **Type Safety**: Full Pydantic models and FastAPI type hints
