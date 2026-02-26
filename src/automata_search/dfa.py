def compute_lps_array(pattern):
    """
    computes the longest prefix suffix for the kmp algorithm. 
    this tells the machine where to backtrack to if a mismatch happens
    """
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text, pattern):
    """
    perfoms the kmp operation and returns the number of matches found
    """

    M = len (pattern)
    N = len(text)

    if M == 0: return 0

    lps = compute_lps_array(pattern)

    i = 0
    j = 0
    matches = 0

    while i < N:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == M:
            matches += 1
            j = lps[j-1]
        
        elif i < N and pattern[j] != text[i]:
            if j!=0:
                j = lps[j-1]
            else:
                i += 1
    return matches
