from .core.config_manager import ConfigManager
from .core.task_scheduler import TaskScheduler
from .kernels.fiji.fiji import FijiKernel

class Mainframe:
    def __init__(self, config_path: str):
        self.config_manager = ConfigManager(config_path)
        self.kernels = {}
        self.task_scheduler = None

    def initialize(self) -> None:
        """Initialize Mainframe by loading config and setting up kernels."""
        self.config_manager.load_config()
        self.config_manager.validate_config()

        utilities = self.config_manager.get_utilities()
        for utility in utilities:
            if utility == 'fiji':
                total_instances = sum(task['instances'] for task in self.config_manager.get_tasks() if task['utility'] == 'fiji')
                fiji_kernel = FijiKernel(total_instances)
                fiji_kernel.initialize()
                self.kernels['fiji'] = fiji_kernel
            # Add more utility types here later

        self.task_scheduler = TaskScheduler(self.kernels)

    def run(self) -> None:
        """Run the Mainframe tasks."""
        if not self.task_scheduler:
            raise RuntimeError("Mainframe not initialized. Call initialize() first.")

        tasks = self.config_manager.get_tasks()
        self.task_scheduler.schedule_tasks(tasks)

    def shutdown(self) -> None:
        """Shutdown Mainframe."""
        if self.task_scheduler:
            self.task_scheduler.shutdown()

# Example usage
if __name__ == "__main__":
    mainframe = Mainframe("configs/routine.json")
    mainframe.initialize()
    mainframe.run()
    mainframe.shutdown()