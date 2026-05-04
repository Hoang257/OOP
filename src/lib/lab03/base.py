import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[3]

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


from src.lib.lab01.model import Athlete as Lab01Athlete


class Athlete(Lab01Athlete):
    def training_load(self):
        return self.num_visiting

    def display(self):
        print(self)
