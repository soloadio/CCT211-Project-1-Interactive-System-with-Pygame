from asyncio import InvalidStateError

# Define constants for the states
RUNNING = "run"
PAUSED = "pause"
ENDED = "end"

class States:
    def __init__(self):
        self.state = ENDED  # Initialize with the end state

    def change_state(self, new_state):
        if new_state == RUNNING or new_state == PAUSED or new_state == ENDED:   # Check if the new state is valid
            self.state = new_state
        else:
            raise InvalidStateError(f"Invalid state: '{new_state}'.")   # Raise an error if the new state is invalid

    def check_state(self, state):
        if state == RUNNING or state == PAUSED or state == ENDED:   # Check if the state to check is valid
            return self.state == state
        else:
            raise InvalidStateError(f"Invalid state: '{state}'.")   # Raise an error if the new state is invalid
        
    def get_state(self):
        return self.state   # Return the current state

