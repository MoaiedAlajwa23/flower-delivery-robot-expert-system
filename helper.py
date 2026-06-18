from homework2.facts import *
from experta import *
from homework2.facts import *


class DuplicationRulesMixin(KnowledgeEngine):

    @Rule(
        StateTransition(old_nid=MATCH.old, new_nid=MATCH.new),
        Need(nid=MATCH.old, pid=MATCH.pid, color=MATCH.c, amount=MATCH.amt),
        NOT(Need(nid=MATCH.new, pid=MATCH.pid, color=MATCH.c)),
        salience=2
    )
    def copy_need_to_child(self, new, pid, c, amt):
        self.declare(Need(nid=new, pid=pid, color=c, amount=amt))

    @Rule(
        StateTransition(old_nid=MATCH.old, new_nid=MATCH.new),
        CargoItem(nid=MATCH.old, type=MATCH.t, color=MATCH.c, amount=MATCH.amt),
        NOT(CargoItem(nid=MATCH.new, type=MATCH.t, color=MATCH.c)),
        salience=2
    )
    def copy_cargo_to_child(self, new, t, c, amt):
        self.declare(CargoItem(nid=new, type=t, color=c, amount=amt))

    @Rule(
        StateTransition(old_nid=MATCH.old, new_nid=MATCH.new),
        TotalNeeds(nid=MATCH.old, value=MATCH.v),
        NOT(TotalNeeds(nid=MATCH.new)),
        salience=2
    )
    def copy_total_needs(self, new, v):
        self.declare(TotalNeeds(nid=new, value=v))

    @Rule(
        StateTransition(old_nid=MATCH.old, new_nid=MATCH.new),
        CargoMeta(nid=MATCH.old, current_load=MATCH.cl, mode=MATCH.m, value=MATCH.v),
        NOT(CargoMeta(nid=MATCH.new)),
        salience=2
    )
    def copy_cargo_meta_to_child(self, new, cl, m, v):
        self.declare(CargoMeta(nid=new, current_load=cl, mode=m, value=v))

    @Rule(
        StateTransition(old_nid=MATCH.old, new_nid=MATCH.new),
        Progress(nid=MATCH.old, deliv=MATCH.d),
        NOT(Progress(nid=MATCH.new)),
        salience=2
    )
    def copy_progress_to_child(self, new, d):
        self.declare(Progress(nid=new, deliv=d))

    @Rule(
        AS.st << StateTransition(old_nid=MATCH.old, new_nid=MATCH.new),
        salience=1
    )
    def cleanup_transition(self, st):
        self.retract(st)

    @Rule(
        SystemPhase(step="search"),
        AS.bad_open << OpenNode(nid=MATCH.bad_nid),

        RobotState(nid=MATCH.bad_nid, x=MATCH.x, y=MATCH.y, g=MATCH.bad_g),
        CargoMeta(nid=MATCH.bad_nid, current_load=MATCH.cl, mode=MATCH.m, value=MATCH.v),
        Progress(nid=MATCH.bad_nid, deliv=MATCH.d),

        RobotState(nid=MATCH.good_nid, x=MATCH.x, y=MATCH.y, g=MATCH.good_g),
        CargoMeta(nid=MATCH.good_nid, current_load=MATCH.cl, mode=MATCH.m, value=MATCH.v),
        Progress(nid=MATCH.good_nid, deliv=MATCH.d),

        TEST(lambda bad_nid, good_nid: bad_nid != good_nid),

        TEST(lambda bad_g, good_g: bad_g >= good_g),

        TEST(lambda bad_nid, good_nid, bad_g, good_g: bad_nid > good_nid if bad_g == good_g else True),

        salience=20
    )
    def prune_duplicate_state(self, bad_open, bad_nid, good_nid):
        self.retract(bad_open)

    @Rule(
        SystemPhase(step="search"),
        AS.bad_open << OpenNode(nid=MATCH.bad_nid),

        RobotState(nid=MATCH.bad_nid, x=MATCH.x, y=MATCH.y, g=MATCH.bad_g),
        CargoMeta(nid=MATCH.bad_nid, current_load=MATCH.cl, mode=MATCH.m, value=MATCH.v),
        Progress(nid=MATCH.bad_nid, deliv=MATCH.d),

        RobotState(nid=MATCH.good_nid, x=MATCH.x, y=MATCH.y, g=MATCH.good_g),
        CargoMeta(nid=MATCH.good_nid, current_load=MATCH.cl, mode=MATCH.m, value=MATCH.v),
        Progress(nid=MATCH.good_nid, deliv=MATCH.d),

        TEST(lambda bad_nid, good_nid: bad_nid != good_nid),
        TEST(lambda bad_g, good_g: bad_g >= good_g),
        TEST(lambda bad_nid, good_nid, bad_g, good_g: bad_nid > good_nid if bad_g == good_g else True),

        salience=20
    )
    def prune_duplicate_state(self, bad_open, bad_nid, good_nid):
        self.retract(bad_open)

        self.declare(Visited(nid=bad_nid, state_hash="pruned"))

        print(f" [Pruned] تم حذف العقدة المكررة {bad_nid} لأنها تطابق العقدة {good_nid}")

    @Rule(
        AS.new_node << OpenNode(status='open', nid=MATCH.new_nid, rx=MATCH.rx, ry=MATCH.ry, g=MATCH.g_new),
        OpenNode(status='closed', nid=MATCH.old_nid, rx=MATCH.rx, ry=MATCH.ry, g=MATCH.g_old),
        TEST(lambda g_new, g_old: g_new >= g_old),
        salience=100
    )
    def prune_cycles(self, new_node):
        print(f" [Prune] حذفنا العقدة {new_node['nid']} لأننا زرنا موقعها سابقاً بتكلفة أقل.")
        self.retract(new_node)

    @Rule(
        SystemPhase(step="search"),
        StateTransition(old_nid=MATCH.old, new_nid=MATCH.new),
        CargoMeta(nid=MATCH.old, current_load=MATCH.cl, mode=MATCH.mode, value=MATCH.val),

        NOT(CargoMeta(nid=MATCH.new))
    )
    def duplicate_cargo_meta(self, new, cl, mode, val):
        self.declare(CargoMeta(nid=new, current_load=cl, mode=mode, value=val))


