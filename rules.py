from homework2.facts import *

class MovementRulesMixin1(KnowledgeEngine):
    @Rule(
        SystemPhase(step="search"),
        ExpandNext(nid=MATCH.p_nid),
        FrontierNode(nid=MATCH.p_nid, depth=MATCH.d),
        MaxDepth(value=MATCH.max_d),
        TEST(lambda d, max_d: d < max_d),
        RobotState(nid=MATCH.p_nid, x=MATCH.x, y=MATCH.y, g=MATCH.g),
        Grid(width=MATCH.w),
        TEST(lambda x, w: x < w),
        NOT(ActionEvaluated(nid=MATCH.p_nid, action="move_right")),
        AS.counter << StateCounter(value=MATCH.new_nid)
    )
    def move_right(self, p_nid, d, x, y, g, counter, new_nid):
        self.declare(ActionEvaluated(nid=p_nid, action="move_right"))
        self.modify(counter, value=new_nid + 1)
        self.declare(RobotState(nid=new_nid, x=x + 1, y=y, g=g + 1))
        self.declare(FrontierNode(nid=new_nid, f=0.0, parent=p_nid, action="move_right", depth=d + 1))
        self.declare(StateTransition(old_nid=p_nid, new_nid=new_nid))

        print("New child state generated successfully.")
        print(f"   - Parent Node (NID: {p_nid}): Robot was at (X:{x}, Y:{y})")
        print("   - Action Executed: Move Right (move_right)")
        print(f"   - Child Node (NID: {new_nid}): Robot is now at (X:{x+1}, Y:{y})")
        print(f"   - Actual Cost (g) is now: {g+1}")
        print("-" * 50)


    @Rule(

        SystemPhase(step="search"),
        ExpandNext(nid=MATCH.p_nid),

        FrontierNode(nid=MATCH.p_nid, depth=MATCH.d),
        MaxDepth(value=MATCH.max_d),
        TEST(lambda d, max_d: d < max_d),

        RobotState(nid=MATCH.p_nid, x=MATCH.x, y=MATCH.y, g=MATCH.g),

        TEST(lambda x: x > 0),

        NOT(ActionEvaluated(nid=MATCH.p_nid, action="move_left")),

        AS.counter << StateCounter(value=MATCH.new_nid)
    )
    def move_left(self, p_nid, d, x, y, g, counter, new_nid):

        self.declare(ActionEvaluated(nid=p_nid, action="move_left"))

        self.modify(counter, value=new_nid + 1)

        self.declare(RobotState(nid=new_nid, x=x - 1, y=y, g=g + 1))

        self.declare(FrontierNode(
            nid=new_nid,
            f=0.0,
            parent=p_nid,
            action="move_left",
            depth=d + 1
        ))

        self.declare(StateTransition(old_nid=p_nid, new_nid=new_nid))

        print("New child state generated successfully.")
        print(f"   - Parent Node (NID: {p_nid}): Robot was at (X:{x}, Y:{y})")
        print("   - Action Executed: Move Left (move_left)")
        print(f"   - Child Node (NID: {new_nid}): Robot is now at (X:{x-1}, Y:{y})")
        print(f"   - Actual Cost (g) is now: {g+1}")
        print("-" * 50)


    @Rule(
        SystemPhase(step="search"),
        ExpandNext(nid=MATCH.p_nid),

        FrontierNode(nid=MATCH.p_nid, depth=MATCH.d),
        MaxDepth(value=MATCH.max_d),
        TEST(lambda d, max_d: d < max_d),

        RobotState(nid=MATCH.p_nid, x=MATCH.x, y=MATCH.y, g=MATCH.g),

        TEST(lambda y: y > 0),

        NOT(ActionEvaluated(nid=MATCH.p_nid, action="move_down")),
        AS.counter << StateCounter(value=MATCH.new_nid)
    )
    def move_down(self, p_nid, d, x, y, g, counter, new_nid):
        self.declare(ActionEvaluated(nid=p_nid, action="move_down"))
        self.modify(counter, value=new_nid + 1)

        self.declare(RobotState(nid=new_nid, x=x, y=y - 1, g=g + 1))

        self.declare(FrontierNode(
            nid=new_nid,
            f=0.0,
            parent=p_nid,
            action="move_down",
            depth=d + 1
        ))

        self.declare(StateTransition(old_nid=p_nid, new_nid=new_nid))

        print("New child state generated successfully.")
        print(f"   - Parent Node (NID: {p_nid}): Robot was at (X:{x}, Y:{y})")
        print("   - Action Executed: Move Down (move_down)")
        print(f"   - Child Node (NID: {new_nid}): Robot is now at (X:{x}, Y:{y-1})")
        print(f"   - Actual Cost (g) is now: {g+1}")
        print("-" * 50)


    @Rule(
        SystemPhase(step="search"),
        ExpandNext(nid=MATCH.p_nid),

        FrontierNode(nid=MATCH.p_nid, depth=MATCH.d),
        MaxDepth(value=MATCH.max_d),
        TEST(lambda d, max_d: d < max_d),

        RobotState(nid=MATCH.p_nid, x=MATCH.x, y=MATCH.y, g=MATCH.g),

        Grid(height=MATCH.h),
        TEST(lambda y, h: y < h),

        NOT(ActionEvaluated(nid=MATCH.p_nid, action="move_up")),
        AS.counter << StateCounter(value=MATCH.new_nid)
    )
    def move_up(self, p_nid, d, x, y, g, h, counter, new_nid):
        self.declare(ActionEvaluated(nid=p_nid, action="move_up"))
        self.modify(counter, value=new_nid + 1)

        self.declare(RobotState(nid=new_nid, x=x, y=y + 1, g=g + 1))

        self.declare(FrontierNode(
            nid=new_nid,
            f=0.0,
            parent=p_nid,
            action="move_up",
            depth=d + 1
        ))

        self.declare(StateTransition(old_nid=p_nid, new_nid=new_nid))

        print("New child state generated successfully.")
        print(f"   - Parent Node (NID: {p_nid}): Robot was at (X:{x}, Y:{y})")
        print("   - Action Executed: Move Up (move_up)")
        print(f"   - Child Node (NID: {new_nid}): Robot is now at (X:{x}, Y:{y+1})")
        print(f"   - Actual Cost (g) is now: {g+1}")
        print("-" * 50)




    @Rule(
        SystemPhase(step="init_maxload"),
        Need(nid=0, pid=MATCH.pid, color=MATCH.c, amount=MATCH.amt),

        NOT(NeedCounted(pid=MATCH.pid, color=MATCH.c)),
        AS.pt << PavilionTotal(pid=MATCH.pid, total=MATCH.t)
    )
    def count_pavilion_need(self, pid, c, amt, pt, t):
        self.declare(NeedCounted(pid=pid, color=c))
        self.modify(pt, total=t + amt)

    @Rule(
        SystemPhase(step="init_maxload"),
        PavilionTotal(total=MATCH.t),
        AS.ml << MaxLoad(value=MATCH.m),
        TEST(lambda t, m: t > m)
    )
    def update_max_load(self, t, ml):

        self.modify(ml, value=t)

    @Rule(
        AS.phase << SystemPhase(step="init_maxload"),
        MaxLoad(value=MATCH.m),
        salience=-20
    )
    def switch_to_search(self, phase, m):
        print("=" * 50)
        print(f"[System Init] تم حساب السعة القصوى للروبوت ديناميكياً: MaxLoad = {m}")
        print("=" * 50 + "\n")

        self.modify(phase, step="search")
