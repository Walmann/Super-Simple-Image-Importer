import json
import os



WorkQueueLoc = f"{os.environ['TEMP']}/WorkQueue.json"

class worker_queue_file_handler():
# class name(object, name):
    def __init__(self, work_queue = dict):
        self.work_queue = work_queue
    
    
    def new():
        x = {}
        with open(WorkQueueLoc, "w+") as file:
            json.dump(x, fp=file)
            return x

    def load():
        try:
            x = {}
            with open(WorkQueueLoc, "r") as file:
                try:
                    x = json.load(file) 
                    return x
                except json.decoder.JSONDecodeError:
                    return x
        except FileNotFoundError:
            with open(WorkQueueLoc, "w+") as file:
                json.dump(x, fp=file)
                return x
    
    def save(self, work_queue):
        with open(WorkQueueLoc, "w+") as file:
            json.dump(self.work_queue, fp=file)
            return True
    
    def delete():
        try:
            os.remove(WorkQueueLoc)
        except FileNotFoundError:
            pass