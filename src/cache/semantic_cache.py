import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class SemanticCache:

    def __init__(self, threshold=0.75):

        self.threshold = threshold

        # cache entries
        self.cache = []

        self.hit_count = 0
        self.miss_count = 0

    def lookup(self, query_embedding):

        best_score = 0
        best_entry = None

        for entry in self.cache:

            similarity = cosine_similarity(
                query_embedding,
                entry["embedding"]
            )[0][0]

            if similarity > best_score:

                best_score = similarity
                best_entry = entry

        if best_score >= self.threshold:

            self.hit_count += 1

            return True, best_entry, best_score

        self.miss_count += 1

        return False, None, None

    def store(self, query, embedding, result, cluster):

        entry = {
            "query": query,
            "embedding": embedding,
            "result": result,
            "cluster": cluster
        }

        self.cache.append(entry)

    def stats(self):

        total = self.hit_count + self.miss_count

        hit_rate = 0 if total == 0 else self.hit_count / total

        return {
            "total_entries": len(self.cache),
            "hit_count": self.hit_count,
            "miss_count": self.miss_count,
            "hit_rate": hit_rate
        }

    def clear(self):

        self.cache = []
        self.hit_count = 0
        self.miss_count = 0