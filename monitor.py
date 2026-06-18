from experta import *
from homework2.facts import *
class DebugMonitor(KnowledgeEngine):
    @Rule(CargoItem(nid=MATCH.nid, type=MATCH.t, color=MATCH.c, amount=MATCH.amt))
    def watch_cargo(self, nid, t, c, amt):
        print(f"[DEBUG] العقدة {nid}: الروبوت يحمل الآن {amt} من {t} بلون {c}")

    @Rule(Need(nid=MATCH.nid, pid=MATCH.pid, color=MATCH.c, amount=MATCH.amt))
    def watch_needs(self, nid, pid, c, amt):
        if amt == 0:
            print(f" [DEBUG] العقدة {nid}: تم تلبية احتياج الجناح {pid} للون {c} بالكامل.")