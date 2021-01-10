from typing import Any, Callable, Dict, Type, TypeVar
from pydantic import BaseModel

Model = TypeVar('Model', bound=BaseModel)
Provider = Callable[[Type[Model]], Dict[str, Any]]
