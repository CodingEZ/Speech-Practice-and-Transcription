import string

CHARFIT = 70

def setCharFit(length):
    global CHARFIT
    CHARFIT = length // 13

def filterText(text):
    """Filters of characters that are not in the alphabet and are not spaces."""
    alphabet = string.ascii_letters
    for index in range(len(text)-1, -1, -1):
        if text[index] not in alphabet and (text[index] != ' '):
            text = text[:index] + text[index+1:]
    return text.lower()

def reachMaxDepth(dictionary, depth=10):
    """Avoids an infinite loop in occurence searching."""
    for key in dictionary:
        if dictionary[key] >= depth:
            return True
    return False

def firstOccurence(pattern, text):
    """Utilizes the Boyer-Moore-Horspool algorithm for locating substrings"""
    patternLen = len(pattern)
    textLen = len(text)
    
    if patternLen > textLen:    # occurrence not possible
        return -1
    
    jump = []   # holds how many indices can be skipped
    for _ in range(256):
        jump.append(patternLen)     # all possible ord numbers
    for patternIndex in range(patternLen-1):
        jump[ord(pattern[patternIndex])] = patternLen - 1 - patternIndex

    appearances = {}
    textIndex = patternLen - 1
    while textIndex < textLen and textIndex != -1:
        patternIndex = patternLen - 1
        while patternIndex >= 0 and text[textIndex] == pattern[patternIndex]:
            patternIndex -= 1
            textIndex -= 1
        if patternIndex == -1:
            return textIndex + 1    # substring found
        textIndex += jump[ord(text[textIndex])]
        appearances[textIndex] = appearances.get(textIndex, 0) + 1
        if reachMaxDepth(appearances):
            break
    return -1

def allOccurences(text, pattern):
    """Finds all occurences of a substring within a string, using the BMH algorithm."""
    foundPositions = []
    textIndex = 0
    while True:
        subtextIndex = firstOccurence(pattern, text)
        textIndex += subtextIndex
        if subtextIndex == -1:
            break
        foundPositions.append(textIndex)
        text = text[subtextIndex+1:]
        textIndex += 1
    return foundPositions

def maxCommonIndices(wordList, textList, start):
    """Finds indices bounding longest common substring given the starting point."""
    maxMatchLength = 1
    maxMatchIndices = []
    text = ' '.join(textList)
    occurences = allOccurences(text, wordList[start])
    for occurence in occurences:
        if text[occurence + len(wordList[start])] != ' ':
            continue
        textShort = text[occurence:]
        textShortList = textShort.split(' ')
        for j in range(len(textShortList)):
            if start + j >= len(wordList) or wordList[start + j] != textShortList[j]:
                break
            
        if j > maxMatchLength:
            maxMatchLength = j
            maxMatchIndices = [(start, start + j, occurence)]
        elif j == maxMatchLength:
            maxMatchIndices.append( (start, start + j, occurence) )
    return maxMatchLength, maxMatchIndices

def longestCommonIndices(wordList, textList, textSet):
    """Finds the indices bounding the longest common substring."""
    maxMatchLength = 1
    maxMatchIndices = []
    for i in range(len(wordList)):
        if wordList[i] in textSet:
            matchLength, matchIndices = maxCommonIndices(wordList, textList, i)
            if matchLength > maxMatchLength:
                maxMatchLength = matchLength
                maxMatchIndices = matchIndices
            elif matchLength == maxMatchLength:
                maxMatchIndices.extend(maxMatchIndices)
    return maxMatchIndices

def findCommonIndices(wordList, textList, start):
    """Finds common substrings that match at least three consecutive words."""
    minMatchLength = 3
    matchIndices = []
    text = ' '.join(textList)
    occurences = allOccurences(text, wordList[start])
    for occurence in occurences:
        if text[occurence + len(wordList[start])] != ' ':
            continue
        textShort = text[occurence:]
        textShortList = textShort.split(' ')
        for j in range(len(textShortList)):
            if start + j >= len(wordList) or wordList[start + j] != textShortList[j]:
                break
            
        if j >= minMatchLength:
            matchIndices.append( (start, start + j, occurence) )
    return matchIndices

def commonIndices(wordList, textList, textSet):
    """Finds all common substrings of at least length three words."""
    allMatchIndices = []
    i = 0
    while i < len(wordList):
        if wordList[i] in textSet:
            matchIndices = findCommonIndices(wordList, textList, i)
            if len(matchIndices) > 0:
                allMatchIndices.extend(matchIndices)
                i += matchIndices[0][1] - matchIndices[0][0]
            else:
                i += 1
        else:
            i += 1
    return allMatchIndices

