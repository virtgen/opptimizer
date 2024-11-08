# Pipeline Execution Modes

Pipeline execution by the `Executor` object can operate in two modes:

### 1. Single Execution Mode
In single execution mode, only one pipeline is executed. This mode is manifested by automatic generation of the parameter `exmode=single` in the execution parameters accesible by modules (in their callbacks).

Following example checks if exexution mode is `single`:

```python
import opptimizer as op

def module_exec(mod_obj, params, tokenData = None):
    exmode = op.oppval('exmode', params)
    singleMode = True if exmode and exmode=='single' else False
    print(f'Single mode:{singleMode}')

op.Executor().run(modules = [module_exec])
```

### 2. Multiple Execution Mode
In multiple execution mode, multiple pipelines are executed according to the structure defined by `paramrange` parameters in executor.run() or executor.execute(). This mode can be identified by lack of parameter `exmode=single` in the execution parameters accesible by modules (in their callbacks).
