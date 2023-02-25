import numpy as np

def classification_random():
    """A function that randomly generates one of the 3 states
    outputted by the classification algorithm. Can be used
    to guide the gameplay.
    """
    states = ["rest", "left", "right"]
    # probabilities p can be changed based on how much you want each state to occur
    cur_state = states[np.random.choice(np.arange(0, 3), p=[0.5, 0.25, 0.25])]
    return cur_state
