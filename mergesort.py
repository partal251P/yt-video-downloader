def fusion(list):
    """
    A simple Mergesort
    :param list: list()
    :return: list()
    """
    if len(list) > 1:
        left = list[:len(list) // 2]
        right = list[len(list) // 2:]

        self.fusion(left)
        self.fusion(right)

        i, j, k = 0, 0, 0
        while i < len(left) and j < len(right):
            if int(left[i]) < int(right[j]):
                list[k] = left[i]
                i += 1
            else:
                list[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            list[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            list[k] = right[j]
            j += 1
            k += 1
    return list