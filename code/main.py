import copy
from regex import *
from state import *
from nfa import *
from dfa import *


def checkAccept(accept, states_id):
    for i in states_id:
        if accept[i]:
            return True
    return False


# You should write this function.
# It takes an NFA and returns a DFA.
def nfaToDFA(nfa):
    # new dfa
    dfa = DFA()
    # copy alphabet
    dfa.alphabet = nfa.alphabet
    # deal with start state
    dfa.states.append(State(0))
    # calculate all reachable states for dfa.startS
    # initial_closure = nfa.epsilonClose([nfa.states[0]]) # not include itself
    reachable = dict()
    for i in range(len(nfa.states)):
        epsilon = nfa.epsilon_Close([nfa.states[i]])  # set of epsilon reachable states except itself
        ep_states = [i]  # add current state
        for j in epsilon:
            ep_states.append(j.id)
        reachable[i] = set(ep_states)
    # print(reachable)
    # whether contain accept
    dfa.is_accepting[0] = checkAccept(nfa.is_accepting, reachable[0])

    queue = deque([(0, reachable[0])])  # queue stores: DFA states，NFA states)
    visited = {tuple(reachable[0]): 0}

    while queue:
        num, curr_state_id_set = queue.popleft()
        for sym in nfa.alphabet:
            next_state_id_set = set()
            for curr_state_id in curr_state_id_set:
                if sym in nfa.states[curr_state_id].transition:
                    next_states = nfa.states[curr_state_id].transition[sym]
                    for sub in next_states:
                        next_state_id_set.add(sub.id)
                        for i in reachable[sub.id]:  # add epsilon close
                            next_state_id_set.add(i)

            if not next_state_id_set:
                continue
            next_state_id_tuple = tuple(next_state_id_set)
            if next_state_id_tuple in visited:
                idx = visited[next_state_id_tuple]
            else:
                idx = len(dfa.states)
                dfa.states.append(State(idx))
                dfa.is_accepting[idx] = checkAccept(nfa.is_accepting, next_state_id_set)
                queue.append((idx, next_state_id_set))
                visited[next_state_id_tuple] = idx

            dfa.addTransition(dfa.states[num], dfa.states[idx], sym)

    return dfa
    pass


# You should write this function.
# It takes an DFA and returns a NFA.
def dfaToNFA(dfa):
    nfa = NFA()
    nfa.states = copy.deepcopy(dfa.states)
    nfa.is_accepting = copy.deepcopy(dfa.is_accepting)
    nfa.alphabet = copy.deepcopy(dfa.alphabet)
    return nfa
    pass


# You should write this function.
# It takes two regular expressions and returns a 
# boolean indicating if they are equivalent
def equivalent(re1, re2):
    nfa1 = re1.transformToNFA()
    nfa2 = re2.transformToNFA()
    dfa1 = nfaToDFA(nfa1)
    dfa1.complement()
    dfa2 = nfaToDFA(nfa2)
    dfa2.complement()
    comp_nfa1 = dfaToNFA(dfa1)
    comp_nfa2 = dfaToNFA(dfa2)

    inside1 = union(comp_nfa1, nfa2)
    outside1 = nfaToDFA(inside1)
    outside1.complement()
    for i in outside1.is_accepting:
        if outside1.is_accepting[i]:
            return False

    inside2 = union(nfa1, comp_nfa2)
    outside2 = nfaToDFA(inside2)
    outside2.complement()
    for i in outside2.is_accepting:
        if outside2.is_accepting[i]:
            return False

    return True
    pass


def union(nfa1, nfa2):
    nfa = NFA()
    # new start state and new accept state
    state_mapping1 = nfa.addStatesFrom(nfa1)
    state_mapping2 = nfa.addStatesFrom(nfa2)
    nfa.addTransition(nfa.states[0], nfa.states[state_mapping2[0]])
    nfa.alphabet = list(set(nfa1.alphabet).union(nfa2.alphabet))
    return nfa


