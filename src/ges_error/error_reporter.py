class ErrorReporter:

    def __init__(self):
        self.errori = []

    def add(self, msg):
        self.errori.append(msg)

    def has_errors(self):
        return len(self.errori) > 0

    def get_all(self):
        return "\n".join(self.errori)
