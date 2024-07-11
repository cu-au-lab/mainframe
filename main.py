import os
import sys

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from mainframe.__init__ import Mainframe

def main():
    config_path = os.path.join(project_root, "routines", "v1.json")
    mainframe = Mainframe(config_path)
    mainframe.initialize()
    mainframe.run()
    mainframe.shutdown()

if __name__ == "__main__":
    main()
