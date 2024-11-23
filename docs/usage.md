## Examples

### Using Lists

```python
from crosszip import crosszip

def concat(a, b, c):
    return f"{a}-{b}-{c}"

list1 = [1, 2]
list2 = ['a', 'b']
list3 = [True, False]

result = crosszip(concat, list1, list2, list3)
print(result)
# Output: ['1-a-True', '1-a-False', '1-b-True', '1-b-False', '2-a-True', '2-a-False', '2-b-True', '2-b-False']
```

### Using Tuples

```python
def add(a, b):
    return a + b

result = crosszip(add, (1, 2), (10, 20))
print(result)
# Output: [11, 21, 12, 22]
```

### Using Sets and Generators

```python
def concat(a, b):
    return f"{a}{b}"

set1 = {1, 2}
gen = (x for x in ["x", "y"])

result = crosszip(concat, set1, gen)
print(result)
# Output: ['1x', '1y', '2x', '2y']
```
