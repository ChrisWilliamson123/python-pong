class StateManager:
    def __init__(self, states, current_state_type, state_transition_logic_fn):
        self.states = states
        self.current_state_type = current_state_type
        self.current_state = states[self.current_state_type]
        self.previous_state_type = None
        self.state_transition_logic_fn = state_transition_logic_fn # takes in states as param and performs logic based on state transition

    def change_state(self, new_state_type):
        self.state_transition_logic_fn(self.states, self.current_state_type, new_state_type)

        self.previous_state_type = self.current_state_type
        self.current_state = self.states[new_state_type]
        self.current_state_type = new_state_type

    @property
    def previous_state(self):
        return self.states[self.previous_state_type]
