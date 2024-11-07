
# Examples
## Basic Optimization Example

```python
from opptimizer import Opptimizer

def simple_function(x):
    return (x - 3) ** 2

optimizer = Opptimizer()
result = optimizer.optimize(simple_function, range=(-10, 10))
print(f"Optimized result: {result}")
```