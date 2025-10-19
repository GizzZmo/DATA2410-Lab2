# GitHub Actions Quick Reference

A quick reference guide for common GitHub Actions tasks and commands.

## Quick Start

```yaml
# Minimal workflow example
name: My Workflow
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - run: echo "Hello, World!"
```

## Common Triggers

```yaml
# On push to specific branches
on:
  push:
    branches: [ main, develop ]

# On pull request
on:
  pull_request:
    branches: [ main ]

# Manual trigger
on: workflow_dispatch

# Scheduled (cron)
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight

# Multiple triggers
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:
```

## Common Actions

### Checkout Code
```yaml
- name: Checkout
  uses: actions/checkout@v4
```

### Setup Python
```yaml
- name: Setup Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.11'
```

### Setup Node.js
```yaml
- name: Setup Node
  uses: actions/setup-node@v4
  with:
    node-version: '18'
```

### Cache Dependencies
```yaml
- name: Cache pip
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
```

### Upload Artifacts
```yaml
- name: Upload artifact
  uses: actions/upload-artifact@v4
  with:
    name: my-artifact
    path: path/to/artifact
```

### Download Artifacts
```yaml
- name: Download artifact
  uses: actions/download-artifact@v4
  with:
    name: my-artifact
```

## Environment Variables

### Built-in Variables
```yaml
- name: Use GitHub variables
  run: |
    echo "Repository: ${{ github.repository }}"
    echo "Ref: ${{ github.ref }}"
    echo "SHA: ${{ github.sha }}"
    echo "Actor: ${{ github.actor }}"
    echo "Workflow: ${{ github.workflow }}"
    echo "Run ID: ${{ github.run_id }}"
    echo "Runner OS: ${{ runner.os }}"
```

### Custom Environment Variables
```yaml
env:
  MY_VAR: value

jobs:
  build:
    env:
      JOB_VAR: job-value
    steps:
    - name: Step with env
      env:
        STEP_VAR: step-value
      run: echo "$MY_VAR $JOB_VAR $STEP_VAR"
```

## Secrets

```yaml
- name: Use secret
  env:
    API_KEY: ${{ secrets.API_KEY }}
  run: |
    # Use $API_KEY in your commands
    echo "Using API key"
```

## Conditional Execution

```yaml
# Run on specific branch
- name: Deploy
  if: github.ref == 'refs/heads/main'
  run: ./deploy.sh

# Run on PR
- name: PR only
  if: github.event_name == 'pull_request'
  run: echo "PR check"

# Run on success
- name: On success
  if: success()
  run: echo "Previous steps succeeded"

# Run on failure
- name: On failure
  if: failure()
  run: echo "Previous steps failed"

# Always run
- name: Always
  if: always()
  run: echo "This always runs"
```

## Matrix Strategy

```yaml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.8', '3.9', '3.10', '3.11']
    runs-on: ${{ matrix.os }}
    steps:
    - uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
```

## Job Dependencies

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - run: echo "Building"

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
    - run: echo "Testing"

  deploy:
    needs: [build, test]
    runs-on: ubuntu-latest
    steps:
    - run: echo "Deploying"
```

## Outputs

```yaml
jobs:
  job1:
    runs-on: ubuntu-latest
    outputs:
      output1: ${{ steps.step1.outputs.test }}
    steps:
    - id: step1
      run: echo "test=hello" >> $GITHUB_OUTPUT

  job2:
    needs: job1
    runs-on: ubuntu-latest
    steps:
    - run: echo "${{ needs.job1.outputs.output1 }}"
```

## Common Patterns

### Install Python Dependencies
```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
```

### Run Tests
```yaml
- name: Run tests
  run: |
    pytest tests/ --cov=. --cov-report=xml
```

### Lint Code
```yaml
- name: Lint
  run: |
    flake8 . --max-line-length=120
    black --check .
```

### Build Docker Image
```yaml
- name: Build Docker image
  run: |
    docker build -t myapp:${{ github.sha }} .
```

### Deploy to Server
```yaml
- name: Deploy
  if: github.ref == 'refs/heads/main'
  run: |
    ssh user@server 'bash -s' < deploy.sh
```

## Debugging

### Enable Debug Logging
Set repository secrets:
- `ACTIONS_STEP_DEBUG` = `true`
- `ACTIONS_RUNNER_DEBUG` = `true`

### Print Debug Info
```yaml
- name: Debug
  run: |
    echo "Event: ${{ github.event_name }}"
    echo "Ref: ${{ github.ref }}"
    echo "SHA: ${{ github.sha }}"
    env | sort
```

## Permissions

```yaml
permissions:
  contents: read
  pull-requests: write
  issues: write
  checks: write
```

## Concurrency

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

## Timeout

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
    - name: Long running task
      timeout-minutes: 10
      run: ./long-task.sh
```

## Working Directory

```yaml
jobs:
  build:
    defaults:
      run:
        working-directory: ./src
    steps:
    - name: Run in specific dir
      working-directory: ./other
      run: pwd
```

## Service Containers

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: postgres
        ports:
          - 5432:5432
```

## Useful CLI Commands

```bash
# Install act (run workflows locally)
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Run workflow locally
act

# Run specific event
act push
act pull_request

# List workflows
act -l

# Dry run
act -n

# Use specific runner image
act -P ubuntu-latest=nektos/act-environments-ubuntu:18.04
```

## Common Issues

### Issue: Workflow not triggering
**Solution**: Check trigger events, branch names, and workflow file location

### Issue: Permission denied
**Solution**: Add appropriate permissions to the workflow

### Issue: Secret not available
**Solution**: Verify secret is set in repository settings

### Issue: Timeout
**Solution**: Increase timeout or optimize slow steps

### Issue: Cache not working
**Solution**: Verify cache key and path are correct

## Resources

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Action Marketplace](https://github.com/marketplace?type=actions)
- [Community Forum](https://github.community/c/code-to-cloud/github-actions/41)

---

*For comprehensive documentation, see [GITHUB_WORKFLOWS.md](../GITHUB_WORKFLOWS.md)*
