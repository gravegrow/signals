from dataclasses import dataclass, field
from typing import Callable, Dict, Tuple


@dataclass
class Connection:
    callable: Callable

    _args: Tuple = field(init=False, default_factory=lambda: ())
    _kwargs: Dict = field(init=False, default_factory=lambda: {})

    def set_arguments(self, *args, **kwargs) -> "Connection":
        self._args = args
        self._kwargs = kwargs
        return self

    @property
    def args(self):
        return self._args

    @property
    def kwargs(self):
        return self._kwargs
