def firstOccurence(pattern, text):
    '''Utilizes the Boyer-Moore-Horspool algorithm for locating substrings'''
    patternLen = len(pattern)
    textLen = len(text)
    
    if patternLen > textLen:    # occurrence not possible
        return -1
    
    jump = []   # holds how many indices can be skipped
    for _ in range(256):
        jump.append(patternLen)     # all possible ord numbers
    for patternIndex in range(patternLen-1):
        jump[ord(pattern[patternIndex])] = patternLen - 1 - patternIndex
        
    textIndex = patternLen - 1
    while textIndex < textLen:
        patternIndex = patternLen - 1
        while patternIndex >= 0 and text[textIndex] == pattern[patternIndex]:
            patternIndex -= 1
            textIndex -= 1
        if patternIndex == -1:
            return textIndex + 1    # substring found
        textIndex += jump[ord(text[textIndex])]
    return -1

def allOccurences(text, pattern):
    searchedPositions = []
    textIndex = 0
    while True:
        subtextIndex = BoyerMooreHorspool(pattern, text)
        textIndex += subtextIndex
        if subtextIndex == -1:
            break
        searchedPositions.append(textIndex)
        text = text[subtextIndex+1:]
    print('Pattern \"' + pattern + '\" found at positions: ', searchedPositions)

def getText(fileName):
    try:
        page = open(fileName, 'r')
        text = str(page.read())
        page.close()
        return (None, text)
    except:
        return ('File could not be opened!', None)
