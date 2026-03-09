# Contributing to Unbiased India News

First of all, thank you for considering contributing to Unbiased India News. It's people like you that make this tool better for everyone.

## Development Standards

To maintain the quality and consistency of the project, please adhere to the following standards:

1. **Modular Architecture:** Ensure all new features are decoupled and follow the established Service-Node-Orchestrator pattern.
2. **Asynchronous Code:** All I/O-bound operations must use `asyncio` and `aiohttp`.
3. **Type Hinting:** Use strict Python type hints for all function signatures and class attributes.
4. **Documentation:** Provide Google-style docstrings for all new modules, classes, and methods.
5. **No Emojis:** Keep documentation and commit messages professional and emoji-free.

## Pull Request Process

1. Fork the repository and create your branch from `main`.
2. If you've added code that should be tested, add unit tests in the `tests/unit` directory.
3. Ensure the test suite passes (`pytest tests/unit`).
4. Update the `Roadmap.md` if your contribution completes a planned milestone.
5. Issue the pull request with a descriptive title and a clear summary of changes.

## Reporting Issues

* Check if the issue has already been reported.
* Use a clear and descriptive title.
* Describe the exact steps which reproduce the problem.
* Include logs from `logs/pipeline.log` if relevant.

---
*By contributing, you agree that your contributions will be licensed under its MIT License.*
