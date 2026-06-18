from experta import *

class Grid(Fact):
    width = Field(int, mandatory=True)
    height = Field(int, mandatory=True)

class Warehouse(Fact):
    x = Field(int, mandatory=True)
    y = Field(int, mandatory=True)

class Progress(Fact):
    nid = Field(int, mandatory=True)
    deliv = Field(int, mandatory=True)

class MaxLoad(Fact):
    value = Field(int, mandatory=True)

class MaxDepth(Fact):
    value = Field(int, mandatory=True)

class Pavilion(Fact):
    pid = Field(str, mandatory=True)
    x = Field(int, mandatory=True)
    y = Field(int, mandatory=True)
    type = Field(str, mandatory=True)

class RobotState(Fact):
    nid = Field(int, mandatory=True)
    x = Field(int, mandatory=True)
    y = Field(int, mandatory=True)
    g = Field(int, default=0)

class Need(Fact):
    nid = Field(int, mandatory=True)
    pid = Field(str, mandatory=True)
    color = Field(str, mandatory=True)
    amount = Field(int, mandatory=True)

class CargoItem(Fact):
    nid = Field(int, mandatory=True)
    type = Field(str, mandatory=True)
    color = Field(str, mandatory=True)
    amount = Field(int, mandatory=True)

class FrontierNode(Fact):
    nid = Field(int, mandatory=True)
    f = Field(float, mandatory=True)
    parent = Field(int, default=-1)
    action = Field(str, default="start")
    depth = Field(int, default=0)

class BestFrontier(Fact):
    nid = Field(int, mandatory=True)
    f = Field(float, mandatory=True)

class ExpandNext(Fact):
    nid = Field(int, mandatory=True)

class Visited(Fact):
    nid = Field(int, mandatory=True)
    state_hash = Field(str, mandatory=True)

class GoalFound(Fact):
    pass


class PavilionTotal(Fact):

    pid = Field(str, mandatory=True)
    total = Field(int, mandatory=True)

class NeedCounted(Fact):

    pid = Field(str, mandatory=True)
    color = Field(str, mandatory=True)
#=========================================
class StateCounter(Fact):

    value = Field(int, mandatory=True)

class ActionEvaluated(Fact):

    nid = Field(int, mandatory=True)
    action = Field(str, mandatory=True)

class StateTransition(Fact):

    old_nid = Field(int, mandatory=True)
    new_nid = Field(int, mandatory=True)


class SystemPhase(Fact):

    step = Field(str, mandatory=True)

class CargoMeta(Fact):

    nid = Field(int, mandatory=True)
    current_load = Field(int, default=0)
    mode = Field(str, default="none")
    value = Field(str, default="none")

class LoadEvaluated(Fact):

    nid = Field(int, mandatory=True)
    pid = Field(str, mandatory=True)
    color = Field(str, mandatory=True)
    mode = Field(str, mandatory=True)

class UnloadEvaluated(Fact):
    nid = Field(int, mandatory=True)
    pid = Field(str, mandatory=True)
    color = Field(str, mandatory=True)

class SolutionPath(Fact):
    nid = Field(int, mandatory=True)
    action = Field(str, mandatory=True)
    step_num = Field(int, mandatory=True)

class BuildPath(Fact):
    next_nid = Field(int, mandatory=True)
    current_step = Field(int, mandatory=True)

class PrintPathSignal(Fact):
    current_step = Field(int, mandatory=True)

class TreePrinted(Fact):
    nid = Field(int, mandatory=True)

class TotalNeeds(Fact):

    nid = Field(int, mandatory=True)
    value = Field(int, mandatory=True)

class StaticDavg(Fact):

    value = Field(int, mandatory=True)

class OpenNode(Fact):
    nid = Field(int, mandatory=True)
    f = Field(float, mandatory=True)


