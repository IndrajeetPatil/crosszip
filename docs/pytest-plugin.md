## crosszip parametrization

After installing the package, you can use the `crosszip_parametrize` marker to parametrize your tests with multiple parameters.
This marker is a pytest plugin that allows you to define parameter names and their corresponding values in a single line.

```python
# confest.py
pytest_plugins = ["crosszip.plugin"]
```

### Basic Usage

The `crosszip_parametrize` marker allows you to define parameter names and their corresponding values:

```python
import pytest

@pytest.mark.crosszip_parametrize("a", [1, 2], "b", [3, 4])
def test_example(a, b):
    assert (a, b) in [(1, 3), (1, 4), (2, 3), (2, 4)]
```

### Realistic Use Cases for `crosszip_parametrize`

#### Testing Mathematical Functions

```python
import math

@pytest.mark.crosszip_parametrize(
    "base", [2, 10],
    "exponent", [-1, 0, 1],
)
def test_power_function(base, exponent):
    result = math.pow(base, exponent)
    assert result == base ** exponent
```

#### Testing API Endpoints

```python
@pytest.mark.crosszip_parametrize(
    "role", ["admin", "user"],
    "http_method", ["GET", "POST", "DELETE"],
)
def test_api_access_control(role, http_method):
    result = simulate_api_call(role=role, method=http_method)
    if role == "admin":
        assert result["status"] == "success"
    else:
        assert result["status"] == "error" if http_method == "DELETE" else "success"
```

#### Testing Form Validation

```python
@pytest.mark.crosszip_parametrize(
    "email", ["valid@example.com", "invalid@", ""],
    "password", ["correct-password", "short", ""],
)
def test_form_validation(email, password):
    result = validate_form(email=email, password=password)
    if "@" not in email or not email:
        assert result["email_error"] == "Invalid email address"
    elif len(password) < 8 or not password:
        assert result["password_error"] == "Password too short"
    else:
        assert result["status"] == "success"
```

#### Testing Localization Support

```python
@crosszip_parametrize(
    "language", ["en", "es", "fr"],
    "platform", ["web", "mobile"],
)
def test_localized_error_messages(language, platform):
    result = get_localized_message("ERROR_INVALID_INPUT", language, platform)
    if language == "en":
        assert result == "Invalid input"
    elif language == "es":
        assert result == "Entrada no válida"
    elif language == "fr":
        assert result == "Entrée non valide"
```