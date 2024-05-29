import copy
from state import *
from collections import deque


# DFA is a class with four fields:
# -states = a list of states in the DFA
#  Note that the start state is always state 0
# -accepting = A dictionary, the key is the state id 
#  and value is a boolean indicating which states are acceping
# -alphabet = a list of symbols in the alphabet of the regular language.
#  Note that & can not be included because we use it as epsilon
# -startS = it is the start state id which we assume it is always 0
class DFA:
    def __init__(self):
        self.states = []
        self.is_accepting = dict()
        self.alphabet = []
        self.startS = 0
        pass

    def __str__(self):
        pass

    # You should write this function.
    # It takes two states and a symbol/char. It adds a transition from
    # the first state of the DFA to the other input state of the DFA.
    def addTransition(self, s1, s2, sym):
        s1.transition[sym] = [s2]
        pass
        # You should write this function.

    # It returns a DFA that is the complement of this DFA
    def complement(self):
        for i in self.states:
            self.is_accepting[i.id] = not self.is_accepting[i.id]
        pass

    # You should write this function.
    # It takes a string and returns True if the string is in the language of this DFA
    def isStringInLanguage(self, string):
        state_id = 0
        for i in string:
            state = self.states[state_id]
            if i in state.transition:
                target_state = state.transition[i][0]
                state_id = target_state.id
            else:
                return False
        return self.is_accepting[state_id]

        pass

    # You should write this function.
    # It runs BFS on this DFA and returns the shortest string accepted by it
    def shortestString(self):
        queue = deque([(self.startS, "")])
        visited = set()
        while queue:
            state, path = queue.popleft()

            if self.is_accepting[state]:
                return path

            # avoid go to the visited state
            if state in visited:
                continue
            visited.add(state)
            for symbol in self.alphabet:
                if symbol in self.states[state].transition:
                    next_state = self.states[state].transition[symbol][0].id
                    queue.append((next_state, path + symbol))
        return ""

        pass

    pass
