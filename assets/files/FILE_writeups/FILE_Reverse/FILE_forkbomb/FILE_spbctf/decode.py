def xor(s: bytes, key: list[int]) -> bytes:
   return bytes([s[i] ^ key[i % len(key)] for i in range(len(s))])


def perm(key, input_nums):
    for i in input_nums:
        tmp = key[i]

        key[i] = key[i + 1]
        key[i + 1] = tmp;


def bubble_sort(arr):
    swaps = []
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps.append(j)
                swapped = True

        if not swapped:
            break

    return swaps


# main()
if __name__ == '__main__':
    s = b'cPK}[aYr^@ZZR`C]TBP_\\Y_U\x7fUWE'
    key = [8, 7, 5, 4, 1, 3, 2, 6, 9, 10]
    swaps = bubble_sort(key.copy())
    perm(key, swaps)
    xor_key = ''.join([str(n) for n in swaps]).encode()
    print(xor_key)

    print(xor(s, xor_key).decode())
