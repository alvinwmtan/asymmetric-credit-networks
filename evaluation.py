import numpy as np
import pandas as pd

def get_gen_score_vec(state):
    """
    Get the generalised score vector of a given network `state`.
    """
    return np.sum(state, axis=1)

def get_cumprops(states, vec_list):
    """
    Gets the cumulative proportions of states across a time series
    of `states`.
    """
    gen_score_vecs = np.array([np.array_str(get_gen_score_vec(s)) for s in states])
    vals = [(gen_score_vecs == v).astype(int) for v in vec_list]
    cum_vals = [np.divide(np.cumsum(v), (range(1,len(states)+1))) for v in vals]
    return cum_vals

def make_long(cumprop, i, vec_list):
    """
    Helper function for tidying a list of cumulative proportions from
    `cumprop` and assigning it the simulation number `i`.
    """
    df = pd.DataFrame(dict(zip(vec_list, cumprop)))
    df["iter"] = df.index
    long = pd.melt(df, id_vars="iter")
    long["sim"] = i
    return long

def make_p_matrix(transition_matrix):
    """
    Specifically given a 3x3 `transition_matrix`, calculates explicitly
    the P matrix induced by this transition matrix over a cycle of 
    size 3.
    """
    tm = transition_matrix
    p_matrix = np.array([
        [0, tm[1,0], tm[0,2], tm[2,1], tm[0,1], tm[1,2], tm[2,0]],
        [tm[0,1], tm[1,0]+tm[1,2]+tm[2,0], 0, 0, 0, tm[2,1], tm[0,2]],
        [tm[2,0], 0, tm[0,1]+tm[0,2]+tm[1,2], 0, tm[2,1], 0, tm[1,0]],
        [tm[1,2], 0, 0, tm[0,1]+tm[2,0]+tm[2,1], tm[0,2], tm[1,0], 0],
        [tm[1,0], 0, tm[1,2], tm[2,0], tm[0,1]+tm[0,2]+tm[2,1], 0, 0],
        [tm[0,2], tm[1,2], 0, tm[0,1], 0, tm[1,0]+tm[2,0]+tm[2,1], 0],
        [tm[2,1], tm[2,0], tm[0,1], 0, 0, 0, tm[0,2]+tm[1,2]+tm[1,0]]
    ])
    return p_matrix

def get_distrib(p_matrix):
    """
    Gets the estimated steady-state distribution given a `p_matrix`
    by finding its left eigenvector with eigenvalue 1.
    """
    eigval, eigvec = np.linalg.eig(p_matrix.T)
    unit_eig = abs(eigval - 1.) < 1e-14 # account for floating point errors
    if (np.sum(unit_eig) != 1):
        return None
    vec = eigvec[:, unit_eig].real
    return vec / np.sum(vec)

def calc_symmetry(transition_matrix):
    """
    Calculates the symmetry of a `transition_matrix` by comparing the
    Frobenius norms of its symmetric and skew-symmetric components.
    """
    t_sym = (transition_matrix + transition_matrix.T) / 2
    t_anti = (transition_matrix - transition_matrix.T) / 2
    norm_sym = np.linalg.norm(t_sym, ord="fro")
    norm_anti = np.linalg.norm(t_anti, ord="fro")
    return (norm_sym - norm_anti) / (norm_sym + norm_anti)

def calc_rmse(actual, predicted):
    """
    Calculates the root mean squared error given actual and predicted
    values.
    """
    return np.sqrt(np.mean((actual - predicted) ** 2))

def calc_entropy(distrib):
    """
    Calculates the Shannon entropy of a `distrib`ution.
    """
    return -1 * np.sum(distrib * np.log2(distrib))