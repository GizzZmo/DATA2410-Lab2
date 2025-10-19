# GitHub Actions Workflow Architecture

This document provides a visual overview of the GitHub Actions workflow architecture for this repository.

## Workflow Ecosystem Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    GitHub Repository                              │
│                   DATA2410-Lab2                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Events (push, PR, etc.)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    GitHub Actions Runner                          │
│                                                                   │
│  ┌───────────────────┐  ┌───────────────────┐  ┌──────────────┐│
│  │   Python CI       │  │  Code Quality     │  │   Copilot    ││
│  │   Workflow        │  │  Workflow         │  │   Agent      ││
│  └───────────────────┘  └───────────────────┘  └──────────────┘│
│           │                      │                      │        │
│           ▼                      ▼                      ▼        │
│  ┌────────────────┐     ┌────────────────┐    ┌──────────────┐ │
│  │ Multi-Python   │     │ Linting &      │    │ Code         │ │
│  │ Testing        │     │ Security Scan  │    │ Assistance   │ │
│  └────────────────┘     └────────────────┘    └──────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Results
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    GitHub Checks & Status                         │
│                                                                   │
│  ✅ All tests passed                                              │
│  ✅ Code quality checks passed                                    │
│  ✅ Security scans completed                                      │
└─────────────────────────────────────────────────────────────────┘
```

## Workflow Execution Flow

### 1. Code Change Lifecycle

```
Developer        GitHub           Workflows         Checks
    │               │                 │               │
    │  Push/PR      │                 │               │
    │──────────────>│                 │               │
    │               │  Trigger        │               │
    │               │────────────────>│               │
    │               │                 │  Run Jobs     │
    │               │                 │──────────────>│
    │               │                 │               │
    │               │                 │  Results      │
    │               │                 │<──────────────│
    │               │  Status Update  │               │
    │               │<────────────────│               │
    │  Notification │                 │               │
    │<──────────────│                 │               │
    │               │                 │               │
```

### 2. Python CI Workflow Execution

```
┌─────────────────────────────────────────────────────────┐
│                    Python CI Workflow                    │
└─────────────────────────────────────────────────────────┘
                           │
           ┌───────────────┴───────────────┐
           │                               │
           ▼                               ▼
    ┌─────────────┐                ┌─────────────┐
    │  Test Job   │                │ Code Quality│
    │             │                │    Job      │
    └─────────────┘                └─────────────┘
           │                               │
    ┌──────┴──────┐                ┌──────┴──────┐
    │             │                │             │
    ▼             ▼                ▼             ▼
┌───────┐   ┌───────┐      ┌───────┐     ┌───────┐
│Python │   │Python │      │Black  │     │isort  │
│ 3.8   │   │ 3.9   │      │Check  │     │Check  │
└───────┘   └───────┘      └───────┘     └───────┘
    │             │                │             │
    ▼             ▼                ▼             ▼
┌───────┐   ┌───────┐      ┌───────┐     ┌───────┐
│Python │   │Python │      │Pylint │     │       │
│ 3.10  │   │ 3.11  │      │Check  │     │       │
└───────┘   └───────┘      └───────┘     └───────┘
    │             │                │             │
    └──────┬──────┘                └──────┬──────┘
           │                               │
           ▼                               ▼
    ┌─────────────┐                ┌─────────────┐
    │  Run Tests  │                │   Report    │
    │  & Coverage │                │   Issues    │
    └─────────────┘                └─────────────┘
```

### 3. Code Quality Workflow Components

```
┌─────────────────────────────────────────────────────────┐
│              Code Quality Workflow                       │
└─────────────────────────────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
           ▼               ▼               ▼
    ┌──────────┐    ┌──────────┐   ┌──────────┐
    │  Lint    │    │ Security │   │Dependency│
    │  Check   │    │   Scan   │   │  Check   │
    └──────────┘    └──────────┘   └──────────┘
           │               │               │
     ┌─────┼─────┐        │          ┌────┴────┐
     │     │     │        │          │         │
     ▼     ▼     ▼        ▼          ▼         ▼
  ┌────┐┌────┐┌────┐  ┌──────┐  ┌──────┐  ┌──────┐
  │Flk8││Pyln││Mypy│  │Bandit│  │Safety│  │Report│
  └────┘└────┘└────┘  └──────┘  └──────┘  └──────┘
```

## Event Triggers and Workflow Mapping

```
┌──────────────────┐
│  GitHub Events   │
└──────────────────┘
         │
    ┌────┴────────────────────────────────┐
    │                                     │
    ▼                                     ▼
┌────────┐                          ┌──────────┐
│  Push  │                          │    PR    │
│  main  │                          │  opened  │
└────────┘                          └──────────┘
    │                                     │
    ├─────────────────┬───────────────────┤
    │                 │                   │
    ▼                 ▼                   ▼
┌─────────┐    ┌──────────┐       ┌──────────┐
│Python CI│    │Code      │       │ Copilot  │
│Workflow │    │Quality   │       │ Agent    │
└─────────┘    └──────────┘       └──────────┘
```

## Workflow Dependencies

```
Start Event
     │
     ▼
┌─────────────────────────────────────────┐
│  Checkout Code (all workflows)          │
└─────────────────────────────────────────┘
     │
     ├────────────────────┬────────────────────┐
     ▼                    ▼                    ▼
┌──────────┐        ┌──────────┐        ┌──────────┐
│  Setup   │        │  Setup   │        │  Setup   │
│  Python  │        │  Python  │        │  Python  │
└──────────┘        └──────────┘        └──────────┘
     │                    │                    │
     ▼                    ▼                    ▼
