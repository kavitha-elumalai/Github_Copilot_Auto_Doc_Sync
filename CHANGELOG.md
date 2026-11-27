# Changelog

## [0.1.0] - Automated Documentation Sync

### Added
- A Python CLI that scans Python and Robot Framework repositories and generates `PROJECT_DOCS.md`.
- Local and GitHub pull-request input resolution, with bounded retries, safe temporary workspaces, and repository validation.
- Secret redaction and environment-file sanitization, including protection against leaking values through generated documentation, logs, or errors.
- Static Python and Robot Framework parsers, deterministic Markdown rendering, IST timestamps, and atomic output writing.
- A Git `post-merge` hook template and GitHub Actions workflow for documentation synchronization after a pull request is merged.
- Unit and end-to-end coverage for parsing, redaction, deterministic output, empty repositories, and failure handling.

### Changed
- CLI diagnostics, parser deadlines, GitHub output requirements, dependency locks, and workflow installation were updated based on code-review findings.
- Requirements, architecture, README, and the code-review report were updated to reflect the implemented behavior and approved mitigations.

### Verification
- `pytest -v`: 91 passed, 1 skipped (symlink creation is not supported in this environment).
- `uv build`: previously completed successfully for both the source distribution and wheel.
