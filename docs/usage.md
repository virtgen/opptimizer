
## Basic Usage

### 1. Import the `opptimizer` Library

Begin by importing the `opptimizer` library into your project:

```python
import opptimizer
```

### 2. Create an `Executor` Instance

Create an instance of the `Executor` class. You can optionally set the context and/or specify a configuration file containing the context during instantiation:

```python
executor = opptimizer.Executor(context=my_context)
# or with a configuration file (you can use any file name)
executor = opptimizer.Executor(cfg="path/to/opp.cfg")
```

### 3. Define Modules

Define the modules you intend to use. Modules can be function:

```python
def module_exec(data):
    # Process data in some way
    return modified_data
```
or instances of the `Mod` class:
```python
module_instance = opptimizer.Mod(module_exec)
```

### 4. Run the `Executor.run()` Method

Run the `Executor` with input data or a list of modules:

```python
result = executor.run(input_data,modules=[module_exec])
```
or with an module instance:

```python
result = executor.run(input_data, modules=[module_instance])
```

You can use any number of modules in `modules` list that will be executed sequentially.

### 5. Get the Result from Execution

Retrieve the result from the execution:

```python
final_result = result.get_result()
```
