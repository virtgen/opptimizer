# Pipeline Execution Modes

Pipeline execution by the `Executor` object can operate in two modes:

### 1. Single Execution Mode
In single execution mode, only one pipeline is executed. This mode is manifested by automatic generation of the parameter `exmode=single` in the execution parameters accesible by modules (in their callbacks).

### 2. Multiple Execution Mode
In multiple execution mode, multiple pipelines are executed according to the structure defined by `paramrange` parameters in executor.run() or executor.execute(). This mode can be identified by lack of parameter `exmode=single` in the execution parameters accesible by modules (in their callbacks).
