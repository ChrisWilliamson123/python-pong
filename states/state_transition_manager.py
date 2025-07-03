from states.state_type import StateType

def change_state(states, from_state, to_state):
    """Handles logic that needs to be performed as transitions occur between pairs of states"""
    if to_state is StateType.GAME:
        if from_state in [StateType.GAME_OVER, StateType.MENU]:
            states[StateType.GAME].reset()
