import pickle

# read data from pkl
with open('../data/air_dictionary.pkl', 'rb') as f:
    air_dict = pickle.load(f)
    print(air_dict)

with open('../data/optd_por_public.txt', encoding='utf-8', mode='r') as file:
    for line in file:
        air_list = line.split('^')
        if air_list[0] in air_dict:
            air_dict[air_list[0]] = air_list[32]

# print(air_dict)

with open('../data/airports_gmt_offset.pkl', 'wb') as f:
    pickle.dump(air_dict, f)
