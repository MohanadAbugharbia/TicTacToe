from typing import Protocol


class Socket_Protocol(Protocol):
    def recv(self) -> None:
        ...
    def send(self) -> None:
        ...
    def close(self) -> None:
        ...
