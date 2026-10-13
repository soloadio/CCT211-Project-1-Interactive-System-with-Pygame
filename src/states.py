from asyncio import InvalidStateError

# Define constants for the states
RUNNING = "run"
PAUSED = "pause"
ENDED = "end"

class States:
    def __init__(self):
        self.state = ENDED  # Initialize with the end state

    def change_state(self, new_state):
        if new_state == RUNNING or new_state == PAUSED or new_state == ENDED:
            self.state = new_state

    def check_state(self, state):
        if state == RUNNING or state == PAUSED or state == ENDED:
            return self.state == state
        else:
            raise InvalidStateError(f"Invalid state: '{state}'.")
        
    def get_state(self):
        return self.state

