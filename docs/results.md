
# Pipeline Result Handling

During the execution of a pipeline, the result can be stored using a module callback function. The function `module.setResult` is used for this purpose. This result will be available after the pipeline's execution in the returned `PTest` object. To retrieve the result from this object, you simply need to call the `test.get_result()` method.

Example:
```
    test = executor.run(...)
    result = test.get_result()
```

**Note:** In multiple execution mode (where multiple pipelines are executed for different tests), the `Executor` will return a `PTest` object from the last pipeline executed, representing the most recent test result.
