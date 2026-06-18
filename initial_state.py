from homework2.facts import *

class InitialStateMixin1:
    @DefFacts()
    def init_environment_and_state(self):
        yield Grid(width=6, height=6)
        yield Warehouse(x=3, y=2)

        yield Progress(nid=0, deliv=0)

        yield MaxDepth(value=120)
        yield MaxLoad(value=4)

        yield Pavilion(pid="p1", x=2, y=4, type="Rose")
        yield Pavilion(pid="p2", x=4, y=3, type="Tulip")
        yield Pavilion(pid="p3", x=4, y=5, type="Orchid")
        yield Pavilion(pid="p4", x=5, y=2, type="GoliatRose")

        yield RobotState(nid=0, x=1, y=3, g=0)
        yield CargoMeta(nid=0, current_load=0, mode="none", value="none")

        yield TotalNeeds(nid=0, value=15)
        yield StaticDavg(value=3)

        yield Need(nid=0, pid="p1", color="Red", amount=2)
        yield Need(nid=0, pid="p1", color="Pink", amount=1)
        yield Need(nid=0, pid="p1", color="White", amount=1)


        yield Need(nid=0, pid="p2", color="Red", amount=3)
        yield Need(nid=0, pid="p2", color="Yellow", amount=1)


        yield Need(nid=0, pid="p3", color="Purple", amount=2)
        yield Need(nid=0, pid="p3", color="Pink", amount=1)


        yield Need(nid=0, pid="p4", color="Gold", amount=2)
        yield Need(nid=0, pid="p4", color="LightPink", amount=2)



        initial_h = 25.0
        initial_f = 0.0 + initial_h

        yield FrontierNode(
            nid=0,
            f=initial_f,
            parent=-1,
            action="start",
            depth=0
        )

        yield BestFrontier(nid=0, f=initial_f)
        yield StateCounter(value=1)
        yield SystemPhase(step="init_maxload")

        yield PavilionTotal(pid="p1", total=0)
        yield PavilionTotal(pid="p2", total=0)
        yield PavilionTotal(pid="p3", total=0)
        yield PavilionTotal(pid="p4", total=0)

        yield TotalNeeds(nid=1,value=15)