# RICCARDO SAMARITAN SM3201396

class InstructionNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class LabelNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class EmptyInputQueueException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class HaltException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message