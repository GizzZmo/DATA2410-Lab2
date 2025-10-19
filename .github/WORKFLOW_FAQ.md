# GitHub Workflows FAQ

Frequently Asked Questions about GitHub Actions and workflows in this repository.

## Table of Contents

- [General Questions](#general-questions)
- [Setup and Configuration](#setup-and-configuration)
- [Troubleshooting](#troubleshooting)
- [Performance](#performance)
- [Security](#security)
- [Best Practices](#best-practices)

---

## General Questions

### What are GitHub Actions?

GitHub Actions is GitHub's built-in CI/CD platform that automates workflows for building, testing, and deploying code. Workflows are defined in YAML files and run in response to repository events.

### Why do we use workflows?

Workflows provide automated:
- Code testing across multiple Python versions
- Code quality checks (linting, formatting)
- Security scanning
- Continuous integration and deployment
- Documentation building
- Release automation

### How do I view workflow runs?

1. Navigate to the **Actions** tab in the GitHub repository
2. See a list of all workflow runs
3. Click on any run to see detailed logs
4. Click on individual jobs to see step-by-step execution

### What triggers workflows in this repository?

- **Push to main branch**: Triggers Python CI and Code Quality workflows
- **Pull requests**: Triggers all testing and quality checks
- **Manual trigger**: Some workflows can be triggered manually
- **Scheduled**: Some workflows run on a schedule

### Are workflows required for my PR to be merged?

Yes, all required workflows must pass before a PR can be merged. This ensures code quality and prevents broken code from being merged.

---

## Setup and Configuration

### How do I create a new workflow?

1. Create a YAML file in `.github/workflows/`
2. Define the workflow name, triggers, and jobs
3. Commit and push the file
4. The workflow will activate on its next trigger event

Example:
```yaml
name: My Workflow
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - run: echo "Hello, World!"
```

### How do I disable a workflow?

**Option 1**: Through GitHub UI
1. Go to Actions tab
2. Select the workflow
3. Click ⋯ menu → "Disable workflow"

**Option 2**: Rename the file
```bash
mv .github/workflows/my-workflow.yml .github/workflows/my-workflow.yml.disabled
```

### How do I add secrets to workflows?

1. Go to repository Settings
2. Navigate to "Secrets and variables" → "Actions"
3. Click "New repository secret"
4. Add name and value
5. Use in workflow: `${{ secrets.SECRET_NAME }}`

### How do I schedule a workflow?

Use the `schedule` trigger with cron syntax:
```yaml
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight UTC
```

Cron examples:
- `'0 0 * * *'` - Daily at midnight
- `'0 */6 * * *'` - Every 6 hours
- `'0 0 * * 0'` - Weekly on Sunday
- `'0 0 1 * *'` - Monthly on the 1st

### How do I test workflows locally?

Use [act](https://github.com/nektos/act):
```bash
# Install act
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Run workflows
act

# Run specific job
act -j test

# Dry run
act -n
```

---

## Troubleshooting

### Why isn't my workflow running?

**Possible causes:**
1. Workflow file not in `.github/workflows/` directory
2. YAML syntax error (use a YAML validator)
3. Trigger event doesn't match (check branch names)
4. Workflow is disabled
5. Workflow requires approval (for first-time contributors)

**Solution:** Check the Actions tab for error messages and verify your trigger configuration.

### My workflow failed. What do I do?

1. Go to the Actions tab
2. Click on the failed run
3. Click on the failed job
4. Expand the failed step to see error details
5. Fix the issue and push again

Common failures:
- Linting errors → Fix code style
- Test failures → Fix failing tests
- Dependency issues → Update requirements
- Permission errors → Check workflow permissions

### How do I view detailed logs?

1. Actions tab → Select workflow run
2. Click on job name
3. Expand individual steps
4. Enable debug logging by setting secrets:
   - `ACTIONS_STEP_DEBUG=true`
   - `ACTIONS_RUNNER_DEBUG=true`

### Why is my workflow stuck or taking too long?

**Possible causes:**
1. Job timeout (default 6 hours)
2. Waiting for runner availability
3. Long-running tests or builds
4. Network issues downloading dependencies
5. Infinite loop in code

**Solutions:**
- Set explicit timeouts: `timeout-minutes: 30`
- Use caching for dependencies
- Optimize slow tests
- Check for infinite loops
- Cancel stuck runs manually

### How do I fix "Permission denied" errors?

Add permissions to your workflow:
```yaml
permissions:
  contents: read
  pull-requests: write
  issues: write
```

Or grant all permissions:
```yaml
permissions: write-all
```

### Why are my secrets not working?

**Common issues:**
1. Secret not added to repository settings
2. Typo in secret name
3. Secret not available for fork PRs (security feature)
4. Using wrong syntax (use `${{ secrets.NAME }}`)

**Solution:** Verify secret exists and name matches exactly.

---

## Performance

### How can I speed up my workflows?

**1. Use caching:**
```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
```

**2. Run jobs in parallel:**
```yaml
jobs:
  job1:
    runs-on: ubuntu-latest
  job2:
    runs-on: ubuntu-latest  # Runs simultaneously with job1
```

**3. Use matrix strategy efficiently:**
```yaml
strategy:
  matrix:
    python-version: ['3.9', '3.11']  # Test only min and max versions
```

**4. Skip unnecessary jobs:**
```yaml
- name: Skip for docs
  if: "!contains(github.event.head_commit.message, '[docs]')"
```

### How much do workflows cost?

- **Public repositories**: Free unlimited minutes
- **Private repositories**: Free tier includes 2,000 minutes/month
- Additional minutes: $0.008/minute (Linux runners)

This repository uses public runners, so workflows are free.

### How long are artifacts stored?

- Default: 90 days
- Can be configured: 1-90 days
- Manually deleted anytime

### Can workflows run in parallel?

Yes! By default, jobs in different workflows run in parallel unless:
- `needs:` dependency is specified
- Concurrency limits are set
- Runner availability is limited

---

## Security

### Are workflows secure?

Generally yes, but follow best practices:
- Don't log secrets
- Pin action versions
- Review third-party actions
- Use least-privilege permissions
- Validate inputs

### How do I secure my workflows?

**1. Pin action versions:**
```yaml
- uses: actions/checkout@v4  # Good
- uses: actions/checkout@692973e3d937129bcbf40652eb9f2f61becf3332  # Better (commit SHA)
```

**2. Use secrets for sensitive data:**
```yaml
- name: Deploy
  env:
    API_KEY: ${{ secrets.API_KEY }}  # Never hardcode
```

**3. Limit permissions:**
```yaml
permissions:
  contents: read  # Only what's needed
```

**4. Review action source code:**
Check the action's repository before using it.

### Can workflows access my secrets?

- Secrets are encrypted and only available during workflow execution
- Not visible in logs (redacted)
- Not available to fork PRs by default (security measure)
- Scoped to the repository where they're defined

### What if I accidentally commit a secret?

1. **Immediately revoke** the secret/token/key
2. Remove from Git history using `git filter-branch` or BFG Repo-Cleaner
3. Update the secret in GitHub settings
4. Force push to update remote: `git push --force`

**Note:** Deleting from recent commits isn't enough; it's still in history.

### Are third-party actions safe?

**Trusted sources:**
- GitHub-official actions (`actions/*`)
- Verified creators (blue checkmark)
- Popular, well-maintained actions

**Before using:**
- Check source code
- Read reviews and issues
- Verify regular updates
- Pin to specific version/SHA

---

## Best Practices

### What are workflow best practices?

1. **Use caching** for dependencies
2. **Pin action versions** for stability
3. **Fail fast** when appropriate
4. **Add timeouts** to prevent infinite runs
5. **Use matrix** for multi-version testing
6. **Document workflows** in README
7. **Monitor usage** and optimize
8. **Keep workflows DRY** with reusable workflows
9. **Use conditional execution** to skip unnecessary steps
10. **Upload artifacts** for debugging

### Should I commit generated files?

Generally **no**. Instead:
- Use workflows to generate files on-demand
- Upload as artifacts if needed
- Use `.gitignore` to exclude generated files
- Document how to generate files

### How often should workflows run?

- **On every push/PR**: Tests, linting
- **Daily**: Security scans, dependency updates
- **Weekly**: Full test suite, reports
- **On release**: Deployment, documentation

Balance coverage with resource usage.

### How do I organize multiple workflows?

```
.github/workflows/
├── ci.yml                 # Main CI pipeline
├── code-quality.yml       # Linting, formatting
├── security.yml           # Security scans
├── deploy-production.yml  # Production deployment
├── deploy-staging.yml     # Staging deployment
└── scheduled-tasks.yml    # Periodic tasks
```

### Should I use self-hosted runners?

**GitHub-hosted pros:**
- No maintenance
- Auto-scaling
- Free for public repos

**Self-hosted pros:**
- More control
- Custom software
- Better performance
- Access to private resources

**Use self-hosted if you need:**
- Special hardware/software
- Access to internal networks
- Significantly more resources
- Lower latency to services

### How do I handle workflow failures in production?

1. **Monitor**: Set up alerts for failures
2. **Rollback**: Have automated rollback procedures
3. **Logs**: Collect and analyze logs
4. **Notify**: Alert team members
5. **Document**: Keep runbooks for common issues

---

## Advanced Topics

### Can I reuse workflow code?

Yes! Use reusable workflows:

**Define reusable workflow** (`.github/workflows/reusable.yml`):
```yaml
name: Reusable Workflow
on:
  workflow_call:
    inputs:
      config-path:
        required: true
        type: string
```

**Call reusable workflow**:
```yaml
jobs:
  call-workflow:
    uses: ./.github/workflows/reusable.yml
    with:
      config-path: ./config.json
```

### How do I pass data between jobs?

Use job outputs:
```yaml
jobs:
  job1:
    outputs:
      output1: ${{ steps.step1.outputs.result }}
    steps:
    - id: step1
      run: echo "result=hello" >> $GITHUB_OUTPUT

  job2:
    needs: job1
    steps:
    - run: echo "${{ needs.job1.outputs.output1 }}"
```

### Can I trigger workflows from other workflows?

Yes, use `workflow_dispatch` or `repository_dispatch`:

```yaml
- name: Trigger another workflow
  uses: peter-evans/repository-dispatch@v2
  with:
    token: ${{ secrets.GITHUB_TOKEN }}
    event-type: my-event
```

### How do I handle different environments?

Use environments in GitHub:

1. Settings → Environments → New environment
2. Configure protection rules
3. Add environment secrets

```yaml
jobs:
  deploy:
    environment: production
    steps:
    - name: Deploy
      run: ./deploy.sh
```

---

## Additional Resources

### Documentation
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Repository GITHUB_WORKFLOWS.md](../GITHUB_WORKFLOWS.md)
- [Workflow Quick Reference](WORKFLOW_QUICK_REFERENCE.md)
- [Workflow Architecture](WORKFLOW_ARCHITECTURE.md)

### Tools
- [act](https://github.com/nektos/act) - Run workflows locally
- [actionlint](https://github.com/rhysd/actionlint) - Workflow linter
- [YAML Validator](https://www.yamllint.com/) - Validate YAML syntax

### Community
- [GitHub Community Forum](https://github.community/c/code-to-cloud/github-actions/41)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [Awesome GitHub Actions](https://github.com/sdras/awesome-actions)

---

## Still Have Questions?

- Check the [Troubleshooting guide](../GITHUB_WORKFLOWS.md#troubleshooting)
- Review workflow logs in the Actions tab
- Search [GitHub Community](https://github.community/)
- Open an issue in this repository

---

*Last updated: October 2025*
