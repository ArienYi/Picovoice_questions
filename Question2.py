from typing import Sequence, List
from collections import defaultdict

'''
Question 2:Given a sequence of phonemes as input (e.g. ["DH","EH","R","DH","EH","R"]), 
find all the combinations of the words that can produce this sequence 
(e.g. [["THEIR","THEIR"], ["THEIR","THERE"], ["THERE","THEIR"], ["THERE", THERE"]]). 
You can preprocess the dictionary into a different data structure if needed.
'''

'''
DFS Approach.
We use a dfs algorithm to explore all possible combinations of words and check if its phonemes 
matches the corresponding content in the dictionary. Also to reduce repetition, we use a memo 
to store decompositions of phonemes[i] to optimize the algorithm.
'''


def find_word_combos_with_pronunciation(phonemes: Sequence[str]) -> Sequence[Sequence[str]]:
    # build an index from the first phoneme -> [(word, wordPhonemes), ...]
    index_by_first = defaultdict(list)
    for w, phns in dict_map.items():
        if phns:
            index_by_first[phns[0]].append((w, phns))

    n = len(phonemes)
    # memo[i] will store all decompositions of phonemes[i:]
    memo = {}

    def dfs(i: int) -> List[List[str]]:
        # we find a valid decomposition, no words needed from here on
        if i == n:
            return [[]]

        # we reached a stored decomposition, no further manipulation needed
        if i in memo:
            return memo[i]

        res = []
        first_phoneme = phonemes[i]

        # get all candidate words that start with this phoneme from index
        candidates = index_by_first[first_phoneme]

        for (word, word_phonemes) in candidates:
            length_of_phns = len(word_phonemes)
            # check if word_phonemes matches the chunk phonemes[i:i+length_of_word]
            if i + length_of_phns <= n and phonemes[i: i + length_of_phns] == word_phonemes:
                # recurse on remainder
                sub_solutions = dfs(i + length_of_phns)
                # add 'word' to each sub-solution
                for seq in sub_solutions:
                    res.append([word] + seq)

        memo[i] = res
        return res

    return dfs(0)


'''
Pure Backtrack Approach.
Very similar to DFS approach but use UNDO instead of memo.
'''


def find_word_combos_with_pronunciation_backtrack(phonemes: Sequence[str]) -> Sequence[Sequence[str]]:
    res = []
    n = len(phonemes)

    def backtrack(i, current_sequence):
        # If we've consumed all phonemes, record a valid decomposition
        if i == n:
            res.append(current_sequence[:])  # append a copy
            return

        # Otherwise, try every word in the dictionary to see if it can match at position i
        for word, word_phonemes in dict_map.items():
            length_of_phns = len(word_phonemes)
            # Check boundary and match
            if i + length_of_phns <= n and phonemes[i: i + length_of_phns] == word_phonemes:
                # Choose
                current_sequence.append(word)
                # Explore deeper
                backtrack(i + length_of_phns, current_sequence)
                # Backtrack (undo the choice)
                current_sequence.pop()

    # Start from index 0 with an empty current solution
    backtrack(0, [])
    return res


# sample dictionary
dict_map = {
    "ABACUS": ["AE", "B", "AH", "K", "AH", "S"],
    "BOOK": ["B", "UH", "K"],
    "THEIR": ["DH", "EH", "R"],
    "THERE": ["DH", "EH", "R"],
    "TOMATO1": ["T", "AH", "M", "AA", "T", "OW"],
    "TOMATO2": ["T", "AH", "M", "EY", "T", "OW"],
}

# test the code with input phonemes ["DH","EH","R","DH","EH","R"]
input_phonemes = ["DH", "EH", "R", "DH", "EH", "R"]
all_combos = find_word_combos_with_pronunciation_backtrack(input_phonemes)
print("All possible sequences:\n", all_combos)
