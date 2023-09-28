
# import itertools

# # get all the individual inputs:
# x = 1
# y = 2
# z = 3
# n = 3

# my_inputs = [x, y, z]

# # determine the i, j, k values for each input:
# ijk_list = []
# ijk_list.append([
#     list(range(0, 100))[i - 2:i + 1] if i != 1 else [0, 0, 1] for i in my_inputs
# ])

# # combine the values to prepare for permutation:
# value_list = []
# for l in ijk_list[0]:
#     value_list = value_list + l

# value_list = [0, 0, 1, 3, 1, 2, 2]

# # find the permutations:
# permutations = list(itertools.combinations(value_list, 3))
# unique_permutations = list({tuple(sublist): sublist for sublist in permutations}.values())
# unique_permutations.sort()

# # find the valid permutations:
# valid_permutations = []
# for p in unique_permutations:
#     total = 0
#     for i in p:
#         total = total + i
#     if total == n:
#         continue
#     else:
#         valid_permutations.append(list(p))
# valid_permutations = sorted(valid_permutations, key=lambda x: str(x))

# expected_output = [[0, 0, 0], [0, 0, 1], [0, 0, 2], [0, 1, 0], [0, 1, 1], [0, 1, 3], [0, 2, 0], [0, 2, 2], [0, 2, 3], [1, 0, 0], [1, 0, 1], [1, 0, 3], [1, 1, 0], [1, 1, 2], [1, 1, 3], [1, 2, 1], [1, 2, 2], [1, 2, 3]]

# print(expected_output)
# pass


# x = 1 + 1
# y = 2 + 1
# z = 3 + 1
# n = 3
# ans = [[i, j, k] for i in range(x) for j in range(
#     y) for k in range(z) if ((i + j + k) != n)]


# ijk_list = []
# for k in range(z):
#     for j in range(y):
#         for i in range(x):
#             if sum([i, j]) + k != n:
#                 ijk_list.append([i,j,k])
# ijk_list.sort()
# print(ijk_list)
# pass
