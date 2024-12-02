class UniqueIDGenerator:
    def __init__(self, start=1):
        self.counter = start

    def generate(self):
        unique_id = self.counter
        self.counter += 1
        return unique_id

