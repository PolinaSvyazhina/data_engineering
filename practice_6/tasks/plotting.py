import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

pd.set_option("display.max_row", 20, "display.max_columns", 60)


def read_file(file_name):
    return pd.read_csv(file_name)


def read_types(file_name):
    dtypes = {}

    with open(file_name, mode='r') as file:
        dtypes = json.load(file)

    for key in dtypes.keys():
        if dtypes[key] == 'category':
            dtypes[key] = pd.CategoricalDtype()
        else:
            dtypes[key] = np.dtype(dtypes[key])
        return dtypes


need_dtypes = read_types("../results/dtypes.json")
dataset = pd.read_csv('../results/df.csv', usecols=lambda x: x in need_dtypes.keys(), dtype=need_dtypes)
dataset.info(memory_usage='deep')

# plot = sns.histplot(data=dataset, x="day_of_week", hue="day_of_week", bins=100)
# plot.get_figure().savefig(os.path.join(res_file, os.path.normpath('day_of_week_2.png')))

# plot = dataset['day_of_week'].hist()
# plot.get_figure().savefig(os.path.join(res_file, os.path.normpath('day_of_week.png')))

# d2 = dataset.groupby(['number_of_game'])['number_of_game'].count()
# circ = d2.plot(kind='pie', y=d2.keys())
# circ.get_figure().savefig(os.path.join(res_file, os.path.normpath('number_of_game.png')))

# plt.figure(figsize=(30,5))
# plt.plot(dataset.groupby(["day_of_week"])['length_minutes'].sum().values, marker='*', color='green')
# plt.savefig(os.path.join(res_file, os.path.normpath('length_minutes_on_day.png')))

# plot = sns.boxplot(data=dataset, x='number_of_game', y='h_errors')
# plot.get_figure().savefig(os.path.join(res_file, os.path.normpath('error_on_play_1.png')))

# data = dataset.copy()
# plt.figure(figsize=(16,16))
# plot = sns.heatmap(data.corr())
# plot.get_figure().savefig(os.path.join(res_file, os.path.normpath('corr.png')))
