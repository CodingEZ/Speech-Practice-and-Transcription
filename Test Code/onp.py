"""
The algorithm implemented here is based on "An O(NP) Sequence Comparison Algorithm"                                   
by described by Sun Wu, Udi Manber and Gene Myers 
"""

#########################################################################################
    # Text comparison algorithm: https://github.com/cubicdaiya/onp/tree/master/python
    # O(NP) Sequence Comparison Algorithm
    #########################################################################################

def editdistance(str1, str2):
    len1 = len(str1)
    len2 = len(str2)
    if len1 >= len2:    # switch such that str2 has greater length in all cases
        str1, str2 = str2, str1
        len1, len2 = len2, len1
        
    offset = len1 + 1
    delta  = len2 - len1
    size   = len1 + len2 + 3
    misplaced = [ -1 for _ in range(size) ]
    p = -1
    while True:
        p += 1
        for k in range(-p, delta, 1):
            misplaced[k+offset] = snake(str1, str2, len1, len2, k, misplaced[k-1+offset]+1, misplaced[k+1+offset])
        for k in range(delta+p, delta, -1):
            misplaced[k+offset] = snake(str1, str2, len1, len2, k, misplaced[k-1+offset]+1, misplaced[k+1+offset])
        misplaced[delta+offset] = snake(str1, str2, len1, len2, delta, misplaced[delta-1+offset]+1, misplaced[delta+1+offset])
        if misplaced[delta+offset] >= len2:
            break
    return delta + 2 * p
    
def snake(str1, str2, len1, len2, k, p, pp):
    y = max(p, pp)
    x = y - k
    while x < len1 and y < len2 and str1[x] == str2[y]:
        x += 1
        y += 1
    return y

def test(str1, str2):
    import itertools
    words1 = str1.split(' ')
    words2 = str2.split(' ')
x = editdistance('great ideas of theoretical computer science', 'of science great theoretical computer ideas')
print(x)
