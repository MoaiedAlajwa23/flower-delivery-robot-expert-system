from homework2.helper import DuplicationRulesMixin
from homework2.helper import ReportingRulesMixin
from homework2.heuristic import HeuristicRulesMixin
from homework2.initial_state import InitialStateMixin1
from homework2.monitor import DebugMonitor
from homework2.rules import MovementRulesMixin1
from homework2.facts import *
from homework2.load import LoadingRulesMixin
from homework2.search import SearchRulesMixin
from homework2.search_control import SearchControlMixin
from homework2.unload import UnloadingRulesMixin


class FlowerRobotEngine1(InitialStateMixin1, MovementRulesMixin1, DuplicationRulesMixin,LoadingRulesMixin,UnloadingRulesMixin,DebugMonitor,SearchRulesMixin,ReportingRulesMixin,HeuristicRulesMixin,SearchControlMixin):

    def __init__(self):
        super().__init__()

if __name__ == "__main__":
    engine = FlowerRobotEngine1()
    engine.reset()

    engine.declare(SystemPhase(step="search"))

    print("Finding the best path with A*...")
    print("waiting...\n")

    engine.run()