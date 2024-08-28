import numpy as np
import matplotlib.pyplot as plt
import math

def infocontent(p):
    
    # Alter the equation below to provide the correct Shannon information 
    # content:

    return -np.log2(p)

def entropy(p):  
    # First make sure the array is now a numpy array
    if type(p) != np.array:
        p = np.array(p)

    # Should we check any potential error conditions on the input?
    if (abs(np.sum(p) - 1) > 0.00001):
        raise Exception("Probability distribution must sum to 1: sum is %.4f" % np.sum(p))
    
    # We need to take the expectation value over the Shannon info content at
    # p(x) for each outcome x:
    weightedShannonInfos = p*(infocontent(p))
    # nansum ignores the nans from calling infocontent(0), but we still get the warning if an entry in p is zero
    return np.nansum(weightedShannonInfos)

def entropyempirical(xn):

    # First, error checking, and converting argument into standard form:    
    if type(xn) == list:
        xn = np.array(xn)
    if xn.ndim == 1:
        xn = np.reshape(xn,(len(xn), 1)) #reshaping our 1-dim vector to numpy format of a column vector
    [xnSamples,xnDimensions] = xn.shape
    
    # We need to work out the alphabet here.
    # The following returns a vector of the alphabet:    
    symbols = np.unique(xn, axis=0)
    # It would be faster to call:
    #   [symbols, counts] = np.unique(xn, axis=0, return_counts=True)
    # but we'll count the samples manually below for instructive purposes

	# Next we need to count the number of occurances of each symbol in 
	# the alphabet:
    counts = []
    for symbol in symbols:
        count = 0
        for row in xn:
            if (row==symbol).all():
                count += 1
        counts.append(count)
    counts = np.array(counts);
    # Now normalise the counts into probabilities:
    probabilities = counts / xnSamples
    
    # Once we have the probabilities we can simply call our existing function:
    result = entropy(probabilities)
    
    return result, symbols, probabilities

def jointentropyempirical(xn, yn=[]):
    
    # First, error checking, and converting argument into standard form:    
    xn = np.array(xn)
    # Convert to column vectors if not already:
    if xn.ndim == 1:
        xn = np.reshape(xn,(len(xn),1))
    yn = np.array(yn)
    if (yn.size > 0):
        # Convert to column vectors if not already:
        if yn.ndim == 1:
            yn = np.reshape(yn,(len(yn),1))
        [rx,cx] = xn.shape
        [ry,cy] = yn.shape
        # Check that their number of rows are the same:
        assert(rx == ry)
        # Now joint them up so we only need work with xn
        xn = np.concatenate((xn,yn), axis=1)
        
    # TRICK: Next combine the row vectors in each sample into a single 
    #  symbol (being the index from the symbols array,
    # so that we can simply compute entropy on that combined symbol
    [symbols, symbolIndexForEachSample] = np.unique(xn, axis=0, return_inverse=True)

    # And compute the entropy using our existing function:
    [result, symbols_of_indices, probabilities] = entropyempirical(symbolIndexForEachSample);

    # The order of symbols is the same as their order for the probabilities

    return result, symbols, probabilities

def mutualinformationempirical(xn,yn):
    
    # First, error checking, and converting argument into standard form:    
    xn = np.array(xn)
    # Convert to column vectors if not already:
    if xn.ndim == 1:
        xn = np.reshape(xn,(len(xn),1))
    yn = np.array(yn)
    if yn.ndim == 1:
        yn = np.reshape(yn,(len(yn),1))
    [rx,cx] = xn.shape
    [ry,cy] = yn.shape

    # Should we check any potential error conditions on the input?
    # Check that their number of rows are the same:
    assert(rx == ry)

    # We need to compute H(X) + H(Y) - H(X,Y):
    # 1. joint entropy:
    (H_XY, xySymbols, xyProbs) = jointentropyempirical(xn, yn); # How to compute this empirically ...?
    # 2. marginal entropy of Y: (call 'joint' in case yn is multivariate)
    (H_Y, ySymbols, yProbs) = jointentropyempirical(yn)
    # 3. marginal entropy of X: (call 'joint' in case yn is multivariate)
    (H_X, xSymbols, xProbs) = jointentropyempirical(xn);
	
    result = H_X + H_Y - H_XY;
    return result