class ReportingRulesMixin(KnowledgeEngine):

    @Rule(
        SystemPhase(step="print_solution"),
        GoalFound(nid=MATCH.g_nid),
        FrontierNode(nid=MATCH.g_nid, parent=MATCH.p, action=MATCH.act)
    )
    def start_backtrack(self, g_nid, p, act):
        self.declare(SolutionPath(nid=g_nid, action=act, step_num=0))
        self.declare(BuildPath(next_nid=p, current_step=1))

    @Rule(
        SystemPhase(step="print_solution"),
        AS.bp << BuildPath(next_nid=MATCH.nid, current_step=MATCH.s),
        FrontierNode(nid=MATCH.nid, parent=MATCH.p, action=MATCH.act),
        TEST(lambda nid: nid != -1)
    )
    def continue_backtrack(self, bp, nid, s, p, act):
        self.retract(bp)
        self.declare(SolutionPath(nid=nid, action=act, step_num=s))
        self.declare(BuildPath(next_nid=p, current_step=s + 1))

    @Rule(
        SystemPhase(step="print_solution"),
        AS.bp << BuildPath(next_nid=-1, current_step=MATCH.total_steps)
    )
    def finish_backtrack(self, bp, total_steps):
        self.retract(bp)

        self.declare(PrintPathSignal(current_step=total_steps - 1))

    @Rule(
        SystemPhase(step="print_solution"),
        AS.sig << PrintPathSignal(current_step=MATCH.s),
        SolutionPath(step_num=MATCH.s, action=MATCH.act, nid=MATCH.nid)
    )
    def print_solution_step(self, sig, s, act, nid):
        self.retract(sig)
        print(f"[step: {s} action: ({act}) id node: {nid}]")

        if s > 0:
            self.declare(PrintPathSignal(current_step=s - 1))
        else:
            print("-" * 60)
            print("print the tree:")
            self.declare(SystemPhase(step="print_tree"))

    @Rule(
        SystemPhase(step="print_tree"),
        FrontierNode(nid=MATCH.nid, f=MATCH.f, parent=MATCH.p, action=MATCH.act, depth=MATCH.d),
        NOT(TreePrinted(nid=MATCH.nid))
    )
    def print_tree_node(self, nid, f, p, act, d):
        self.declare(TreePrinted(nid=nid))
        print(f"  node: {nid} | parent: {p} | the action: {act} | depth: {d} | f: {f}")


    @Rule(
        SystemPhase(step="print_tree"),

        NOT(AND(
            FrontierNode(nid=MATCH.nid),
            NOT(TreePrinted(nid=MATCH.nid))
        )),
        salience=-10
    )
    def end_program(self):
        print("=" * 60)
        print("the [best] path and the tree were printed")
        print("=" * 60)
        self.halt()
