# Workflows Directory

This directory contains GitHub Actions workflow files that automate various tasks for this repository.

## Available Workflows

### 1. Python CI (`python-ci.yml`)

**Purpose**: Continuous Integration for Python code

**Triggers**:
- Push to main branch
- Pull requests to main branch

**What it does**:
- Tests code against multiple Python versions (3.8, 3.9, 3.10, 3.11)
- Runs linting with flake8 to catch syntax errors
- Executes unit tests with pytest (if tests directory exists)
- Generates code coverage reports
- Performs code quality checks with Black, isort, and pylint

**Status**: Example workflow (not active by default)

---

### 2. Code Quality (`code-quality.yml`)

**Purpose**: Comprehensive code quality and security checks

**Triggers**:
- All pushes
- All pull requests

**What it does**:
- **Linting**: Runs flake8 and pylint for code quality
- **Formatting**: Checks code formatting with Black
- **Import Ordering**: Verifies imports are sorted with isort
- **Type Checking**: Runs mypy for static type analysis
- **Security Scanning**: Uses bandit to detect security issues
- **Dependency Check**: Scans dependencies for known vulnerabilities with safety

**Status**: Example workflow (not active by default)

---

### 3. Copilot Coding Agent

**Purpose**: Automated code assistance using GitHub Copilot

**Triggers**: Dynamic (managed by GitHub)

**What it does**:
- Provides automated code review and suggestions
- Assists with issue tracking and resolution
- Analyzes pull requests and provides recommendations

**Status**: Active

---

## Enabling Workflows

These example workflows are provided as templates. To enable them:

1. Review the workflow configuration
2. Customize settings as needed for your project
3. Commit and push the workflow files
4. Workflows will automatically activate on their next trigger event

## Disabling Workflows

To disable a workflow:

1. Navigate to the **Actions** tab in GitHub
2. Select the workflow you want to disable
3. Click the **⋯** menu and select "Disable workflow"

Alternatively, you can:
- Delete the workflow file from this directory
- Rename the file extension (e.g., `.yml.disabled`)

## Workflow Best Practices

1. **Use caching**: Workflows cache pip dependencies for faster runs
2. **Matrix testing**: Test across multiple Python versions
3. **Continue on error**: Some checks use `continue-on-error: true` to not block the workflow
4. **Upload artifacts**: Important reports are saved as artifacts
5. **Fail-fast disabled**: Allows all Python versions to be tested even if one fails

## Customization

### Adding New Workflows

1. Create a new `.yml` file in this directory
2. Define your workflow structure (see examples above)
3. Test locally using [act](https://github.com/nektos/act) if possible
4. Commit and push to activate

### Modifying Existing Workflows

- Adjust trigger events in the `on:` section
- Add or remove jobs and steps as needed
- Configure Python versions in the matrix strategy
- Update linting rules and tools

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Python CI/CD Best Practices](https://docs.python.org/3/library/unittest.html)
- [Comprehensive Workflow Guide](../../GITHUB_WORKFLOWS.md)

## Troubleshooting

If a workflow fails:

1. Check the Actions tab for detailed logs
2. Review the error messages in failed steps
3. Verify all dependencies are correctly specified
4. Ensure Python code follows linting standards
5. Test changes locally before pushing

For more help, see the [Troubleshooting section](../../GITHUB_WORKFLOWS.md#troubleshooting) in the main workflow documentation.

---

*For comprehensive information about GitHub Actions and workflows, see [GITHUB_WORKFLOWS.md](../../GITHUB_WORKFLOWS.md)*
