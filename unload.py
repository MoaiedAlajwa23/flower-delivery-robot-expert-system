
from homework2.facts import *


class UnloadingRulesMixin(KnowledgeEngine):

    @Rule(
        SystemPhase(step="search"),
        ExpandNext(nid=MATCH.p_nid),
        RobotState(nid=MATCH.p_nid, x=MATCH.rx, y=MATCH.ry, g=MATCH.g),
        Pavilion(pid=MATCH.pid, x=MATCH.rx, y=MATCH.ry, type=MATCH.ptype),

        CargoItem(nid=MATCH.p_nid, type=MATCH.ptype, color=MATCH.c, amount=MATCH.cargo_amt),
        Need(nid=MATCH.p_nid, pid=MATCH.pid, color=MATCH.c, amount=MATCH.need_amt),

        Progress(nid=MATCH.p_nid, deliv=MATCH.d),
        TotalNeeds(nid=MATCH.p_nid, value=MATCH.tot_needs),

        TEST(lambda need_amt: need_amt > 0),
        TEST(lambda cargo_amt, need_amt: cargo_amt > need_amt),

        NOT(UnloadEvaluated(nid=MATCH.p_nid, pid=MATCH.pid, color=MATCH.c)),
        AS.counter << StateCounter(value=MATCH.new_nid)
    )
    def start_unload_with_leftover(self, p_nid, rx, ry, g, pid, ptype, c, cargo_amt, need_amt, d, tot_needs, counter,
                                   new_nid):

        print("pav:"+pid)
        self.declare(UnloadEvaluated(nid=p_nid, pid=pid, color=c))
        self.modify(counter, value=new_nid + 1)

        self.declare(RobotState(nid=new_nid, x=rx, y=ry, g=g + 1))
        self.declare(Need(nid=new_nid, pid=pid, color=c, amount=0))

        # تحديث العدادات للعقدة الجديدة
        self.declare(Progress(nid=new_nid, deliv=d + need_amt))
        self.declare(TotalNeeds(nid=new_nid, value=tot_needs - need_amt))

        self.declare(CargoItem(nid=new_nid, type=ptype, color=c, amount=cargo_amt - need_amt))

        self.declare(FrontierNode(nid=new_nid, f=0.0, parent=p_nid, action=f"Unload_{c}_at_{pid}", depth=1))
        self.declare(StateTransition(old_nid=p_nid, new_nid=new_nid))

        print(
            f"[Initial Unload] - Node {new_nid}: Need for color ({c}) fulfilled for pavilion {pid}. Cost increased to: {g + 1}")

    @Rule(
        SystemPhase(step="search"),
        ExpandNext(nid=MATCH.p_nid),
        RobotState(nid=MATCH.p_nid, x=MATCH.rx, y=MATCH.ry, g=MATCH.g),
        Pavilion(pid=MATCH.pid, x=MATCH.rx, y=MATCH.ry, type=MATCH.ptype),

        CargoItem(nid=MATCH.p_nid, type=MATCH.ptype, color=MATCH.c, amount=MATCH.cargo_amt),
        Need(nid=MATCH.p_nid, pid=MATCH.pid, color=MATCH.c, amount=MATCH.need_amt),

        Progress(nid=MATCH.p_nid, deliv=MATCH.d),
        TotalNeeds(nid=MATCH.p_nid, value=MATCH.tot_needs),

        TEST(lambda need_amt: need_amt > 0),
        TEST(lambda cargo_amt, need_amt: cargo_amt == need_amt),

        NOT(UnloadEvaluated(nid=MATCH.p_nid, pid=MATCH.pid, color=MATCH.c)),
        AS.counter << StateCounter(value=MATCH.new_nid)
    )
    def start_unload_exact_match(self, p_nid, rx, ry, g, pid, ptype, c, need_amt, d, tot_needs, counter, new_nid):
        print("pav:"+pid)
        self.declare(UnloadEvaluated(nid=p_nid, pid=pid, color=c))
        self.modify(counter, value=new_nid + 1)

        self.declare(RobotState(nid=new_nid, x=rx, y=ry, g=g + 1))
        self.declare(Need(nid=new_nid, pid=pid, color=c, amount=0))

        self.declare(Progress(nid=new_nid, deliv=d + need_amt))
        self.declare(TotalNeeds(nid=new_nid, value=tot_needs - need_amt))

        self.declare(FrontierNode(nid=new_nid, f=0.0, parent=p_nid, action=f"Unload_{c}_at_{pid}", depth=1))
        self.declare(StateTransition(old_nid=p_nid, new_nid=new_nid))

        print(
            f"[Initial Unload (Exact)] - Node {new_nid}: Need for color ({c}) fulfilled for pavilion {pid}. Cost increased to: {g + 1}")

    @Rule(
        SystemPhase(step="search"),
        ExpandNext(nid=MATCH.p_nid),
        RobotState(nid=MATCH.p_nid, x=MATCH.rx, y=MATCH.ry, g=MATCH.g),
        Pavilion(pid=MATCH.pid, x=MATCH.rx, y=MATCH.ry, type=MATCH.ptype),

        CargoItem(nid=MATCH.p_nid, type=MATCH.ptype, color=MATCH.c, amount=MATCH.cargo_amt),
        Need(nid=MATCH.p_nid, pid=MATCH.pid, color=MATCH.c, amount=MATCH.need_amt),

        Progress(nid=MATCH.p_nid, deliv=MATCH.d),
        TotalNeeds(nid=MATCH.p_nid, value=MATCH.tot_needs),

        TEST(lambda need_amt: need_amt > 0),
        TEST(lambda cargo_amt, need_amt: cargo_amt > need_amt),

        NOT(UnloadEvaluated(nid=MATCH.p_nid, pid=MATCH.pid, color=MATCH.c)),
        AS.counter << StateCounter(value=MATCH.new_nid)
    )
    def continue_unload_with_leftover(self, p_nid, rx, ry, g, pid, ptype, c, cargo_amt, need_amt, d, tot_needs, counter,
                                      new_nid):
        print("pav:"+pid)
        self.declare(UnloadEvaluated(nid=p_nid, pid=pid, color=c))
        self.modify(counter, value=new_nid + 1)

        self.declare(RobotState(nid=new_nid, x=rx, y=ry, g=g))
        self.declare(Need(nid=new_nid, pid=pid, color=c, amount=0))

        self.declare(Progress(nid=new_nid, deliv=d + need_amt))
        self.declare(TotalNeeds(nid=new_nid, value=tot_needs - need_amt))

        self.declare(CargoItem(nid=new_nid, type=ptype, color=c, amount=cargo_amt - need_amt))

        self.declare(FrontierNode(nid=new_nid, f=0.0, parent=p_nid, action=f"Unload_Extra_{c}_at_{pid}", depth=1))
        self.declare(StateTransition(old_nid=p_nid, new_nid=new_nid))

        print(
            f"[Consecutive Unload] - Node {new_nid}: Additional need for color ({c}) fulfilled in pavilion {pid}. Cost remains at: {g}")

    @Rule(
        SystemPhase(step="search"),
        ExpandNext(nid=MATCH.p_nid),
        RobotState(nid=MATCH.p_nid, x=MATCH.rx, y=MATCH.ry, g=MATCH.g),
        Pavilion(pid=MATCH.pid, x=MATCH.rx, y=MATCH.ry, type=MATCH.ptype),

        CargoItem(nid=MATCH.p_nid, type=MATCH.ptype, color=MATCH.c, amount=MATCH.cargo_amt),
        Need(nid=MATCH.p_nid, pid=MATCH.pid, color=MATCH.c, amount=MATCH.need_amt),

        Progress(nid=MATCH.p_nid, deliv=MATCH.d),
        TotalNeeds(nid=MATCH.p_nid, value=MATCH.tot_needs),

        TEST(lambda need_amt: need_amt > 0),
        TEST(lambda cargo_amt, need_amt: cargo_amt == need_amt),

        NOT(UnloadEvaluated(nid=MATCH.p_nid, pid=MATCH.pid, color=MATCH.c)),
        AS.counter << StateCounter(value=MATCH.new_nid)
    )
    def continue_unload_exact_match(self, p_nid, rx, ry, g, pid, ptype, c, need_amt, d, tot_needs, counter, new_nid):
        print("pav:"+pid)
        self.declare(UnloadEvaluated(nid=p_nid, pid=pid, color=c))
        self.modify(counter, value=new_nid + 1)

        self.declare(RobotState(nid=new_nid, x=rx, y=ry, g=g))
        self.declare(Need(nid=new_nid, pid=pid, color=c, amount=0))

        # تحديث العدادات للعقدة الجديدة
        self.declare(Progress(nid=new_nid, deliv=d + need_amt))
        self.declare(TotalNeeds(nid=new_nid, value=tot_needs - need_amt))

        self.declare(FrontierNode(nid=new_nid, f=0.0, parent=p_nid, action=f"Unload_Extra_{c}_at_{pid}", depth=1))
        self.declare(StateTransition(old_nid=p_nid, new_nid=new_nid))

        print(
            f"[Consecutive Unload (Exact)] - Node {new_nid}: Additional need for color ({c}) fulfilled in pavilion {pid}. Cost remains at: {g}")


