
# Input and Output Directory Management

## Input Directory for Pipeline Execution

The input directory for running pipelines can be set using the `din` parameter within the `context` or `params` argument when constructing the `Executor` or during the execution via `executor.run()`, as shown below:

```python
Executor(context='din=data/_in')
```

If the `din` parameter is not explicitly set, the default input directory will be `_in` in the current working directory of the script using the `Executor`.

The `din` parameter can also be defined using a configuration file `.cfg`.

---

## Output Directory for Pipeline Execution

The `Executor` object generates intermediate and output files for subsequent pipeline runs within a directory specified by the `dout` parameter, set in the `context` or `params` argument, or during execution via `executor.run()`.

If the `dout` parameter is not provided, the output directory defaults to a subdirectory named `_out` in the current working directory of the script from which `executor.run()` is called. Each subsequent pipeline run creates a dedicated subdirectory within the output directory, following the naming convention `exec-XXX`, where `XXX` is a sequential three-digit identifier (e.g., `exec-001`, `exec-002`, etc.).

### Customizing Subdirectory Names

The prefix `exec` can be modified using the `exedir` parameter via the `context` or `params` argument. For example, to change the prefix to `parser`, use:

```python
executor.run(context='execdir=parser')
```

This setting will generate output subdirectories named `parser-001`, `parser-002`, etc.

---

## Cleanup output directory before execution

This function is designed to clear the output directory before pipeline execution based on specific conditions controlled by several parameters. It ensures a clean working environment by removing specified directories if such cleanup is requested. Only directories following the schema `exec-XXX` (where `XXX` is a sequential number) are considered for removal. The `exec` keyword can be replaced by using `exedir` parameter in above section.

### Parameters:

- **`clean` (bool)**: Controls whether this function is activated. When set to `True`, the function will proceed with clearing; when set to `False`, it will be skipped.
- **`cleanInclude` (list)**: Defines a list of directories that should be removed. Only directories listed here that match the `exec-XXX` schema (where `XXX` is a sequential number) will be considered for deletion, while others will remain untouched.
- **`cleanExclude` (list)**: Specifies directories that should not be removed during the clearing process. Even if these directories are listed in `cleanInclude`, they will be preserved if they are present in this list.

### Examples

1. **Remove Only a Specified Directory**  
   This example removes only two directories `exec-001` and `exec-002`:

```python
   executor.run('Results: ', context='clean=True;cleanInclude=exec-001,exec-001')
```
   This will ensure that only `exec-001` is removed, while other directories remain untouched.

2. **Remove All Directories Except One**  
   This example removes all directories except `exec-002`:
```python
   executor.run('Results: ', context='clean=True;cleanExclude=exec-002')
```
   This will remove all directories matching the `exec-XXX` schema, except for `exec-002`, which is preserved.

---

### Fixed Output Subdirectory Name

To ensure that the output subdirectory always has a fixed name (e.g., `parser` instead of `parser-001`), use the `execdirexact` parameter:

```python
executor.run(context='execdir=parser;exedirexact=True')
```

With this setting, pipeline runs are always saved in the `parser` directory, which will be cleared before each new execution if it already exists.
