import inspect
from typing import Callable, List

from signals.connection import Connection


class Signal:
    connections: List[Connection]

    def __init__(self) -> None:
        self.connections = []

    def connect(self, fn: Callable) -> "Signal":
        connection = Connection(fn)

        if connection in self.connections:
            self.connections.pop(self.connections.index(connection))
            self.connections.append(connection)
            return self

        self.connections.append(connection)

        return self

    def emit(self, *args, **kwargs) -> None:
        if not self.connections:
            return

        for connection in self.connections:
            if connection.args or connection.kwargs:
                args = connection.args
                kwargs = connection.kwargs

            sigargs, _, _, defaults, _, _, _ = inspect.getfullargspec(connection.callable)

            for item in ("self", "cls"):
                if item in sigargs:
                    sigargs.remove(item)

            args = args[: len(sigargs)]

            if defaults:
                args = args[: -len(defaults)]

            for key in list(kwargs.keys()):
                if key not in sigargs:
                    del kwargs[key]

            connection.callable(*args, **kwargs)

    def disconnect(self, fn: Callable) -> None:
        for connection in self.connections:
            if connection.callable == fn:
                self.connections.remove(connection)

    def bind(self, *args, **kwargs) -> "Signal":
        self.connections[-1].set_arguments(*args, **kwargs)

        return self
