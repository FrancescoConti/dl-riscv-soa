import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from adjustText import adjust_text
import matplotlib
import itertools
import string

dataframe = pd.read_excel('data.xlsx')
matplotlib.rcParams.update({
    'font.family':  'sans-serif',
    'font.sans-serif':['Helvetica']
})

dataframe = dataframe.replace("-", "NaN")
dataframe.columns = dataframe.columns.astype(str)
dataframe[dataframe.columns[5]] = dataframe[dataframe.columns[5]].apply(pd.to_numeric, errors='coerce')
dataframe[dataframe.columns[6]] = dataframe[dataframe.columns[6]].apply(pd.to_numeric, errors='coerce')
dataframe[dataframe.columns[7]] = dataframe[dataframe.columns[7]].apply(pd.to_numeric, errors='coerce')
dataframe[dataframe.columns[7]] = dataframe[dataframe.columns[6]]/dataframe[dataframe.columns[5]]*1000

# Drop NaN
dfclean = dataframe.dropna(subset=[dataframe.columns[5], dataframe.columns[6]])

sns.set_theme(style="whitegrid")
style = ["FP64", "FP32", "FP16", "FP8", "FP4", "INT32", "INT8", "INT4", "INT2 x INT8", "INT2 x INT4", "INT2", "Analog"]
g = sns.relplot(data=dfclean, edgecolor="black", style=dfclean.columns[9], style_order=style, x=dfclean.columns[5], y=dfclean.columns[6], hue=dfclean.columns[10], s=100, label=dfclean.columns[1], palette=["red", "green", "blue"], height=6, aspect=2)
g.set(xscale="log")
g.set(yscale="log")

# Turn on minor ticks for the x and y axes
plt.minorticks_on()

# Specify the minor grid's appearance
plt.grid(which='minor', linestyle=':', linewidth='0.7', color='black')
plt.grid(which='major', linestyle=':', linewidth='0.8', color='black')

plt.plot((1,1e5), (1e-1, 1e4), linestyle='--', linewidth='0.7', color='black') # 100GOPS/W
plt.plot((1,1e5), (1, 1e5),    linestyle='--', linewidth='0.7', color='black') # 1000GOPS/W
plt.plot((1,1e5), (1e1, 1e6),  linestyle='--', linewidth='0.7', color='black') # 1000GOPS/W
plt.xlim((1e1,1e5))
plt.ylim((1, 3e6))

def generate_alphabetic_symbols(n):
    letters = string.ascii_lowercase + string.ascii_uppercase
    result = []
    length = 1

    while len(result) < n:
        # Create combinations of the current length
        for combo in itertools.product(letters, repeat=length):
            result.append(''.join(combo))
            if len(result) == n:
                return result
        length += 1

    return result

symbols = generate_alphabetic_symbols(len(dfclean))

# Add labels to the markers
df = dfclean.sort_values(by=dfclean.columns[5])
df = df[df[df.columns[5]] >= 10]
anns = []
anns = np.asarray([plt.text(df.iloc[i][5]*1.06, df.iloc[i][6]*1.06, f"{symbols[i]}", fontstyle='italic', fontweight='bold') for i in range(len(df))])

ss = ""
for i in range(len(df)):
    s = (df.iloc[i][0]).replace(" ", "&nbsp;") + f"&nbsp;[<a href=https://doi.org/{df.iloc[i][19]}>{df.iloc[i][19]}</a>]"
    ss += f"<b><i>{symbols[i]}</i></b>:&nbsp;{s}, \n"

x = np.asarray([df.iloc[i][5] for i in range(len(df))])
y = np.asarray([df.iloc[i][6] for i in range(len(df))])
plt.text(1e1, 1.1, "100 GOPS/W", rotation=14)
plt.text(1e1, 1.1e1, "1 TOPS/W", rotation=14)
plt.text(1e1, 1.1e2, "10 TOPS/W", rotation=14)

adjust_text(anns.tolist(), x, y)

# Adjust layout to make space for the text box
plt.subplots_adjust(bottom=0.2)

plt.savefig("plot.png", dpi=500)

# Save the ss content to a text file
with open("plot_info.txt", "w") as file:
    file.write(ss)