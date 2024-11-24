## Basic Usage

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
from crosszip import crosszip

def add(a, b):
    return a + b

result = crosszip(add, (1, 2), (10, 20))
print(result)
# Output: [11, 21, 12, 22]
```

### Using Sets and Generators

```python
from crosszip import crosszip

def concat(a, b):
    return f"{a}{b}"

set1 = {1, 2}
gen = (x for x in ["x", "y"])

result = crosszip(concat, set1, gen)
print(result)
# Output: ['1x', '1y', '2x', '2y']
```

!!! danger

    Depending on the size of the input iterables, the output of `crosszip` can grow exponentially.<br>
    Use with caution when working with large inputs.

## Real-World Examples

### Label Generation for Machine Learning

```python
from crosszip import crosszip

def create_label(category, subcategory, version):
    return f"{category}_{subcategory}_v{version}"

categories = ["cat", "dog"]
subcategories = ["small", "large"]
versions = ["1.0", "2.0"]

labels = crosszip(create_label, categories, subcategories, versions)
print(labels)
# Output: ['cat_small_v1.0', 'cat_small_v2.0', 'cat_large_v1.0', 'cat_large_v2.0', 'dog_small_v1.0', 'dog_small_v2.0', 'dog_large_v1.0', 'dog_large_v2.0']
```

### Generating SQL Query Conditions

```python
from crosszip import crosszip

def create_condition(column, operator, value):
    return f"{column} {operator} {value}"

columns = ["age", "salary"]
operators = [">", "<"]
values = [30, 50000]

conditions = crosszip(create_condition, columns, operators, values)
print(conditions)
# Output: ['age > 30', 'age > 50000', 'age < 30', 'age < 50000', ...]
```

### Combining Colors and Textures for Design

```python
from crosszip import crosszip

def create_design(color, texture):
    return f"{color} with {texture} texture"

colors = ["red", "blue"]
textures = ["smooth", "rough"]

designs = crosszip(create_design, colors, textures)
print(designs)
# Output: ['red with smooth texture', 'red with rough texture', 'blue with smooth texture', 'blue with rough texture']
```
