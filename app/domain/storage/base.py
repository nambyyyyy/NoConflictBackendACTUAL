from abc import ABC, abstractmethod
from typing import BinaryIO


class BaseStorage(ABC):
    @abstractmethod
    def save(self, file: BinaryIO, filepath: str) -> str:
        """Сохраняет файл и возвращает путь"""
        pass
    
    @abstractmethod
    def delete(self, filepath: str) -> None:
        """Удаляет файл"""
        pass
    
    @abstractmethod
    def exists(self, filepath: str) -> bool:
        """Проверяет существование файла"""
        pass