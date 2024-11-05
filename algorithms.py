# Assuming this class is saved in a file named `algorithms.py`
class StringMatchingAlgorithms:
    @staticmethod
    def rabin_karp(pattern, text, q=101):
        m = len(pattern)
        n = len(text)
        d = 256  # Number of characters in the input alphabet
        p = 0  # Hash value for pattern
        t = 0  # Hash value for text
        h = pow(d, m - 1) % q

        for i in range(m):
            p = (d * p + ord(pattern[i])) % q
            t = (d * t + ord(text[i])) % q

        results = []

        for i in range(n - m + 1):
            if p == t:
                if text[i:i + m] == pattern:
                    results.append(i)

            if i < n - m:
                t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
                if t < 0:
                    t += q

        return results

    @staticmethod
    def KMPSearch(pattern, text):
        M = len(pattern)
        N = len(text)

        lps = [0] * M
        j = 0
        StringMatchingAlgorithms.computeLPSArray(pattern, M, lps)

        results = []
        i = 0

        while N - i >= M:
            if pattern[j] == text[i]:
                i += 1
                j += 1

            if j == M:
                results.append(i - j)
                j = lps[j - 1]

            elif i < N and pattern[j] != text[i]:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1

        return results

    @staticmethod
    def computeLPSArray(pattern, M, lps):
        length = 0
        lps[0] = 0

        i = 1
        while i < M:
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