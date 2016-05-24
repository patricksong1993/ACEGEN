def populate_length(cur_length, pre_length, set_length):
    for p in pre_length:
        for s in set_length:
            cur_length[p+s] = cur_length.get(p+s, 0)+pre_length[p]*set_length[s]

def inverse_score(score):
    if type(score) is str:
        scores = score.split(':')
        return scores[1] + ":" + scores[0]
    if type(score) is int:
        return 0 - score