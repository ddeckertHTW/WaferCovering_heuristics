def minkowskiSumAllPermutations(A, B):
    sum_set = set()
    for offset_a in A:
        A_Offset = [(x - offset_a[0], y - offset_a[1]) for x, y in A]
        for a in A_Offset:
            for b in B:
                sum_set.add((a[0] + b[0], a[1] + b[1]))

    return list(sum_set)