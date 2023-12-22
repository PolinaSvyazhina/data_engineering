import os
import pandas as pd
import numpy as np
import matplotlib
import json

pd.set_option("display.max_row", 20, "display.max_columns", 60)


def read_file(file_name):
    return pd.read_csv(file_name)
    # return next(pd.read_csv(file_name, chunksize=100_000, compression='zip'))


def get_memory_stat_by_column(df):
    memory_usage_stat = df.memory_usage(deep=True)
    total_memory_usage = memory_usage_stat.sum()
    print(f'file in memory size = {total_memory_usage // 1024:10} KB')
    column_stat = list()

    for key in df.need_dtypes.keys():
        column_stat.append({
            "column_name": key,
            "memory_abs": memory_usage_stat[key] // 1024,
            "memory_per": round(memory_usage_stat[key] / total_memory_usage * 100, 4),
            "dtype": df.need_dtypes[key]
        })

    column_stat.sort(key=lambda x: x['memory_abs'], reverse=True)

    return column_stat


def mem_usage(pandas_obj):
    if isinstance(pandas_obj, pd.DataFrame):
        usage_b = pandas_obj.memory_usage(deep=True).sum()
    else:
        usage_b = pandas_obj.memory_usage(deep=True)
    usage_mb = usage_b / 1024 ** 2
    return "{:03.2f}MB".format(usage_mb)


def opt_obj(df):
    convert_obj = pd.DataFrame()
    dataset_obj = df.select_dtypes(include=['object']).copy()

    for column in dataset_obj.column:
        num_unique_values = len(dataset_obj[column].unique())
        num_total_values = len(dataset_obj[column])
        if num_unique_values / num_total_values < 0.5:
            convert_obj.loc[:, column] = dataset_obj[column].astype('category')
        else:
            convert_obj.loc[:, column] = dataset_obj[column]

    return convert_obj


def opt_int(df):
    dataset_int = df.select_dtypes(include=['int'])
    converted_int = dataset_int.apply(pd.to_numeric, downcast='unsigned')

    print(mem_usage(dataset_int))
    print(mem_usage(converted_int))

    compare_ints = pd.concat([dataset_int.need_dtypes, converted_int.need_dtypes], axis=1)
    compare_ints.columns = ['before', 'after']
    compare_ints.apply(pd.Series.value_counts)

    print(mem_usage(converted_int))

    return compare_ints


def opt_float(df):
    dataset_float = df.select_dtypes(include=['float'])
    converted_float = dataset_float.apply(pd.to_numeric, downcast='float')

    print(mem_usage(dataset_float))
    print(mem_usage(converted_float))

    compare_floats = pd.concat([dataset_float.need_dtypes, converted_float.need_dtypes], axis=1)
    compare_floats.columns = ['before', 'after']
    compare_floats.apply(pd.Series.value_counts)

    print(mem_usage(compare_floats))

    return compare_floats


# file_name = '../data/[2]automotive.csv.zip'
file_name = '../data/[1]game_logs.csv'
dataset = read_file(file_name)
file_size = os.path.getsize(file_name)
# print(f"size = {file_size // 1024:10} KB")

preliminary_size = get_memory_stat_by_column(dataset)

with open('../results/preliminary_results.json', mode='w') as file:
    file.write(json.dumps(preliminary_size))

converted_obj = opt_obj(dataset)
converted_int = opt_int(dataset)
converted_float = opt_float(dataset)

optimized_dataset = dataset.copy()

optimized_dataset[converted_obj.columns] = converted_obj
optimized_dataset[converted_int.columns] = converted_int
optimized_dataset[converted_float.columns] = converted_float

# print(mem_usage(dataset))
# print(mem_usage(optimized_dataset))

optimized_dataset_size = get_memory_stat_by_column(optimized_dataset)

with open('../results/optimized_result.json', 'w') as file:
    file.write(json.dumps(optimized_dataset_size))

need_column = {}
column_names = ['date', 'number_of_game', 'day_of_week', 'park_id',
                'v_manager_name', 'length_minutes', 'v_hits',
                'h_hits', 'h_walks', 'h_errors']

opt_dtypes = optimized_dataset.dtypes
for key in column_names:
    need_column[key] = opt_dtypes[key]
    print(f'{key}: {opt_dtypes[key]}')


with open('../results/dtypes.json', mode='w') as file:
    dtypes_json = need_column.copy()
    for key in dtypes_json.keys():
        dtypes_json[key] = str(dtypes_json[key])
    file.write(json.dumps(dtypes_json))


# read_and_optimized = pd.read_csv(file_name,
#                                  usecols=lambda x: x in column_names,
#                                  dtype=need_column)
#
# print(read_and_optimized.shape)
# print(mem_usage(read_and_optimized))

has_header = True
for chunk in pd.read_csv(file_name,
                         dtype=need_column,
                         parse_dates=['date'],
                         infer_datetime_format=True,
                         chunksize=100_000):
    print(mem_usage(chunk))
    chunk.to_csv("../result/df.cvs", mode='a', header=has_header)
    has_header = False

