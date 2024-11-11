# Introduction to Opptimizer
Opptimizer is an optimization framework designed for AI pipelines, enabling efficient management and execution of complex processes and workflows.

This section provides a quick overview of installation, basic usage, and simple examples.  
To dive deeper, please see the full documentation at [https://opptimizer.readthedocs.io/](https://opptimizer.readthedocs.io/).

## Installation

Installin by PyPI is appropriate for most use cases.

```
pip install opptimizer
```
There is also advanced way of local install described [here](https://opptimizer.readthedocs.io/en/latest/advanced-installation).

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
def module_exec(mod_obj, params, tokenData):
    # Process tokenData
    return tokenData
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

## Examples of Usage
### Basic Pipeline Example

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

## License

This project is licensed under the Apache License 2.0. You may use, modify, and distribute this software freely, provided that you comply with the terms of the license, which include attribution and a disclaimer of warranties. For the full license text, please see [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).