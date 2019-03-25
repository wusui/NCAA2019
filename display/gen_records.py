def gen_records(in_data):
    rec_vec = []
    factor = 0
    for rec in in_data:
        new_rec = {}
        if factor == 0:
            expon = 2 * len(in_data[rec][1]) - 1
            factor = 2 ** expon
        new_rec['name'] = rec
        new_rec['winning_outcomes'] = sum(in_data[rec][1][0])
        new_rec['percentage'] = in_data[rec][0] / factor
        new_rec['next_round'] = in_data[rec][1]
        rec_vec.append(new_rec)
    ret_list = sorted(rec_vec, reverse=True,
                      key=lambda item: (item['winning_outcomes'],
                                        item['percentage']))
    return ret_list
