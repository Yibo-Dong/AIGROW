import sys
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

data_path = sys.argv[1]
output_path = data_path.split('.')[0] + ".pdf"
data = pd.read_csv(data_path)

plt.figure(figsize=(16,16))

my_pal = {'AIGEN':"b", "AIGFUZZ":"m", "AIGROW":"#f89588", "HWMCC":"#63b2ee"}
sns.set(style = "white")
fig = sns.boxplot(x=' ', y="Ratio", data=data, width=0.5, linewidth=6, palette=my_pal, fliersize=25)

if data_path.find("car") != -1:
    y = [0, 25, 50, 75]
    ylabel = [0, 25, 50, 75]
else: 
    y = [0, 15, 30, 45]
    ylabel = [0, 15, 30, 45]
fig.set_yticks(y)
fig.set_yticklabels(ylabel, fontsize=70)
fig.set_ylabel(' ', fontsize=42)

xlabel = ['AIGEN', 'AIGFUZZ', 'AIGROW','HWMCC']
fig.set_xticklabels(xlabel, fontsize=70, rotation=45)

plt.tight_layout()
fig.get_figure().savefig(output_path)