def allUnmatchedIndices(wordList, textSet):
    """Finds words that cannot be found in the transcription."""
    unMatched = set()
    for i in range(len(wordList)):
        if wordList[i] not in textSet:
            unMatched.add(i)
    return unMatched

def correctWordRatio(wordList, textList, textSet):
    """Calculates the ratio of correct words."""
    allMatchIndices = commonIndices(wordList, textList, textSet)
    correctCount = 0
    for match in allMatchIndices:
        correctCount += match[1] - match[0]
    lastOccurence = match[2]
    text = ' '.join(textList)[:lastOccurence]
    totalCount = text.count(' ') + match[1] - match[0]
    return correctCount / totalCount

def displayText(app):
    """Displays text with good formatting, using ellipses."""
    app.resetLog()
    app.updateLog(' Transcribed text: \n')

    if len(app.recordText) <= CHARFIT:
        app.updateLog('    ' + app.recordText + '\n')
        return
        
    start = CHARFIT
    while start >= 0 and app.recordText[start] != ' ':
        start -= 1
    end = len(app.recordText) - CHARFIT
    while end < len(app.recordText) and app.recordText[end] != ' ':
        end += 1
        
    if start < end:
        app.updateLog('    ' + app.recordText[:start] + ' ... \n' + \
                      '     ... ' + app.recordText[end:] + '\n')
        return
    app.updateLog('    ' + app.recordText[:CHARFIT] + ' ... \n' + \
                  '     ... ' + app.recordText[CHARFIT:] + '\n')

def displayLongestCommon(app, commonStrings):
    """Displays the longest common substring with good formatting, using ellipses."""
    app.updateLog(' Longest common strings:\n')
    for common in commonStrings:
        if len(common) <= CHARFIT:
            app.updateLog('    ' + common + '\n')
            continue
        
        start = CHARFIT
        while start >= 0 and common[start] != ' ':
            start -= 1
        end = len(common) - CHARFIT
        while end < len(common) and common[end] != ' ':
            end += 1
        if start < end:
            app.updateLog('    ' + common[:start] + ' ... \n     ... ' + common[end:] + '\n')
            continue
        app.updateLog('    ' + common[:CHARFIT] + ' ... \n     ... ' + common[CHARFIT:] + '\n')
    if len(commonStrings) > 3:
        app.updateLog('       ... and other strings ... ')
    app.updateLog('\n')

def displayCommon(app, commonStrings):
    """Displays all common substrings with good formatting, using ellipses."""
    app.updateLog(' Common strings:\n')
    for common in commonStrings[:3]:
        if len(common) <= CHARFIT:
            app.updateLog('    ' + common + '\n')
            continue
        
        start = CHARFIT
        while start >= 0 and common[start] != ' ':
            start -= 1
        end = len(common) - CHARFIT
        while end < len(common) and common[end] != ' ':
            end += 1
        if start < end:
            app.updateLog('    ' + common[:start] + ' ... \n     ... ' + common[end:] + '\n')
            continue
        app.updateLog('    ' + common[:CHARFIT] + ' ... \n     ... ' + common[CHARFIT:] + '\n')
    if len(commonStrings) > 3:
        app.updateLog('       ... and other strings ... ')
    app.updateLog('\n')

def displayUnmatched(app, unmatchedWords):
    """Displays unmatched words with good formatting, using ellipses."""
    app.updateLog(' Unmatched words:\n')
    if len(unmatchedWords) <= CHARFIT:
        app.updateLog('    ' + unmatchedWords + '\n')
        return

    start = CHARFIT
    while start >= 0 and unmatchedWords[start] != ' ':
        start -= 1
    end = len(unmatchedWords) - CHARFIT
    while end < len(unmatchedWords) and unmatchedWords[end] != ',':
        end += 1
    if start < end:
        app.updateLog('    ' + unmatchedWords[:start] + ' ... \n     ... ' + unmatchedWords[end:] + '\n')
    else:
        app.updateLog('    ' + unmatchedWords[:CHARFIT] + ' ... \n     ... ' + unmatchedWords[CHARFIT:] + '\n')    

def displayCorrectRatio(app, correctRatio):
    """Displays the correct word ratio."""
    app.updateLog('\n Ratio of correct words: %2.3f' % correctRatio)

def getText(fileName):
    page = open(fileName, 'r')
    text = str(page.read())
    page.close()
    text = filterText(text)
    return text
