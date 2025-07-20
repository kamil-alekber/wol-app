# Contributing to Wake-On-LAN Web Application

Thank you for your interest in contributing to the Wake-On-LAN Web Application! We welcome contributions from everyone.

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct. Please be respectful and constructive in all interactions.

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check the existing issues to see if the problem has already been reported. When you create a bug report, please include as many details as possible:

- Use a clear and descriptive title
- Describe the exact steps to reproduce the problem
- Provide specific examples to demonstrate the steps
- Describe the behavior you observed and what behavior you expected
- Include screenshots if applicable
- Include your environment details (OS, Python version, browser, etc.)

### Suggesting Enhancements

Enhancement suggestions are welcome! Please provide:

- A clear and descriptive title
- A detailed description of the proposed enhancement
- Explain why this enhancement would be useful
- Provide examples of how the enhancement would work

### Pull Requests

1. **Fork** the repository
2. **Create** a new branch from `main` for your feature or bug fix
3. **Make** your changes
4. **Add** or update tests as needed
5. **Ensure** all tests pass
6. **Update** documentation if necessary
7. **Commit** your changes with clear, descriptive commit messages
8. **Push** to your fork
9. **Submit** a pull request

#### Pull Request Guidelines

- Follow the existing code style
- Write clear, concise commit messages
- Include tests for new functionality
- Update documentation as needed
- Ensure CI/CD checks pass
- Link to any relevant issues

## Development Setup

1. **Clone** your fork of the repository
2. **Install** Python 3.8+ and required system dependencies:
   ```bash
   # macOS
   brew install wakeonlan
   
   # Ubuntu/Debian
   sudo apt-get install wakeonlan
   ```
3. **Create** a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install** dependencies:
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov flake8 black isort  # For development
   ```
5. **Copy** the configuration file:
   ```bash
   cp config.example.json config.json
   ```

## Code Style

- Follow PEP 8 style guidelines
- Use `black` for code formatting: `black .`
- Use `isort` for import sorting: `isort .`
- Use `flake8` for linting: `flake8 .`
- Write docstrings for all functions and classes
- Use type hints where appropriate

## Testing

- Write tests for all new functionality
- Ensure all existing tests continue to pass
- Run tests with: `pytest`
- Check coverage with: `pytest --cov=.`

## Documentation

- Update the README.md if you change functionality
- Add docstrings to new functions and classes
- Comment complex code sections

## Commit Message Guidelines

Use clear and meaningful commit messages:

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

Examples:
```
Add device auto-discovery feature

Implements network scanning to automatically detect WOL-capable devices.
Fixes #123
```

## Release Process

1. Version numbers follow [Semantic Versioning](https://semver.org/)
2. Update version in relevant files
3. Update CHANGELOG.md
4. Create a new release on GitHub

## Questions?

If you have questions about contributing, please:

1. Check the existing documentation
2. Search through existing issues
3. Create a new issue with the "question" label

Thank you for contributing!
