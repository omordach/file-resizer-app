# Project Structure

## Root Layout

```
/
├── backend/           # FastAPI backend application
├── frontend/          # React frontend application
├── docker-compose.yml # Multi-container orchestration
└── README.md          # Project documentation
```

## Backend Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py         # FastAPI app, routes, middleware setup
│   ├── rate_limit.py   # Rate limiting middleware
│   └── utils.py        # File processing utilities
├── tests/
│   ├── assets/         # Test fixtures (images, PDFs)
│   ├── test_app.py     # API endpoint tests
│   ├── test_rate_limit.py
│   └── test_utils.py
├── Dockerfile          # Multi-stage build (frontend + backend)
└── requirements.txt    # Python dependencies
```

### Backend Conventions

- **Entry point**: `app/main.py` defines the FastAPI app instance
- **Static files**: Mounted at root `/` serving frontend build
- **API routes**: Prefixed with `/api/` (e.g., `/api/process`)
- **Middleware**: Applied globally via `app.middleware("http")`
- **Error handling**: Global exception handler for unhandled errors
- **Environment**: Use `python-dotenv` for configuration
- **Testing**: pytest with FastAPI TestClient

## Frontend Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── FileResizerForm.jsx  # Main form component
│   │   └── ui/                  # Reusable UI components (shadcn/ui style)
│   ├── lib/
│   │   └── utils.js             # Utility functions (cn helper)
│   ├── App.jsx                  # Root component
│   ├── main.jsx                 # React entry point
│   └── index.css                # Global styles with Tailwind directives
├── tests/
│   ├── e2e.spec.mjs             # Playwright E2E tests
│   └── test-image.png           # Test fixtures
├── public/                      # Static assets (icons, manifest)
├── dist/                        # Build output (gitignored)
├── index.html                   # HTML entry point
├── vite.config.js               # Vite configuration
├── tailwind.config.js           # Tailwind configuration
├── components.json              # shadcn/ui configuration
└── package.json
```

### Frontend Conventions

- **Component style**: Functional components with hooks
- **Imports**: Use `@/` alias for src directory imports
- **UI components**: Located in `src/components/ui/`, follow shadcn/ui patterns
- **Styling**: TailwindCSS utility classes, use `cn()` helper for conditional classes
- **File structure**: Feature-based components in `src/components/`
- **Testing**: Playwright for E2E, tests in `tests/` directory

## Docker Architecture

- **Multi-stage build**: Stage 1 builds frontend, Stage 2 builds backend and copies frontend dist
- **Static serving**: Backend serves frontend build from `./static` directory in container
- **Port**: Exposes 8080 for both API and frontend
- **Dependencies**: ImageMagick and Ghostscript installed in backend container

## Key Patterns

- **Monorepo structure**: Frontend and backend in separate directories at root level
- **Single container deployment**: Frontend built and served by backend in production
- **Environment-based paths**: Static file paths differ between local dev and Docker
- **Test assets**: Stored in respective `tests/assets/` directories
- **Configuration files**: At root of each application directory (frontend/, backend/)
