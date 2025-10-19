# Contributing to DATA2410 Lab 2

Thank you for considering contributing to this project! This document provides guidelines and information for contributors.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Setup](#development-setup)
3. [Making Changes](#making-changes)
4. [Code Quality](#code-quality)
5. [GitHub Workflows](#github-workflows)
6. [Pull Request Process](#pull-request-process)

## Getting Started

Before you begin:

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/DATA2410-Lab2.git
   cd DATA2410-Lab2
   ```
3. Create a new branch for your work:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Requirements

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies (if any):
   ```bash
   pip install -r requirements.txt  # If requirements.txt exists
   ```

3. Install development tools:
   ```bash
   pip install flake8 black isort pylint pytest
   ```

## Making Changes

### Code Style

This project follows Python PEP 8 style guidelines. Please ensure your code:

- Uses meaningful variable and function names
- Includes docstrings for functions and classes
- Has proper indentation (4 spaces)
- Follows naming conventions:
  - Functions and variables: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_SNAKE_CASE`

### Testing

Before submitting changes:

1. Test your code manually:
   ```bash
   # For server
   python server.py
   
   # For client
   python client.py
   
   # For GUI client
   python client_gui.py
   ```

2. If you add new features, consider adding tests

### Documentation

- Update relevant documentation if you change functionality
- Add comments for complex logic
- Update README.md if you add new features
- Include docstrings for new functions/classes

## Code Quality

We use automated tools to maintain code quality. Before submitting a pull request, run:

### Linting

```bash
# Check for syntax errors and style issues
flake8 . --max-line-length=120

# Check code formatting
black --check --line-length=120 .

# Check import ordering
isort --check-only --profile black .
```

### Auto-formatting

You can automatically format your code:

```bash
# Format code with Black
black --line-length=120 .

# Sort imports
isort --profile black .
```

### Type Checking (Optional)

```bash
mypy *.py --ignore-missing-imports
```

## GitHub Workflows

This repository uses GitHub Actions for automated testing and code quality checks.

### Understanding Workflows

When you create a pull request, automated workflows will:

1. **Python CI**: Test your code against multiple Python versions
2. **Code Quality**: Run linting, formatting checks, and security scans

See [GITHUB_WORKFLOWS.md](GITHUB_WORKFLOWS.md) for detailed information about our workflow system.

### Workflow Status

- ✅ All checks must pass before your PR can be merged
- ❌ If checks fail, review the logs and fix the issues
- ⚠️ Some checks may allow warnings but should be addressed

### Running Workflows Locally

To test workflows before pushing:

1. Install [act](https://github.com/nektos/act):
   ```bash
   curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
   ```

2. Run workflows locally:
   ```bash
   # Run all workflows
   act
   
   # Run specific workflow
   act -j test
   ```

## Pull Request Process

### Before Submitting

1. Ensure all code quality checks pass
2. Test your changes thoroughly
3. Update documentation if needed
4. Commit your changes with clear messages:
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

### Creating a Pull Request

1. Go to the original repository on GitHub
2. Click "New Pull Request"
3. Select your fork and branch
4. Fill in the PR template:
   - **Title**: Clear, concise description
   - **Description**: Detailed explanation of changes
   - **Testing**: How you tested the changes
   - **Screenshots**: If applicable

### PR Review Process

1. Automated checks will run
2. Maintainers will review your code
3. Address any feedback:
   ```bash
   # Make changes
   git add .
   git commit -m "Address review comments"
   git push origin feature/your-feature-name
   ```
4. Once approved, your PR will be merged

### After Merge

1. Delete your branch (optional):
   ```bash
   git branch -d feature/your-feature-name
   ```

2. Update your fork:
   ```bash
   git checkout main
   git pull upstream main
   git push origin main
   ```

## Code Review Guidelines

When reviewing PRs, check for:

- ✅ Code follows style guidelines
- ✅ Changes are well-documented
- ✅ No unnecessary changes or files
- ✅ Commits are logical and well-described
- ✅ Tests pass
- ✅ Security considerations addressed

## Communication

### Issues

- Check existing issues before creating new ones
- Use clear, descriptive titles
- Provide detailed descriptions with steps to reproduce (for bugs)
- Include screenshots or code snippets when relevant

### Pull Requests

- Link related issues
- Keep PRs focused on a single feature/fix
- Respond to review comments promptly
- Ask questions if feedback is unclear

## Getting Help

If you need help:

1. Check the [README.md](README.md) for basic information
2. Review [GITHUB_WORKFLOWS.md](GITHUB_WORKFLOWS.md) for workflow help
3. Look through existing issues and discussions
4. Open a new issue with the "question" label

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Python PEP 8 Style Guide](https://pep8.org/)
- [Git Best Practices](https://git-scm.com/book/en/v2)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

## Recognition

Contributors will be recognized in the project. Thank you for your contributions!

---

*For detailed workflow documentation, see [GITHUB_WORKFLOWS.md](GITHUB_WORKFLOWS.md)*

*For workflow quick reference, see [.github/WORKFLOW_QUICK_REFERENCE.md](.github/WORKFLOW_QUICK_REFERENCE.md)*
