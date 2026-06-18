
from homework2.facts import *


class SearchControlMixin(KnowledgeEngine):

    @Rule(
        SystemPhase(step="search"),
        FrontierNode(nid=MATCH.nid, f=MATCH.f),

        TEST(lambda f: f > 0.0),

        NOT(Visited(nid=MATCH.nid)),
        NOT(OpenNode(nid=MATCH.nid)),
        salience=10
    )
    def add_to_open_list(self, nid, f):
        self.declare(OpenNode(nid=nid, f=f))

    @Rule(
        SystemPhase(step="search"),
        NOT(ExpandNext()),

        AS.open_node << OpenNode(nid=MATCH.best_nid, f=MATCH.best_f),

        NOT(OpenNode(f=MATCH.other_f & TEST(lambda other_f, best_f: other_f < best_f))),
        salience=5
    )
    def select_best_state(self, open_node, best_nid, best_f):

        self.retract(open_node)

        self.declare(Visited(nid=best_nid, state_hash=str(best_nid)))
        self.declare(ExpandNext(nid=best_nid))

        print(f"[A* Selection] - Best node selected for expansion: NID {best_nid} with F = {best_f}")

    @Rule(
        SystemPhase(step="search"),
        AS.exp << ExpandNext(nid=MATCH.nid),
        salience=-5
    )
    def clear_expand_next(self, exp, nid):
        self.retract(exp)

