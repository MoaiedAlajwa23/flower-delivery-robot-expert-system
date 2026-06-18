from homework2 import *

class LoadingRulesMixin(KnowledgeEngine):

    @Rule(
        SystemPhase(step="search"),
        ExpandNext(nid=MATCH.p_nid),

        RobotState(nid=MATCH.p_nid, x=MATCH.rx, y=MATCH.ry, g=MATCH.g),
        Warehouse(x=MATCH.rx, y=MATCH.ry),

        CargoMeta(nid=MATCH.p_nid, current_load=0, mode="none"),

        Need(nid=MATCH.p_nid, pid=MATCH.pid, color=MATCH.c, amount=MATCH.amt),
        Pavilion(pid=MATCH.pid, type=MATCH.ptype),
        TEST(lambda amt: amt > 0),

        MaxLoad(value=MATCH.max_l),
        TEST(lambda amt, max_l: amt <= max_l),

        NOT(LoadEvaluated(nid=MATCH.p_nid, pid=MATCH.pid, color=MATCH.c, mode="color")),
        AS.counter << StateCounter(value=MATCH.new_nid)
    )
    def start_load_option_A(self, p_nid, rx, ry, g, pid, ptype, c, amt, max_l, counter, new_nid):
        self.declare(LoadEvaluated(nid=p_nid, pid=pid, color=c, mode="color"))
        self.modify(counter, value=new_nid + 1)

        self.declare(RobotState(nid=new_nid, x=rx, y=ry, g=g + 1))

        self.declare(CargoMeta(nid=new_nid, current_load=amt, mode="color", value=c))
        self.declare(CargoItem(nid=new_nid, pid=pid, type=ptype, color=c, amount=amt))

        self.declare(FrontierNode(nid=new_nid, f=0.0, parent=p_nid, action=f"Start_Load_Color_{c}", depth=1))
        self.declare(StateTransition(old_nid=p_nid, new_nid=new_nid))

    @Rule(
        SystemPhase(step="search"),
        ExpandNext(nid=MATCH.p_nid),

        RobotState(nid=MATCH.p_nid, x=MATCH.rx, y=MATCH.ry, g=MATCH.g),
        Warehouse(x=MATCH.rx, y=MATCH.ry),

        CargoMeta(nid=MATCH.p_nid, current_load=MATCH.cl, mode="color", value=MATCH.c),
        MaxLoad(value=MATCH.max_l),

        Need(nid=MATCH.p_nid, pid=MATCH.pid, color=MATCH.c, amount=MATCH.amt),
        Pavilion(pid=MATCH.pid, type=MATCH.ptype),
        TEST(lambda amt: amt > 0),

        TEST(lambda cl, amt, max_l: (cl + amt) <= max_l),

        NOT(CargoItem(nid=MATCH.p_nid, pid=MATCH.pid, color=MATCH.c)),

        NOT(LoadEvaluated(nid=MATCH.p_nid, pid=MATCH.pid, color=MATCH.c, mode="color_continue")),
        AS.counter << StateCounter(value=MATCH.new_nid)
    )
    def continue_load_option_A(self, p_nid, rx, ry, g, cl, c, pid, ptype, amt, counter, new_nid):

        self.declare(LoadEvaluated(nid=p_nid, pid=pid, color=c, mode="color_continue"))
        self.modify(counter, value=new_nid + 1)

        self.declare(RobotState(nid=new_nid, x=rx, y=ry, g=g))

        self.declare(CargoMeta(nid=new_nid, current_load=cl + amt, mode="color", value=c))
        self.declare(CargoItem(nid=new_nid, pid=pid, type=ptype, color=c, amount=amt))

        self.declare(FrontierNode(nid=new_nid, f=0.0, parent=p_nid, action=f"Add_Load_Color_{c}", depth=1))
        self.declare(StateTransition(old_nid=p_nid, new_nid=new_nid))

    @Rule(
        SystemPhase(step="search"),
        ExpandNext(nid=MATCH.p_nid),

        RobotState(nid=MATCH.p_nid, x=MATCH.rx, y=MATCH.ry, g=MATCH.g),
        Warehouse(x=MATCH.rx, y=MATCH.ry),

        # الروبوت فارغ
        CargoMeta(nid=MATCH.p_nid, current_load=0, mode="none"),

        # التقاط نوع الجناح لتثبيته
        Pavilion(pid=MATCH.pid, type=MATCH.ptype),
        Need(nid=MATCH.p_nid, pid=MATCH.pid, color=MATCH.c, amount=MATCH.amt),
        TEST(lambda amt: amt > 0),

        MaxLoad(value=MATCH.max_l),
        TEST(lambda amt, max_l: amt <= max_l),

        NOT(LoadEvaluated(nid=MATCH.p_nid, pid=MATCH.pid, color=MATCH.c, mode="type")),
        AS.counter << StateCounter(value=MATCH.new_nid)
    )
    def start_load_option_B(self, p_nid, rx, ry, g, pid, ptype, c, amt, max_l, counter, new_nid):

        self.declare(LoadEvaluated(nid=p_nid, pid=pid, color=c, mode="type"))
        self.modify(counter, value=new_nid + 1)

        self.declare(RobotState(nid=new_nid, x=rx, y=ry, g=g + 1))

        # تثبيت النمط "type" والقيمة ptype (مثلاً: "Rose")
        self.declare(CargoMeta(nid=new_nid, current_load=amt, mode="type", value=ptype))
        self.declare(CargoItem(nid=new_nid, pid=pid, type=ptype, color=c, amount=amt))

        self.declare(FrontierNode(nid=new_nid, f=0.0, parent=p_nid, action=f"Start_Load_Type_{ptype}", depth=1))
        self.declare(StateTransition(old_nid=p_nid, new_nid=new_nid))

    @Rule(
        SystemPhase(step="search"),
        ExpandNext(nid=MATCH.p_nid),

        RobotState(nid=MATCH.p_nid, x=MATCH.rx, y=MATCH.ry, g=MATCH.g),
        Warehouse(x=MATCH.rx, y=MATCH.ry),

        CargoMeta(nid=MATCH.p_nid, current_load=MATCH.cl, mode="type", value=MATCH.ptype),
        MaxLoad(value=MATCH.max_l),

        # إيجاد احتياج لجناح متوافق مع نفس النوع MATCH.ptype
        Pavilion(pid=MATCH.pid, type=MATCH.ptype),
        Need(nid=MATCH.p_nid, pid=MATCH.pid, color=MATCH.c, amount=MATCH.amt),
        TEST(lambda amt: amt > 0),

        TEST(lambda cl, amt, max_l: (cl + amt) <= max_l),
        NOT(CargoItem(nid=MATCH.p_nid, pid=MATCH.pid, color=MATCH.c)),

        NOT(LoadEvaluated(nid=MATCH.p_nid, pid=MATCH.pid, color=MATCH.c, mode="type_continue")),
        AS.counter << StateCounter(value=MATCH.new_nid)
    )
    def continue_load_option_B(self, p_nid, rx, ry, g, cl, ptype, pid, c, amt, counter, new_nid):
        self.declare(LoadEvaluated(nid=p_nid, pid=pid, color=c, mode="type_continue"))
        self.modify(counter, value=new_nid + 1)
        self.declare(RobotState(nid=new_nid, x=rx, y=ry, g=g))

        self.declare(CargoMeta(nid=new_nid, current_load=cl + amt, mode="type", value=ptype))
        self.declare(CargoItem(nid=new_nid, pid=pid, type=ptype, color=c, amount=amt))

        self.declare(FrontierNode(nid=new_nid, f=0.0, parent=p_nid, action=f"Add_Load_Type_{ptype}", depth=1))
        self.declare(StateTransition(old_nid=p_nid, new_nid=new_nid))