┌──────────┐        ┌──────────┐        ┌──────────┐
│  Cache   │        │  Cache   │        │  Cache   │
│   Deps   │        │   Deps   │        │   Deps   │
└──────────┘        └──────────┘        └──────────┘
     │                    │                    │
     ▼                    ▼                    ▼
┌──────────┐        ┌──────────┐        ┌──────────┐
│ Install  │        │ Install  │        │ Install  │
│   Deps   │        │  Tools   │        │   Deps   │
└──────────┘        └──────────┘        └──────────┘
     │                    │                    │
     ▼                    ▼                    ▼
┌──────────┐        ┌──────────┐        ┌──────────┐
│   Run    │        │   Run    │        │   Run    │
│  Tests   │        │  Checks  │        │  Agent   │
└──────────┘        └──────────┘        └──────────┘
     │                    │                    │
     └────────────────────┴────────────────────┘
                          │
                          ▼
                    ┌──────────┐
                    │ Report   │
                    │ Results  │
                    └──────────┘
```

## Artifact Flow

```
┌─────────────┐
│  Workflows  │
└─────────────┘
       │
       ├─────────────────┬─────────────────┐
       │                 │                 │
       ▼                 ▼                 ▼
┌──────────┐      ┌──────────┐     ┌──────────┐
│Coverage  │      │Security  │     │  Lint    │
│ Report   │      │ Report   │     │  Report  │
└──────────┘      └──────────┘     └──────────┘
       │                 │                 │
       └─────────────────┴─────────────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ GitHub Artifacts│
                └─────────────────┘
                         │
                         ▼
                ┌─────────────────┐
                │  Downloadable   │
                │    for 90 days  │
                └─────────────────┘
```

## Security Workflow Integration

```
┌─────────────────────────────────────────────────────────┐
│                  Security Pipeline                       │
└─────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌──────────────┐   ┌──────────────┐  ┌──────────────┐
│   Bandit     │   │    Safety    │  │  CodeQL      │
│  (Code Scan) │   │ (Dependency) │  │  (Analysis)  │
└──────────────┘   └──────────────┘  └──────────────┘
        │                  │                  │
        └──────────────────┴──────────────────┘
                           │
                           ▼
                ┌────────────────────┐
                │  Security Tab      │
                │  (GitHub)          │
                └────────────────────┘
```

## Workflow State Machine

```
┌─────────┐
│ Queued  │
└─────────┘
     │
     ▼
┌─────────┐
│Requested│
└─────────┘
     │
     ▼
┌─────────┐      ┌─────────┐
│ Waiting │─────>│Cancelled│
└─────────┘      └─────────┘
     │
     ▼
┌─────────┐      ┌─────────┐
│In Progress──────>│ Skipped │
└─────────┘      └─────────┘
     │
     ├──────────┬──────────┐
     ▼          ▼          ▼
┌─────────┐┌─────────┐┌─────────┐
│ Success ││ Failure ││Cancelled│
└─────────┘└─────────┘└─────────┘
```

## Caching Strategy

```
┌─────────────────────────────────────────┐
│          First Workflow Run             │
└─────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
┌──────────────┐        ┌──────────────┐
│Install Deps  │        │  Cache Key:  │
│  (~2 min)    │───────>│  OS-pip-hash │
└──────────────┘        └──────────────┘
                               │
                               ▼
┌─────────────────────────────────────────┐
│         Subsequent Runs                 │
└─────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
┌──────────────┐        ┌──────────────┐
│ Cache Hit?   │        │   Restore    │
│              │───────>│   Cache      │
└──────────────┘        │  (~10 sec)   │
                        └──────────────┘
```

## Parallel vs Sequential Execution

### Parallel Execution (Default)
```
Job 1 ────────────>
Job 2 ────────────>
Job 3 ────────────>
       Time ───────>
```

### Sequential Execution (with needs)
```
Job 1 ──────>
             Job 2 ──────>
                          Job 3 ──────>
                   Time ────────────────>
```

## Best Practices Applied

1. **Caching**: All workflows cache Python dependencies
2. **Matrix Strategy**: Python CI tests across multiple versions
3. **Fail-Fast Disabled**: Allows all tests to complete
4. **Continue on Error**: Non-critical checks don't block workflow
5. **Conditional Execution**: Steps run only when needed
6. **Artifact Upload**: Important reports saved for review

## Monitoring and Alerts

```
┌─────────────────────────────────────────────────────────┐
│              Workflow Monitoring                         │
└─────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌──────────────┐   ┌──────────────┐  ┌──────────────┐
│GitHub Actions│   │   Status     │  │  Email       │
│   Tab        │   │   Badges     │  │Notifications │
└──────────────┘   └──────────────┘  └──────────────┘
```

## Resource Usage

```
Resource Type          Usage per Workflow Run
─────────────────────────────────────────────
Compute Time           2-5 minutes
Storage (Artifacts)    ~50MB (90-day retention)
Network Transfer       ~200MB (download deps)
GitHub Actions Minutes ~5 min/run × jobs
```

## Further Reading

- [GITHUB_WORKFLOWS.md](../GITHUB_WORKFLOWS.md) - Comprehensive documentation
- [WORKFLOW_QUICK_REFERENCE.md](WORKFLOW_QUICK_REFERENCE.md) - Quick command reference
- [workflows/README.md](workflows/README.md) - Workflow-specific documentation

---

*This architecture is designed to be scalable, maintainable, and efficient.*
