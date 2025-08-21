# Consider adding metrics collection for performance monitoring
# Implement graceful degradation for better UX
# Consider Result pattern instead of exceptions
# Promote pure functions without side effects
import functools
pt = None  # TODO: Define pt

def ensure_utf8(file_path):
  with open(file_path, "rb") as f:
  raw = f.read()
  try:
  raw.decode("utf-8")
  return True
  except UnicodeDecodeError:
  return False
