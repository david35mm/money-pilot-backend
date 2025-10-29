import importlib
from pathlib import Path
import pkgutil

from api.models.base import Base

# Auto-import every .py file inside this package (except __init__.py)
package_dir = Path(__file__).resolve().parent
for _, module_name, _ in pkgutil.iter_modules([str(package_dir)]):
  if module_name not in {"__init__", "base"}:
    importlib.import_module(f"api.models.{module_name}")
