# Python Multi-Module Project

A demonstration of Python module-based architecture that enables independent development teams to work on separate modules while maintaining clean integration.

## Project Structure

This project consists of two independent modules:

```
python-module-based/
├── child_library/          # Independent reusable module
│   ├── pyproject.toml     # Package configuration
│   ├── __init__.py        # Exports subtraction_router
│   ├── controllers/       # FastAPI route controllers
│   │   └── subtraction_controller.py
│   └── handlers/          # Business logic
│       └── math_handler.py
│
├── parent_module/         # Main application module
│   ├── pyproject.toml    # Package configuration with child_library dependency
│   ├── main.py           # FastAPI app entry point
│   ├── controllers/      # FastAPI route controllers
│   │   ├── health_controller.py
│   │   └── math_controller.py
│   └── handlers/         # Business logic
│       ├── health_handler.py
│       └── math_handler.py
└── README.md
```

## Architecture Overview

### Child Library (`child_library/`)
- **Purpose**: Independent, reusable module that can be developed separately
- **Exports**: `subtraction_router` - a FastAPI router for subtraction operations
- **Package Name**: `subtraction-module`
- **Key Features**:
  - Self-contained subtraction functionality
  - FastAPI router that can be integrated into any FastAPI application
  - Environment variable support via python-dotenv

### Parent Module (`parent_module/`)
- **Purpose**: Main FastAPI application that integrates child_library
- **Package Name**: `parent-module`
- **Key Features**:
  - Health check endpoint
  - Addition functionality (native to parent)
  - Subtraction functionality (imported from child_library)
  - Full FastAPI server with uvicorn

### How They Work Together

The [parent_module/main.py](parent_module/main.py) imports and uses the child library:

```python
from child_library import subtraction_router

app = FastAPI(title="Parent Module API", version="1.0.0")
app.include_router(subtraction_router, tags=["Math"])
```

This architecture allows:
- **Independent Development**: Teams can work on `child_library` and `parent_module` separately
- **Code Reusability**: The child library can be used in multiple parent applications
- **Clean Separation**: Each module has its own dependencies and configuration
- **Version Control**: Modules can be versioned independently

## Installation

### Prerequisites
- Python 3.13 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended)

### Installing uv

If you don't have `uv` installed:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via pip
pip install uv
```

### Step 1: Install Child Library

First, install the child library module dependencies:

```bash
cd child_library

# Sync dependencies and create virtual environment
uv sync

# This creates a .venv directory and installs all dependencies
```

### Step 2: Build Child Library (for parent module)

Build the distribution package that the parent module will use:

```bash
# Still in child_library directory
uv build

# This creates dist/subtraction_module-0.1.0.tar.gz
```

### Step 3: Install Parent Module

Install the parent module, which depends on the child library:

```bash
cd ../parent_module

# Sync dependencies (including child_library)
uv sync

# This automatically installs all dependencies including the child library
```

**Note**: The parent module's [pyproject.toml](parent_module/pyproject.toml) references the child library as a file dependency:
```toml
dependencies = [
    "subtraction-module @ file:///${PROJECT_ROOT}/../child_library/dist/subtraction_module-0.1.0.tar.gz",
]
```

### Development Mode Setup

For active development on both modules simultaneously:

```bash
# Install child library dependencies
cd child_library
uv sync

# Install parent module dependencies
cd ../parent_module
uv sync
```

With `uv sync`, dependencies are managed in isolated virtual environments (`.venv` directories) for each module. Changes to the source code in development mode are immediately reflected.

## Running the Application

### Start the FastAPI Server

```bash
cd parent_module

# Run with uv (uses the virtual environment automatically)
uv run python main.py

# Or activate the virtual environment first
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows
python main.py
```

The server will start on `http://0.0.0.0:8000`

### API Endpoints

Once running, you can access:

- **Health Check**: `GET /health` (from parent_module)
- **Addition**: `GET /add?a=10&b=5` (from parent_module)
- **Subtraction**: `GET /subtract?a=10&b=5` (from child_library)
- **API Docs**: `http://localhost:8000/docs` (Swagger UI)
- **ReDoc**: `http://localhost:8000/redoc`

### Example Requests

```bash
# Health check
curl http://localhost:8000/health

# Addition (parent module)
curl "http://localhost:8000/add?a=10&b=5"

# Subtraction (child library)
curl "http://localhost:8000/subtract?a=10&b=5"
```

## Environment Variables

Both modules support environment variables via `.env` files:

```bash
# Create .env file in project root or in each module
echo "TEST_KEY=your_test_value" > .env
```

The `TEST_KEY` variable is used for demonstration purposes in both modules.

## Development Workflow

### For Child Library Developers

1. Make changes in [child_library/](child_library/)
2. Test independently or rebuild distribution:
   ```bash
   cd child_library
   uv build
   ```
3. After building, update the parent module to pick up changes:
   ```bash
   cd ../parent_module
   uv sync --reinstall-package subtraction-module
   ```

### For Parent Module Developers

1. Make changes in [parent_module/](parent_module/)
2. Run the application to test:
   ```bash
   cd parent_module
   uv run python main.py
   ```
3. The child_library functionality is available via import

### Updating Dependencies

If child_library is updated and you need to reinstall:

```bash
# Rebuild child library
cd child_library
uv build

# Update parent module dependencies
cd ../parent_module
uv sync --reinstall-package subtraction-module
```

## Benefits of This Architecture

1. **Team Independence**: Separate teams can own and develop each module
2. **Clear Boundaries**: Well-defined interfaces between modules
3. **Reusability**: Child library can be used in multiple projects
4. **Testing**: Each module can be tested independently
5. **Version Management**: Independent versioning and release cycles
6. **Dependency Management**: Each module manages its own dependencies

## Troubleshooting

### Child library not found
```bash
# Ensure child library is built
cd child_library
uv build

# Check if distribution exists
ls dist/

# Sync parent module to install child library
cd ../parent_module
uv sync
```

### Import errors
```bash
# Reinstall parent module dependencies
cd parent_module
uv sync --reinstall

# Or reinstall specific package
uv sync --reinstall-package subtraction-module
```

### Virtual environment issues
```bash
# Remove and recreate virtual environment
cd parent_module  # or child_library
rm -rf .venv
uv sync
```

### Port already in use
```bash
# Change port in main.py or kill the process using port 8000
lsof -ti:8000 | xargs kill -9
```

### uv command not found
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via pip
pip install uv
```
