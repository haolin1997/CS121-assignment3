import math
import numpy as np

class CosSimilarity():
    def __init__(self, query_v, doc_v):
        self.qv = query_v
        self.dv = doc_v
        self.similarity = self._get_sim()

    def _get_sim(self, qv, dv):
        nqv = self._normalization(qv)
        ndv = self._normalization(dv)
        result = np.dot(nqv,ndv)
        return result

    def _normalization(self, v):
        length = 0
        for c in v:
            length += c^2
        length = math.sqrt(length)

        new_v = list()
        for i in range(len(v)):
            new_v[i] = v / length

        return new_v
        
        