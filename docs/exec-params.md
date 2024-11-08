# Execution parameters

This section specifiec parameters that can be defined in 'context' or 'params' for Executor in its constructor or run() method 

## Cleanup output directory before execution

This function is designed to clear the output directory before pipeline execution based on specific conditions controlled by several parameters. It ensures a clean working environment by removing specified directories if such cleanup is requested. Only directories following the schema `exec-XXX` (where `XXX` is a sequential number) are considered for removal.

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
