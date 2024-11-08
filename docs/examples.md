
# Examples
## Basic Pipeline Example

The following example demonstrates a simple pipeline that extends an input string by adding additional parts through modules `mod_1` and `mod_2`, ultimately returning the combined text.
```python
import opptimizer as op

def mod_1(mod_obj, params, tokenData = None):
    tokenData = tokenData + 'result 1'
    return tokenData

def mod_2(mod_obj, params, tokenData = None):
    tokenData = tokenData + ', result 2'
    mod_obj.setResult(tokenData)

executor = op.Executor(modules = [mod_1, mod_2])
response = executor.run('Results: ')

print(f"{response.get_result()}")
```

```markdown
Output:
    Results: result 1, result 2
```