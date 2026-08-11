# OCR Pipeline Spec Kit

## Purpose
This document defines the implementation plan, rules, best practices, and conventions for the ocr_pipeline repository. It ensures that the project is consistent, maintainable, and easy to extend.

## Project Goals
- Provide a lightweight Python OCR pipeline for images and multi-page PDFs.
- Integrate with Baidu Unlimited-OCR as the initial backend.
- Support JSON and CSV output.
- Offer a CLI entrypoint and a reusable Python API.
- Keep the architecture pluggable for future OCR backends.

## Architecture
- `src/ocr_pipeline/io.py`: input handling for images and PDF rasterization.
- `src/ocr_pipeline/preprocess.py`: image preprocessing operations.
- `src/ocr_pipeline/backend.py`: abstract OCR backend API and Baidu implementation.
- `src/ocr_pipeline/export.py`: result serialization to JSON/CSV.
- `src/ocr_pipeline/cli.py`: command-line entrypoint for batch processing.

## Coding Rules
- Use Python 3.11+ compatibility.
- Keep functions small and testable.
- Validate external inputs early.
- Prefer explicit error handling and logging over silent failures.
- Do not hardcode API keys; use environment variables or configuration.

## Testing
- Add unit tests for each module.
- Mock external OCR calls where possible.
- Include at least one integration-style test for end-to-end flow.
- Keep tests isolated and reproducible.

## Documentation
- `README.md` must include installation, usage examples, and architecture notes.
- Document environment variables and backend configuration.
- Include a developer section for running tests and adding new backends.

## Contribution Guidelines
- Open PRs against `main` with clear descriptions.
- Add tests for every new feature.
- Keep changes small and focused.

## Release / Versioning
- Use semantic versioning if releasing packages.
- Document breaking changes in the README or changelog.

## Workflow
1. Scaffold package structure.
2. Implement MVP features.
3. Add tests and docs.
4. Validate on sample inputs.
5. Iterate with improvements.
