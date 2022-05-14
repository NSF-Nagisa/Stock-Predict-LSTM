from lstm import AWLSTM
import csv

Us = [4, 8, 16, 32]
Ts = [1, 2, 5, 10, 15]
l2s = [0.001, 0.01, 0.1, 1]
las = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1]
les = [0.001, 0.005, 0.01, 0.05, 0.1]

result = []

for l2 in l2s:
    for T in Ts:
        for U in Us:
            paras = {'seq': int(T),
                     'unit': int(U),
                     'alp': float(l2),
                     'bet': 0.01,
                     'eps': 0.01,
                     'lr': 0.01 
                    }
            model = AWLSTM(data_path='./data/SSE50/pred', model_path='.', model_save_path='./tmp/model',parameters=paras, hinge=1, att=1, batch_size=1024,
                            tra_date='2018-01-02', val_date='2020-10-09', tes_date='2021-03-01')
            _, test = model.train()
            result.append(test['acc'])


with open('./test.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for row in result:
        writer.writerow(row)


