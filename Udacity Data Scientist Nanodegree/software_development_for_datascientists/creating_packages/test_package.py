import importlib

def test_package_exists():
    """Check if the module containing simple_function exists."""
    assert importlib.util.find_spec("simple") is not None, "Module not found"

def test_simple_function_call():
    """Call simple_function to ensure it runs without errors."""
    from simple import function
    function.simple_function()
