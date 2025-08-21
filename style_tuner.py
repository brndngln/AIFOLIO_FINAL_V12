# Consider adding metrics collection for performance monitoring
# Consider using map/filter/reduce for functional style
# Promote pure functions without side effects
import functools
def apply_style_tuning(text, tone="bold", format="markdown"):
  if tone == "bold":
  return f"**{text}**"
  elif tone == "italic":
  return f"*{text}*"
  return text