if __name__ == "__main__":
    def testNFA(strRe, s, expected):
        re = parse_re(strRe)
        # test your nfa conversion
        nfa = re.transformToNFA()
        res = nfa.isStringInLanguage(s)
        if res == expected:
            print(strRe, " gave ", res, " as expected on ", s)
        else:
            print("**** ", strRe, " Gave ", res, " on ", s, " but expected ", expected)
            pass
        pass


    def testDFA(strRe, s, expected):

        re = parse_re(strRe)
        nfa = re.transformToNFA()
        # test your dfa conversion
        dfa = nfaToDFA(nfa)

        res = dfa.isStringInLanguage(s)

        if res == expected:
            print(strRe, " gave ", res, " as expected on ", s)
        else:
            print("**** ", strRe, " Gave ", res, " on ", s, " but expected ", expected)
            pass
        pass

    def testEquivalence(strRe1, strRe2, expected):
        re1 = parse_re(strRe1)
        re2 = parse_re(strRe2)

        res = equivalent(re1, re2)
        if res == expected:
            print("Equivalence(", strRe1, ", ", strRe2, ") = ", res, " as expected.")
        else:
            print("Equivalence(", strRe1, ", ", strRe2, ") = ", res, " but expected ", expected)
            pass
        pass


    def pp(r):
        print()
        print("Starting on " + str(r))
        re = parse_re(r)
        print(repr(re))
        print(str(re))
        pass


    # test your NFA:
    testNFA('&', '', True)
    testNFA('a', '', False)
    testNFA('a', 'a', True)
    testNFA('a', 'ab', False)
    testNFA('a*', '', True)
    testNFA('a*', 'a', True)
    testNFA('a*', 'aaa', True)
    testNFA('a|b', '', False)
    testNFA('a|b', 'a', True)
    testNFA('a|b', 'b', True)
    testNFA('a|b', 'ab', False)
    testNFA('ab|cd', '', False)
    testNFA('ab|cd', 'ab', True)
    testNFA('ab|cd', 'cd', True)
    testNFA('ab|cd*', '', False)
    testNFA('ab|cd*', 'c', True)
    testNFA('ab|cd*', 'cd', True)
    testNFA('ab|cd*', 'cddddddd', True)
    testNFA('ab|cd*', 'ab', True)
    testNFA('((ab)|(cd))*', '', True)
    testNFA('((ab)|(cd))*', 'ab', True)
    testNFA('((ab)|(cd))*', 'cd', True)
    testNFA('((ab)|(cd))*', 'abab', True)
    testNFA('((ab)|(cd))*', 'abcd', True)
    testNFA('((ab)|(cd))*', 'cdcdabcd', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', '', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'ab', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'abcd', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'cd', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'dfgab', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'defg', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'deeefg', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hkln', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'q', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijkln', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijklmmmmmmmmmmn', True)

    testDFA('&', '', True)
    testDFA('a', '', False)
    testDFA('a', 'a', True)
    testDFA('a', 'ab', False)
    testDFA('a*', '', True)
    testDFA('a*', 'a', True)
    testDFA('a*', 'aaa', True)
    testDFA('a|b', '', False)
    testDFA('a|b', 'a', True)
    testDFA('a|b', 'b', True)
    testDFA('a|b', 'ab', False)
    testDFA('ab|cd', '', False)
    testDFA('ab|cd', 'ab', True)
    testDFA('ab|cd', 'cd', True)
    testDFA('ab|cd*', '', False)
    testDFA('ab|cd*', 'c', True)
    testDFA('ab|cd*', 'cd', True)
    testDFA('ab|cd*', 'cddddddd', True)
    testDFA('ab|cd*', 'ab', True)
    testDFA('((ab)|(cd))*', '', True)
    testDFA('((ab)|(cd))*', 'ab', True)
    testDFA('((ab)|(cd))*', 'cd', True)
    testDFA('((ab)|(cd))*', 'abab', True)
    testDFA('((ab)|(cd))*', 'abcd', True)
    testDFA('((ab)|(cd))*', 'cdcdabcd', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', '', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'ab', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'abcd', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'cd', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'dfgab', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'defg', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'deeefg', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hkln', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'q', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijkln', True)
    testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijklmmmmmmmmmmn', True)
    testEquivalence('((a|b)*|b)*', '(b)((a|b)*|b)*', False)
    testEquivalence('a*', 'aa*', False)
    testEquivalence('a|b', 'a|((a|b)|b)', True)
    testEquivalence('(a|b)*', '(a|((a|b)|b))*', True)
    testEquivalence('&', '&&', True)
    testEquivalence('&', '&&a', False)
    testEquivalence('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijklmmmmmmmmmmn', False)
    testEquivalence('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', '((ab|cd)*|(de*fg|h(ij)*klm*m*n|q))*', True)

    pass
