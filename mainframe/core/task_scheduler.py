from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor
from mainframe.kernels.base_kernel import BaseKernel

class TaskScheduler:
    def __init__(self, kernels: Dict[str, BaseKernel]):
        self.kernels = kernels
        self.executor = ThreadPoolExecutor(max_workers=sum(kernel.total_instances for kernel in kernels.values()))

    def schedule_tasks(self, tasks: List[Dict]) -> None:
        """Schedule and run tasks on available kernel instances."""
        for task in tasks:
            utility = task['utility']
            if utility not in self.kernels:
                print(f"Warning: No kernel available for utility {utility}. Skipping task {task['name']}.")
                continue

            kernel = self.kernels[utility]
            instances_needed = task['instances']
            available_instances = kernel.get_available_instances(instances_needed)

            if len(available_instances) < instances_needed:
                print(f"Warning: Not enough available instances for task {task['name']}. Using {len(available_instances)} instances.")

            for instance in available_instances:
                instance.set_task(task)
                self.executor.submit(self.run_task, instance, task)

    def run_task(self, instance: BaseKernel, task: Dict) -> None:
        """Run a task on a specific kernel instance."""
        try:
            instance.run_task(task)
        finally:
            instance.clear_task()

    def shutdown(self) -> None:
        """Shutdown all kernel instances and the executor."""
        for kernel in self.kernels.values():
            kernel.shutdown()
        self.executor.shutdown()
