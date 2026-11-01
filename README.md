<p align="center">
  <img src="https://res.cloudinary.com/medmahdimaarouf/image/upload/v1690126172/Proxtractor/prx-logo-dark.svg" width="120" alt="CropsFlow Logo" />
</p>

<h1 align="center">CropsFlow</h1>

<p align="center">
  A Python automation framework for building modular, scalable, and service-oriented workflow applications.
</p>

# Introduction

CropsFlow is a Python-based framework for building automation-driven applications with modular services, dependency injection, actions, pipes, tasks, scheduling, and orchestration.

It is designed for developers who want to compose reusable application components and run task-based workflows in a structured environment. The framework supports runtime scanning, module-based composition, service registration, API routing, task lifecycle management, and background scheduling.

## Why CropsFlow?

- Modular application design
- Dependency injection support
- Reusable actions and pipes
- Task and workflow templates
- Scheduler for periodic and delayed jobs
- FastAPI-based router integrations
- Event-driven communication support
- Orchestration for automation workloads

# Installation

## Install from PyPI

```bash
pip install cropsflow
```

## Install from source

```bash
git clone https://github.com/medmahdimaarouf/py-cropsflow.git
cd py-cropsflow
pip install -r requirements.txt
```

# Example

## Service example

```python
from cropsflow.common import service, InjectionScope

@service(scope=InjectionScope.DEFAULT)
class Driver:
    def __init__(self):
        pass
```

## Action example

```python
from cropsflow.common import action, option, inject
from cropsflow.common.abstracts import Action, ActionContext

@action(selector='my-pipe')
@option(key='my-option', meta_type=str)
class MyAction(Action):

    @inject(arg_name='driver', token=Driver)
    def __init__(self, driver: Driver):
        self.driver = driver

    def start(self, context: ActionContext, options: dict = {}):
        return {"status": "ok", "message": "Action executed"}
```

## Pipe example

```python
from cropsflow.common import pipe

@pipe(selector='my-pipe')
class MyPipe:
    def accumulate(self, value, accessor: str = None):
        self.value = value
```

## Module example

```python
from cropsflow.common import module
from cropsflow.common.module import CommonModule

@module(
    declarations=[],
    imports=[CommonModule],
    exports=[],
    providers=[]
)
class MyModule:
    def __init__(self):
        pass
```

# Usage

## Application bootstrap

```python
import asyncio
from cropsflow.core.application import Application

async def main():
    app = Application()
    # app.bootstrap(module=AppModule)
    print("Application initialized")

asyncio.run(main())
```

## Scheduling jobs

```python
from cropsflow.scheduler import BackgroundScheduler

scheduler = BackgroundScheduler()

@scheduler.every(seconds=10)
def check_status():
    print("Running every 10 seconds")
```

## Task template example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<task dataset="brand-items">
    <meta>
        <title>Example task</title>
        <version>1.0</version>
        <description>
            Example task for running multi actions
        </description>
        <tags>
            task,automation,robots
        </tags>
        <readme src="./readme.md"/>
    </meta>
    <playbook>
        <sleep seconds="2">
            <sleep seconds="1"/>
            <sleep seconds="2"/>
            <sleep seconds="3"/>
        </sleep>
    </playbook>
</task>
```

## Router integration

```python
from cropsflow.router import Router
from fastapi import FastAPI

app = FastAPI()
router = Router(prefix="/api")

@router.get("/health")
async def health():
    return Router.success({"status": "ok"})
```

## Common module

CropsFlow includes a built-in `CommonModule` that exposes reusable actions and pipes such as:

- `DelayAction`
- `IterateAction`
- `CMDAction`
- `MapPipe`
- `ListPipe`
- `IntegerPipe`
- `TextPipe`
- `DecimalPipe`

## Core concepts

The framework is built around a few core concepts:

- `@service`: registers a class as a service
- `@inject`: resolves dependencies at runtime
- `@module`: groups components and exports dependencies
- `@action`: marks a workflow action
- `@pipe`: defines a data transformation pipe
- `@task`: attaches a task template to a class
- `Application`: bootstraps and resolves the dependency graph
- `Scheduler`: runs periodic and delayed jobs
- `Router`: exposes REST endpoints through FastAPI
- `Orchestrator`: manages automation workers and execution flows

# Contributing

Contributions are welcome.

To contribute:

1. Fork the repository.
2. Create a feature branch.
3. Make your changes with tests when applicable.
4. Run validation checks.
5. Submit a pull request with a clear description.

Please keep the project clean and maintain a consistent coding style. If you are adding new features, also document the behavior and usage clearly.

# License

This project is licensed under the Apache License, Version 2.0.

See the [LICENSE](LICENSE) file for details.

---

### Navigation

[Introduction](#introduction) • [Installation](#installation) • [Example](#example) • [Usage](#usage) • [Contributing](#contributing) • [License](#license)
