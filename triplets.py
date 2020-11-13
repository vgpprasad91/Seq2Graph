
import re

from relationship_extraction import RelExtractionClassifier

re_extract = RelExtractionClassifier()


class GetTriplets:

    def __init__(self):
        self.triplet1 = []
        self.triplet2 = []
        self.triplet3 = []
        self.score = []

    def _add_triplets(self, term, term1, string):
        result = re.search(term + "(.*)" + term1, string)
        self.triplet1.append(term)
        self.triplet2.append(re_extract.predict(result.group(1))[0])
        self.score.append(re_extract.predict(result.group(1))[1])
        self.triplet3.append(term1)

    # Todo Optimize for better
    def predict_triplets(self, phrases, text):
        for x in range(0, len(phrases)):
            for y in range(0, len(phrases[x])):
                for z in range(0, len(phrases[x][y]) - 1):
                    try:
                        if len(phrases[x][y]) == 1:
                            pass
                        else:
                            self._add_triplets(phrases[x][y][z], phrases[x][y][z], text[x][y])
                        if z == len(phrases[x][y]) - 2:
                            pass
                    except:
                        pass
        return (self.triplet1, self.triplet2, self.score, self.triplet3)