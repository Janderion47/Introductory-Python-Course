data_list = [('apple', 5),
             ('banana', 2),
             ('orange', 8),
             ('grapes', 3),
             ('pineapple', 1)]


def conv_list_to_dict(stuff):
    out_dict = {}
    for key,value in stuff:
        out_dict[key] = value
    
    return out_dict

converted_thing=conv_list_to_dict(data_list)
print(converted_thing)