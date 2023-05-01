

# Decorator example

def logger(func):
  def wrapper(*args, **kwargs):
    print(f"Calling {func.__name__} with args {args} and kwargs {kwargs}")
    result = func(*args, **kwargs)
    print(f"{func.__name__} returned {result}")
    return result
  return wrapper

# Use the decorator to add logging to a function
@logger
def add(x, y):
  return x + y

# Call the decorated function
add(3, 4)
