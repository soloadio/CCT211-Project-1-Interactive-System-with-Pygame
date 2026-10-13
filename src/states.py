class states:
    def __init__(self):
        self.states = ["run", "pause", "end"]
        self.state = self.states[2]  # Initialize with the end state

    def change_state(self, new_state):
        if new_state in self.states:
            self.state = new_state

    def get_state(self):
        return self.state
