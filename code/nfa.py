from state import *
import regex
import copy
from collections import deque


# NFA is a class with four fields:
# -states = a list of states in the NFA
#  Note that the start state is always state 0
# -accepting = A dictionary, the key is the state id 
#  and value is a boolean indicating which states are acceping
# -alphabet = a list of symbols in the alphabet of the regular language.
#  Note that & can not be included because we use it as epsilon
# -startS = it is the start state id which we assume it is always 0
class NFA:
    def __init__(self):
        self.states = []
        self.is_accepting = dict()
        self.alphabet = []
        self.startS = 0
        pass

    def __str__(self):
        pass

    # You should write this function.
    # It takes two states and a symbol. It adds a transition from 
    # the first state of the NFA to the other input state of the NFA.
    def addTransition(self, s1, s2, sym='&'):
        if sym != '&' and sym not in self.alphabet:
            self.alphabet.append(sym)
        if sym in s1.transition:
            if s2 not in s1.transition[sym]:
                s1.transition[sym].append(s2)
        else:
            s1.transition[sym] = [s2]
        pass

    # You should write this function.
    # It takes an nfa, adds all the states from that nfa and return a 
    # mapping of (state number in old NFA to state number in this NFA) as a dictionary.
    def addStatesFrom(self, nfa):
        state_mapping = {}
        len_self = len(self.states)
        len_nfa = len(nfa.states)
        for i in range(len_self, len_self + len_nfa):
            # update states.id & add states
            self.states.append(nfa.states[i - len_self])
            self.states[i].id = i
            state_mapping[i - len_self] = i
            # update accept

            self.is_accepting[i] = nfa.is_accepting[i - len_self]
            # update alphabet
        for symbol in nfa.alphabet:
            if symbol not in self.alphabet:
                self.alphabet.append(symbol)

        return state_mapping
        pass

    # You should write this function.
    # It takes a state and returns the epsilon closure of that state 
    # which is a set of states which are reachable from this state 
    # on epsilon transitions.
    def epsilonClose(self, ns):
        states = []
        for n in ns:
            for sym, nn in self.states[n.id].transition.items():
                if sym == '&':
                    for s in nn:
                        states.append(s)
        return set(states)

    # rewrite epsilon close function
    def epsilon_Close(self, ns):
        s = ns[0]
        visited = set()
        queue = [s]
        res = set()
        while queue:
            curr_s = queue.pop(0)
            if curr_s in visited:
                continue
            else:
                for sym, states in curr_s.transition.items():
                    if sym == '&':
                        for n_s in states:
                            queue.append(n_s)
                            res.add(n_s)
            visited.add(curr_s)

        return res

    # It takes a string and returns True if the string is in the language of this NFA
    def problematic(self, string):

        queue = [(self.states[0], 0)]
        currS = self.states[0]
        pos = 0
        visited = []
        while queue:
            currS, pos = queue.pop()  # LIFO, we need FIFO, queue.pop(0)
            if pos == len(string):
                if currS.id in self.is_accepting and self.is_accepting[currS.id]:
                    return self.is_accepting[currS.id]
                for n in self.epsilonClose([currS]):
                    queue.append((n, pos))
                continue
            for s in self.states:
                if s.id == currS.id:
                    if string[pos] in s.transition:
                        stats = s.transition[string[pos]]
                        for stat in stats:
                            queue.extend([(stat, pos + 1)])
                            queue.extend([(s, pos + 1) for s in self.epsilonClose([stat])])
                    else:
                        for n in self.epsilonClose([currS]):
                            queue.append((n, pos))
                    break
        if pos == len(string):
            return currS.id in self.is_accepting and self.is_accepting[currS.id]
        else:
            return False

    def isStringInLanguage(self, string):
        queue = deque([(self.states[0], 0)])
        visited = set()

        while queue:
            curr, pos = queue.popleft()
            if (curr, pos) in visited:
                continue
            visited.add((curr, pos))

            if pos == len(string):
                if curr.id in self.is_accepting and self.is_accepting[curr.id]:
                    return True
                for n in self.epsilonClose([curr]):
                    queue.append((n, pos))
                continue

            if string[pos] in curr.transition:
                for stat in curr.transition[string[pos]]:
                    queue.append((stat, pos + 1))
                    for s in self.epsilonClose([stat]):
                        queue.append((s, pos + 1))
            else:
                for n in self.epsilonClose([curr]):
                    queue.append((n, pos))

        return False

    pass
