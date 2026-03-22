def getPermutations(length):
    permutations = []
    queue = [([], list(range(length)))]
    while queue:
        next = queue.pop(0)
        if len(next[1]) > 0:
            for element in next[1]:
                leftCopy = next[1].copy()
                leftCopy.remove(element)
                queue.append((next[0] + [element], leftCopy))
        else:
            permutations += [next[0]]
    return permutations