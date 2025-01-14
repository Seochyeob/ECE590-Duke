import nfa
from nfa import *
from state import *


class Regex:
    def __repr__(self):
        ans = str(type(self)) + "("
        sep = ""
        for i in self.children:
            ans = ans + sep + repr(i)
            sep = ", "
            pass
        ans = ans + ")"
        return ans

    def transformToNFA(self):
        pass

    pass


class ConcatRegex(Regex):
    def __init__(self, r1, r2):
        self.children = [r1, r2]
        pass

    def __str__(self):
        return "{}{}".format(self.children[0], self.children[1])

    def transformToNFA(self):
        nfa1 = self.children[0].transformToNFA()
        nfa2 = self.children[1].transformToNFA()
        mapping = nfa1.addStatesFrom(nfa2)
        state2 = nfa1.states[mapping[0]]
        # add nfa1's accepting state to nfa2's starting state
        for i in range(mapping[0]):
            if nfa1.is_accepting[i]:
                nfa1.is_accepting[i] = False
                nfa1.addTransition(nfa1.states[i], state2)
        # update alphabet
        for i in nfa2.alphabet:
            if i not in nfa1.alphabet:
                nfa1.alphabet.append(i)
        return nfa1
        pass

    pass


class StarRegex(Regex):
    def __init__(self, r1):
        self.children = [r1]
        pass

    def __str__(self):
        return "({})*".format(self.children[0])

    def transformToNFA(self):
        nfa = self.children[0].transformToNFA()
        for i in range(len(nfa.states)):
            # add transitions
            if nfa.is_accepting[i] and i != 0:
                nfa.addTransition(nfa.states[i], nfa.states[nfa.startS])
        # add startS as accepting state since 0 length is acceptable
        nfa.is_accepting[nfa.startS] = True
        return nfa
        pass

    pass


class OrRegex(Regex):
    def __init__(self, r1, r2):
        self.children = [r1, r2]
        pass

    def __str__(self):
        return "(({})|({}))".format(self.children[0], self.children[1])

    def transformToNFA(self):
        nfa1 = self.children[0].transformToNFA()
        nfa2 = self.children[1].transformToNFA()
        or_nfa = NFA()
        # new start state and new accept state
        state_mapping1 = or_nfa.addStatesFrom(nfa1)
        state_mapping2 = or_nfa.addStatesFrom(nfa2)
        or_nfa.addTransition(or_nfa.states[0], or_nfa.states[state_mapping2[0]])

        or_nfa.alphabet = list(set(nfa1.alphabet).union(nfa2.alphabet))
        return or_nfa
        pass

    pass


class SymRegex(Regex):
    def __init__(self, sym):
        self.sym = sym
        pass

    def __str__(self):
        return self.sym

    def __repr__(self):
        return self.sym

    def transformToNFA(self):
        nfa = NFA()
        start_state = State(0)
        accept_state = State(1)
        # add 2 states
        nfa.states.append(start_state)
        nfa.states.append(accept_state)
        # add accepting state
        nfa.is_accepting[0] = False
        nfa.is_accepting[1] = True
        # add transition
        nfa.states[0].transition[self.sym] = [nfa.states[1]]
        # add alphabet
        if self.sym not in nfa.alphabet:
            nfa.alphabet.append(self.sym)
        return nfa
        pass

    pass


class EpsilonRegex(Regex):
    def __init__(self):
        pass

    def __str__(self):
        return '&'

    def __repr__(self):
        return '&'

    def transformToNFA(self):
        nfa = NFA()
        start_state = State(0)
        # add state
        nfa.states.append(start_state)
        # add accepting state
        nfa.is_accepting[start_state.id] = True
        return nfa
        pass

    pass


class ReInput:
    def __init__(self, s):
        self.str = s
        self.pos = 0
        pass

    def peek(self):
        if (self.pos < len(self.str)):
            return self.str[self.pos]
        return None

    def get(self):
        ans = self.peek()
        self.pos += 1
        return ans

    def eat(self, c):
        ans = self.get()
        if (ans != c):
            raise ValueError("Expected " + str(c) + " but found " + str(ans) +
                             " at position " + str(self.pos - 1) + " of  " + self.str)
        return c

    def unget(self):
        if (self.pos > 0):
            self.pos -= 1
            pass
        pass

    pass


# R -> C rtail
# rtail -> OR C rtail | eps
# C -> S ctail
# ctail -> S ctail | eps
# S -> atom stars
# atom -> (R) | sym | &
# stars -> * stars | eps


# It gets a regular expression string and returns a Regex object.
def parse_re(s):
    inp = ReInput(s)

    def parseR():
        return rtail(parseC())

    def parseC():
        return ctail(parseS())

    def parseS():
        return stars(parseA())

    def parseA():
        c = inp.get()
        if c == '(':
            ans = parseR()
            inp.eat(')')
            return ans
        if c == '&':
            return EpsilonRegex()
        if c in ')|*':
            inp.unget()
            inp.fail("Expected open paren, symbol, or epsilon")
            pass
        return SymRegex(c)

    def rtail(lhs):
        if (inp.peek() == '|'):
            inp.get()
            x = parseC()
            return rtail(OrRegex(lhs, x))
        return lhs

    def ctail(lhs):
        if (inp.peek() is not None and inp.peek() not in '|*)'):
            temp = parseS()
            return ctail(ConcatRegex(lhs, temp))
        return lhs

    def stars(lhs):
        while (inp.peek() == '*'):
            inp.eat('*')
            lhs = StarRegex(lhs)
            pass
        return lhs

    return parseR()
