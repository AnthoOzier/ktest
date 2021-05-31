
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from rv_gen import gen_couple
import torch
import numpy as np

def distances(x, y=None):
    """
    If Y=None, then this computes the distance between X and itself
    """
    if (isinstance(x, np.ndarray)):
        x = torch.from_numpy(x)
    if (isinstance(y, np.ndarray)):
        y = torch.from_numpy(y)
    
    assert(x.ndim == 2)

    if y is None:
        sq_dists = torch.cdist(x, x, compute_mode='use_mm_for_euclid_dist_if_necessary').pow(
            2)  # [sq_dists]_ij=||X_j - X_i \\^2
    else:
        assert(y.ndim == 2)
        assert(x.shape[1] == y.shape[1])
        sq_dists = torch.cdist(x, y, compute_mode='use_mm_for_euclid_dist_if_necessary').pow(
            2)  # [sq_dists]_ij=||x_j - y_i \\^2
    return sq_dists

def mediane(x, y=None):
    """
    Computes the median 
    """
    if (isinstance(x, np.ndarray)):
        x = torch.from_numpy(x)
    if (isinstance(y, np.ndarray)):
        y = torch.from_numpy(y)
    
    dxx = distances(x)
    if y == None:
        return dxx.median()
    dyy = distances(y)
    dxy = distances(x,y)
    dyx = dxy.t()
    dtot = torch.cat((torch.cat((dxx,dxy),dim=1),
                      torch.cat((dyx,dyy),dim=1)),dim=0)
    return dtot.median()

def gauss_kernel(x, y, sigma=1):
    """
    Computes the standard Gaussian kernel k(x,y)=exp(- ||x-y||**2 / (2 * sigma**2))

    X - 2d array, samples on left hand side
    Y - 2d array, samples on right hand side, can be None in which case they are replaced by X

    returns: kernel matrix
    """
    
    d = distances(x, y)   # [sq_dists]_ij=||X_j - Y_i \\^2
    K = torch.exp(-d / (2 * sigma**2))  # Gram matrix
    return K

def gauss_kernel_mediane(x,y,return_mediane=False):
    m = mediane(x, y)
    if return_mediane:
        return ( lambda x, y: gauss_kernel(x,y,m), m.item() )
    else: 
        return lambda x, y: gauss_kernel(x,y,m)

def linear_kernel(x,y):
    """
    Computes the standard linear kernel k(x,y)= <x,y> 

    X - 2d array, samples on left hand side
    Y - 2d array, samples on right hand side, can be None in which case they are replaced by X

    returns: kernel matrix
    """
    K = torch.matmul(x,y.T)
    return K

if __name__ == "__main__":

    x,y = gen_couple().values()
    print('\n *** distance \n',distances(x,y))
    print('\n *** gauss_kernek_mediane \n',gauss_kernel_mediane(x,y)(x,y))
    
