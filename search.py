from homework2.facts import *

from experta import *


class SearchRulesMixin(KnowledgeEngine):

    # @Rule(
    #     AS.phase << SystemPhase(step="search"),
    #     ExpandNext(nid=MATCH.nid),
    #
    #     FrontierNode(nid=MATCH.nid, depth=MATCH.depth),
    #     RobotState(nid=MATCH.nid, g=MATCH.g),
    #     Need(nid=MATCH.nid,pid=MATCH.pid,color=MATCH.c,amount=MATCH.amount),
    #     CargoMeta(current_load=MATCH.current_load),
    #     TEST(lambda amount,current_load: amount == 0 & current_load ==0),
    #
    #     salience=2000
    # )
    # def verify_path_bounds(self, phase, nid, g, depth):
    #
    #     self.modify(phase, step="print_solution")
    #     self.declare(GoalFound(nid=nid))
    #
    #     print("\n" + "=" * 50)
    #     print("[Goal State] - Optimal solution reached successfully!")
    #     print(f"   - Goal Node ID: {nid}")
    #     print(f"   - Total Actual Cost (g): {g}")
    #     print(f"   - Solution Depth: {depth}")
    #     print("=" * 50 + "\n")



    @Rule(
        AS.phase << SystemPhase(step="search"),
        ExpandNext(nid=MATCH.nid),

        FrontierNode(nid=MATCH.nid, depth=MATCH.depth),
        RobotState(nid=MATCH.nid, g=MATCH.g),

        # NOT(Need(nid=MATCH.nid, amount=P(lambda amt: amt > 0))),

        Need(nid=MATCH.nid, pid=MATCH.pid, color=MATCH.c, amount=MATCH.amount),
        CargoMeta(nid=MATCH.nid,current_load=MATCH.current_load),
        TotalNeeds(nid=MATCH.nid, value=MATCH.value),

        TEST(lambda amount, current_load: amount == 0 & current_load == 0),
        # NOT(CargoItem(nid=MATCH.nid))
    )
    def goal_state_found(self, phase, nid, g, depth,value):
        print("VVVV"+str(value))
        self.modify(phase, step="print_solution")
        self.declare(GoalFound(nid=nid))

        print("\n" + "=" * 50)
        print("[Goal State] - Optimal solution reached successfully!")
        print(f"   - Goal Node ID: {nid}")
        print(f"   - Total Actual Cost (g): {g}")
        print(f"   - Solution Depth: {depth}")
        print("=" * 50 + "\n")



    @Rule(
        SystemPhase(step="search"),

        NOT(OpenNode()),
        NOT(ExpandNext()),

        NOT(GoalFound()),

        salience=10
    )
    def search_failed_agenda_empty(self):
        print("\n" + "" * 25)
        print(" فشل البحث: أجندة العقد المفتوحة (Open List) فارغة!")
        print("الروبوت بحث في كل المسارات الممكنة ولم يجد طريقاً لإنجاز المهمة.")
        print("" * 25 + "\n")

        self.halt()