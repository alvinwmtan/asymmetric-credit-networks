import numpy as np
import random as random
from collections import deque

def initialise_graph(size):
    """
    Randomly initialises a complete graph of size `size`
    """
    state = np.zeros((size, size), dtype=int)

    for i in range(size):
        for j in range(i): 
            if random.random() > 0.5:
                state[i, j] = 1
            else:
                state[j, i] = 1
    
    return state

def make_transition_matrix(size):
    """
    Randomly generates a transition matrix of size `size`
    """
    t_matrix = np.random.random((size, size))
    np.fill_diagonal(t_matrix, 0)
    return t_matrix / np.sum(t_matrix)

def sample_transition(transition_matrix):
    """
    Randomly samples a transition from `transition_matrix`
    """
    size = transition_matrix.shape[0]
    idxs = np.array([(i, j) for i in range(size) for j in range(size)], dtype="i,i").astype(object)
    return np.random.choice(idxs, p=np.ravel(transition_matrix))

def bfs(state, source, target):
    """
    Given the current `state` of the network, uses breadth-first search 
    to attempt a transaction from the `source` to the `target`, returning 
    None if no feasible path exists.
    """
    visited = [target]
    queue = deque([[target]])

    while queue:
        cur_node = queue.popleft()
        # print(cur_node)
        last_visited = cur_node[-1]
        if last_visited == source:
            return cur_node

        for neighbour in np.nonzero(np.atleast_1d(np.asarray(state[last_visited] > 0)))[0]:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(cur_node + [neighbour])
                # print(queue)
    
    return None

def do_transaction(state, solution):
    """
    Given the current `state` of a network, executes the `solution`, which 
    is a sequence of nodes along which a unit transaction is routed.
    """
    if len(solution) > 1:
        for (s, t) in zip(solution[:-1], solution[1:]):
            state[s, t] -= 1
            state[t, s] += 1
    return state

def run_simulation(num_nodes, num_sims, num_iters, transition_matrix=None):
    """
    Runs a simulation on a network of size `num_nodes`, over `num_sims`
    simulations of `num_iters` iterations each. The network is randomly
    initialised, and the transition matrix is randomly generated unless
    `transition_matrix` is supplied, in which case that matrix is used.
    """
    all_sims = []
    all_trans = []

    make_tm = transition_matrix is None

    for i in range(num_sims):
        if (i+1)%50 == 0:
            print(f"Sim {(i+1):03d}")

        state = initialise_graph(num_nodes)
        if make_tm:
            transition_matrix = make_transition_matrix(num_nodes)
        all_states = [state.copy()]
        all_trans.append(transition_matrix.copy())

        for i in range(num_iters):
            (source, target) = sample_transition(transition_matrix)
            soln = bfs(state, source, target)
            if soln is None:
                all_states.append(state.copy())
            else:
                new_state = do_transaction(state, soln)
                all_states.append(new_state.copy())
                state = new_state
        
        all_sims.append(all_states)
    
    return all_sims, all_trans