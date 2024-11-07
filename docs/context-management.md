
# Context Management Logic

The `Executor` object is responsible for executing pipelines and has its own base context, which can be set either during its creation as a parameter in the constructor or via the `set_context` method. If set, this base context will be used for all pipelines executed by this instance of the `Executor`.

## Context Setup

When creating an `Executor` instance, you can define a base context as follows:

```python
executor = Executor(context=base_context)
```

Alternatively, you can set the context after the instance has been created using:

```python
executor.set_context(new_context)
```

The base context, if defined, will be used for all pipeline executions initiated by this `Executor`.

## Context Merging During Execution

When executing a chain of pipelines using the `run()` or `execute()` methods on the `Executor` object, an execution context can be passed as a parameter. If the `Executor` already has a base context set (via the constructor or the `set_context` method), this parameter context will be merged with the base context. The merged context becomes the final context used during execution.

Example usage:

```python
executor.run(context=execution_context, ...)
```

This merging behavior ensures that the provided execution context is combined with any pre-existing base context, and the resulting merged context is used throughout the execution process.

## Context Propagation to Modules

Each `Mod` module used during the execution process is provided with the final merged context from the `Executor` before being used. While executing pipelines, methods within the module can retrieve the context using the `getContext()` method.

Example of retrieving context within a `Mod` module:

```python
context = self.getContext()
```

## Advanced Context Management in `PScript`

The `PScript` object, used to manage pipeline execution through `Executor` objects, can load its context during initialization (in 'Init' method) from a configuration file containing parameters such as input and output directories or module paths as files. The context within the `PScript` object can later be used in scripts as a parameter for the `run()` or `execute()` methods on an `Executor` object. Use of such context in PScript is usually used in advanced mode of Opptimizer usage in local mode.

