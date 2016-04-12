import math

def winner_only_re(predictions):
    asset = 1.0
    init = asset
    for prediction in predictions:
        if math.isnan(prediction.match_winner_prob['p1']):
            continue
        if prediction.round == 7:
            stake = 1.0
        elif prediction.round == 6:
            stake = 1.0 / 2
        elif prediction.round == 5:
            stake = 1.0 / 4
        elif prediction.round == 4:
            stake = 1.0 / 8
        elif prediction.round == 3:
            stake = 1.0 / 16
        if prediction.match_winner_prob['p1'] > prediction.match_winner_prob['p2'] and prediction.match_winner == 'p1':
            asset += stake*(prediction.match_winner_odds['p1']-1)
        elif prediction.match_winner_prob['p2'] > prediction.match_winner_prob['p1'] and prediction.match_winner == 'p2':
            asset += stake*(prediction.match_winner_odds['p2']-1)
        else:
            asset -= stake
    return asset/init


def winner_hedge_re(predictions):
    asset = 1.0
    init = asset
    for prediction in predictions:
        if math.isnan(prediction.match_winner_prob['p1']):
            continue
        p1_invest_pct = cal_invest_pct(prediction.match_winner_prob['p1'])
        if prediction.round == 7:
            stake = 1.0
        elif prediction.round == 6:
            stake = 1.0 / 2
        elif prediction.round == 5:
            stake = 1.0 / 4
        elif prediction.round == 4:
            stake = 1.0 / 8
        elif prediction.round == 3:
            stake = 1.0 / 16
        if prediction.match_winner_prob['p1'] > prediction.match_winner_prob['p2'] and prediction.match_winner == 'p1':
            asset += stake*(prediction.match_winner_odds['p1']-1)*p1_invest_pct
        elif prediction.match_winner_prob['p2'] > prediction.match_winner_prob['p1'] and prediction.match_winner == 'p2':
            asset += stake*(prediction.match_winner_odds['p2']-1)*(1-p1_invest_pct)
        else:
            asset -= stake
    return asset/init


def set_winner_only_re(predictions):
    asset = 1.0
    init = asset
    for prediction in predictions:
        if math.isnan(prediction.match_winner_prob['p1']):
            continue
        if prediction.round == 7:
            stake = 1.0
        elif prediction.round == 6:
            stake = 1.0 / 2
        elif prediction.round == 5:
            stake = 1.0 / 4
        elif prediction.round == 4:
            stake = 1.0 / 8
        elif prediction.round == 3:
            stake = 1.0 / 16
        if prediction.match_winner_prob['p1'] > 0.5:
            # predicting p1 to win
            if prediction.match_score == '3:0':
                adjust_pct = prediction.match_score_prob['3:0'] / (prediction.match_score_prob['3:0']+prediction.match_score_prob['3:1']+prediction.match_score_prob['3:2'])
                asset += (prediction.match_score_odds['3:0'] * adjust_pct - 1) * stake
            elif prediction.match_score == '3:1':
                adjust_pct = prediction.match_score_prob['3:1'] / (prediction.match_score_prob['3:0']+prediction.match_score_prob['3:1']+prediction.match_score_prob['3:2'])
                asset += (prediction.match_score_odds['3:1'] * adjust_pct - 1) * stake
            elif prediction.match_score == '3:2':
                adjust_pct = prediction.match_score_prob['3:2'] / (prediction.match_score_prob['3:0']+prediction.match_score_prob['3:1']+prediction.match_score_prob['3:2'])
                asset += (prediction.match_score_odds['3:2'] * adjust_pct - 1) * stake
            else:
                asset -= stake
        else:
            # predicting p2 to win
            if prediction.match_score == '0:3':
                adjust_pct = prediction.match_score_prob['0:3'] / (prediction.match_score_prob['0:3']+prediction.match_score_prob['1:3']+prediction.match_score_prob['2:3'])
                asset += (prediction.match_score_odds['0:3'] * adjust_pct - 1) * stake
            elif prediction.match_score == '1:3':
                adjust_pct = prediction.match_score_prob['1:3'] / (prediction.match_score_prob['0:3']+prediction.match_score_prob['1:3']+prediction.match_score_prob['2:3'])
                asset += (prediction.match_score_odds['1:3'] * adjust_pct - 1) * stake
            elif prediction.match_score == '2:3':
                adjust_pct = prediction.match_score_prob['2:3'] / (prediction.match_score_prob['0:3']+prediction.match_score_prob['1:3']+prediction.match_score_prob['2:3'])
                asset += (prediction.match_score_odds['2:3'] * adjust_pct - 1) * stake
            else:
                asset -= stake
    return asset / init


def cal_invest_pct(prob):
    return (prob ** 4) * (1 + 4 * (1 - prob) + 10 * (1 - prob) ** 2) + (20 * (prob * (1 - prob)) ** 3) * (prob ** 2) * ((1 - 2 * prob * (1 - prob)) ** (-1))