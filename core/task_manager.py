import threading
import queue


# =====================================================
# TASK QUEUE
# =====================================================

task_queue = queue.Queue()


# =====================================================
# TASK WORKER
# =====================================================

def task_worker():

    while True:

        task_function, args = task_queue.get()

        try:

            task_function(*args)

        except Exception as e:

            print(f"Task Error: {e}")

        task_queue.task_done()


# =====================================================
# START BACKGROUND WORKER
# =====================================================

worker_thread = threading.Thread(
    target=task_worker,
    daemon=True
)

worker_thread.start()


# =====================================================
# ADD TASK
# =====================================================

def add_task(task_function, *args):

    task_queue.put(
        (task_function, args)
    )