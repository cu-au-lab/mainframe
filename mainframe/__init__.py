import os
from pathlib import Path

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

        self.task_scheduler = TaskScheduler(self.kernels)

    def run(self) -> None:
        """Run the Mainframe tasks."""
        if not self.task_scheduler:
            raise RuntimeError("Mainframe not initialized. Call initialize() first.")

        tasks = self.config_manager.get_tasks()
        
        for task in tasks:
            input_dir = Path(task['inputs'])
            output_dir = Path(task['outputs'])
            output_dir.mkdir(parents=True, exist_ok=True)
            
            all_images = list(input_dir.glob('*.png'))
            total_images = len(all_images)
            processed_images = 0

            while processed_images < total_images:
                remaining_images = total_images - processed_images
                batch_size = min(remaining_images, task['capacity'] * task['instances'])
                
                current_batch = all_images[processed_images:processed_images + batch_size]
                
                # Create subtasks for each instance
                subtasks = []
                for i in range(task['instances']):
                    start = i * (batch_size // task['instances'])
                    end = (i + 1) * (batch_size // task['instances'])
                    if i == task['instances'] - 1:
                        end = batch_size  # Ensure all remaining images are included in the last subtask
                    
                    subtask = task.copy()
                    subtask['inputs'] = [str(img) for img in current_batch[start:end]]
                    subtask['outputs'] = str(output_dir)
                    subtasks.append(subtask)
                
                self.task_scheduler.schedule_tasks(subtasks)
                
                processed_images += batch_size
                print(f"Processed {processed_images}/{total_images} images for task: {task['name']}")

    def shutdown(self) -> None:
        """Shutdown Mainframe."""
        if self.task_scheduler:
            self.task_scheduler.shutdown()

# Example usage
if __name__ == "__main__":
    mainframe = Mainframe("routines/v1.json")
    mainframe.initialize()
    mainframe.run()
    mainframe.shutdown()
