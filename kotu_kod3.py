from datetime import datetime, timedelta

class task:
    def __init__(self, t, p, d, e):
        self.t = t
        self.p = p
        self.d = d
        self.e = e 

def sorting_things(t):
    now = datetime.now()
    def s(task):
        tl = (task.d - now).total_seconds() / 3600
        if tl == 0:
            return 1000000  
        return (task.p / tl) / task.e

    t.sort(key=s, reverse=True)
    return t

tasks = [
    task("report", 10, datetime.now() + timedelta(hours=5), 2),
    task("slides", 7, datetime.now() + timedelta(hours=48), 4),
    task("assignment", 8, datetime.now() + timedelta(hours=12), 6),
    task("docs", 6, datetime.now() + timedelta(hours=24), 3)
]

x = sorting_things(tasks)
for i in x:
    print(i.t)
