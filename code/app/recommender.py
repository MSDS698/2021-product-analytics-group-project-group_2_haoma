class Recommender():
    score_keys = ['score_1_name', 'score_2_name', 'score_3_name']

    def __init__(self):
        ...

    def recommend(self, summary):
        ...
        recommendations = ['1ST CHOICE HOME HEALTH CARE',
                           'ANX HOME HEALTHCARE',
                           'MERIDIAN HOME HEALTH']
        return recommendations

    def get_metrics(self, recommendations, summary):
        ...
        scores = {}
        for agency in recommendations:
            scores[agency] = {}
            scores[agency][self.score_keys[0]] = 10
            scores[agency][self.score_keys[1]] = 7
            scores[agency][self.score_keys[2]] = 8
        return scores

    def get_column_names(self):
        names = []
        for k in self.score_keys:
            names += [" ".join(k.split("_")).title()]
        return names
