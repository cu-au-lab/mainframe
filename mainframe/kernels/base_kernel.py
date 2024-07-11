from abc import ABC, abstractmethod
from typing import List, Dict

class BaseKernel(ABC):
    def __init__(self, total_instances: int):
        self.total_instances = total_instances
        self.instances = []

    @abstractmethod
    def initialize(self) -> None:
        """Initialize the kernel and create instances."""
        pass

    @abstractmethod
    def run_task(self, task: Dict) -> None:
        """Run a task on this kernel."""
        pass

    @abstractmethod
    def get_available_instances(self, count: int) -> List:
        """Get a list of available instances."""
        pass

    @abstractmethod
    def shutdown(self) -> None:
        """Shutdown all instances of this kernel."""
        pass
