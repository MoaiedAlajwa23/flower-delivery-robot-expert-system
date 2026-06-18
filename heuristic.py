from homework2.facts import *

class HeuristicRulesMixin(KnowledgeEngine):

    @Rule(
        SystemPhase(step="search"),

        AS.fn << FrontierNode(nid=MATCH.nid, f=0.0, parent=MATCH.p),
        TEST(lambda nid: nid != 0),

        RobotState(nid=MATCH.nid, x=MATCH.rx, y=MATCH.ry, g=MATCH.g),
        Warehouse(x=MATCH.wx, y=MATCH.wy),
        MaxLoad(value=MATCH.max_l),
        TotalNeeds(nid=MATCH.nid, value=MATCH.needs),
        StaticDavg(value=MATCH.d_avg),

        CargoMeta(nid=MATCH.nid, current_load=0)
    )
    def calculate_f_empty(self, fn, rx, ry, g, wx, wy, max_l, needs, d_avg):
        d_rw = abs(rx - wx) + abs(ry - wy)

        trips = (needs + max_l - 1) // max_l if max_l > 0 else 0

        if trips > 0:
            h = d_rw + (trips - 1) * (2 * d_avg + 2) + d_avg + 2
        else:
            h = 0

        f_score = g + h

        self.modify(fn, f=float(f_score))

    @Rule(
        SystemPhase(step="search"),

        AS.fn << FrontierNode(nid=MATCH.nid, f=0.0, parent=MATCH.p),
        TEST(lambda nid: nid != 0),

        RobotState(nid=MATCH.nid, g=MATCH.g),
        MaxLoad(value=MATCH.max_l),
        TotalNeeds(nid=MATCH.nid, value=MATCH.needs),
        StaticDavg(value=MATCH.d_avg),

        CargoMeta(nid=MATCH.nid, current_load=MATCH.cl),
        TEST(lambda cl: cl > 0)
    )
    def calculate_f_loaded(self, fn, g, max_l, needs, d_avg):
        trips = (needs + max_l - 1) // max_l if max_l > 0 else 0

        if trips > 0:
            h = (trips - 1) * (2 * d_avg + 2) + d_avg + 2
        else:
            h = 0

        f_score = g + h

        self.modify(fn, f=float(f_score))