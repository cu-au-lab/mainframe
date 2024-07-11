import os
import sys
import traceback

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from mainframe.__init__ import Mainframe

def main():
    try:
        config_path = os.path.join(project_root, "routines", "v1.json")
        mainframe = Mainframe(config_path)
        mainframe.initialize()
        mainframe.run()
        mainframe.shutdown()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please ensure Fiji is installed and the path is correct.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("Full traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    main()
