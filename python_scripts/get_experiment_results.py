"""Script to combine and evaluate the results of ZeroMQ vs LSL latency
experiment."""
import pandas as pd

exp_unity = pd.read_csv("./experiment_results/lsl2_unity.csv")
exp_python = pd.read_csv("./experiment_results/lsl2_python.csv")

df = pd.DataFrame()
df['msg_send_time'] = exp_python[exp_python.columns[1]]
df['msg_send'] = exp_python[exp_python.columns[2]]
df['msg_received_time'] = exp_unity[exp_unity.columns[0]]
df['msg_received'] = exp_unity[exp_unity.columns[1]]

time_diff = []
for index, row in df.iterrows():
    if index > 1:
        time_diff.append(int(row['msg_received_time'][-6:]) - int(row['msg_send_time'][-6:]))
    else:
        time_diff.append("error")
df['time_difference'] = time_diff
df.to_csv("./experiment_results/lsl_combined.csv")