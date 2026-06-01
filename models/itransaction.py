from abc import ABC, abstractmethod


class ITransaction(ABC):
    @abstractmethod
    def print_receipt(self) -> None:
        pass
