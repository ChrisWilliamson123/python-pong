from states.state_type import StateType

def change_state(states, from_state, to_state):
    """Handles logic that needs to be performed as transitions occur between pairs of states"""
    if from_state is StateType.GAME_OVER and to_state is StateType.GAME:
        # Reset the game
        states[StateType.GAME].reset()
