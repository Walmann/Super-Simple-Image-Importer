import json

class worker_queue_handler():
# class name(object, name):
    def __init__(self, work_queue = dict):
        self.work_queue = work_queue


    def load():
        with open("WorkQueue.json", "r") as file:
            x = {}
            try:
                x = json.load(file) 
                return x
            except json.decoder.JSONDecodeError:
                return x
    
    
    def save(self, work_queue):
        with open("WorkQueue.json", "w+") as file:
            json.dump(self.work_queue, fp=file)
            return True