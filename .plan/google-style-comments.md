# Objective
Add Google-style comments and docstrings to both the Python backend and TypeScript frontend codebases to improve code readability, API documentation, and maintainability.

# Scope & Impact
- **Python Backend (`backend/`)**: Update classes, methods, and functions across the backend modules (e.g., `precognito/api.py`, `precognito/auth.py`, `precognito/inventory/api.py`, `precognito/financial/services.py`, etc.) to use Google-style docstrings, including `Args:`, `Returns:`, and `Raises:` sections where applicable.
- **TypeScript Frontend (`frontend/src/`)**: Update classes, interfaces, React components, and utility functions to use JSDoc/TSDoc following Google style guidelines, describing parameters and return types.
- **Impact**: Enhances code self-documentation and developer experience without altering the runtime behavior of the system. This change touches a large surface area of files.

# Proposed Solution
Due to the large number of files that need repetitive updates (adding/modifying comments), this task is an ideal candidate for delegation to the `generalist` sub-agent. The agent will traverse the source directories and systematically enrich the code comments.

# Implementation Plan
1. **Phase 1: Python Backend Docstrings**
   - Use the `generalist` agent to process the `backend/precognito/` directory module by module.
   - For each Python file, identify classes and functions. Add or modify docstrings to strictly follow the Google Python Style Guide docstring format.
2. **Phase 2: TypeScript Frontend Comments**
   - Use the `generalist` agent to process the `frontend/src/` directory.
   - Add JSDoc/TSDoc comments describing React components, utility functions, interfaces, and hooks following the Google TypeScript Style Guide conventions.

# Verification
- Run tests (`pytest` for backend, `vitest`/`playwright` for frontend) to ensure no syntax errors were inadvertently introduced while modifying docstrings/comments.
- (Optional) Run `ruff` on the Python codebase to check for any basic formatting or syntax issues introduced. Run `eslint` or `tsc` on the frontend for similar checks.