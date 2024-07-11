import imagej
from typing import List, Dict
from pathlib import Path
from mainframe.kernels.base_kernel import BaseKernel

class FijiInstance:
    def __init__(self, id: int):
        self.id = id
        self.ij = imagej.init()
        self.current_task = None

    def run_macro(self, macro: str, input_files: List[str], output_dir: str) -> None:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        for input_file in input_files:
            input_path = Path(input_file)
            output_path = output_dir / input_path.name
            
            # Open the image
            image = self.ij.io().open(str(input_path))
            
            # Run the macro
            self.ij.py.run_macro(macro)
            
            # Save the processed image
            self.ij.io().save(image, str(output_path))
            
            # Close the image to free up memory
            image.close()

    def close(self) -> None:
        self.ij.dispose()

    def is_available(self) -> bool:
        return self.current_task is None

    def set_task(self, task: dict) -> None:
        self.current_task = task

    def clear_task(self) -> None:
        self.current_task = None

class FijiKernel(BaseKernel):
    def __init__(self, total_instances: int):
        super().__init__(total_instances)

    def initialize(self) -> None:
        self.instances = [FijiInstance(i) for i in range(self.total_instances)]

    def run_task(self, task: Dict) -> None:
        instance = self.get_available_instances(1)[0]
        instance.run_macro(task['macro'], task['inputs'], task['outputs'])

    def get_available_instances(self, count: int) -> List[FijiInstance]:
        return [instance for instance in self.instances if instance.is_available()][:count]

    def shutdown(self) -> None:
        for instance in self.instances:
            instance.close()
