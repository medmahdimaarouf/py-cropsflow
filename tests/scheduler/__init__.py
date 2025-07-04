'''

from cropsflow.scheduler import AsyncScheduler
import time

scheduler = AsyncScheduler()

timer: int = 0


def call_back():
    global timer
    print('call_back: ', time.perf_counter() - timer)
    timer = time.perf_counter()


scheduler.start()

timer = time.perf_counter()
scheduler.schedule_every(seconds=2, call_back=call_back)
scheduler.schedule_every(seconds=3, call_back=call_back)

'''