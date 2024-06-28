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

# Create HTML table content
html_content = """
<table id="data-table" class="display" style="width:100%">
    <thead>
        <tr>
            <th>#</th>
            <th>Name</th>
            <th>Category</th>
            <th>Technology node</th>
            <th>Area [mm2]</th>
            <th>Power [mW]</th>
            <th>Performance [GOPS]</th>
            <th>Efficiency [GOPS/W]</th>
            <th>Main Data Type</th>
            <th>Maturity</th>
            <th>Source</th>
        </tr>
    </thead>
    <tbody>
"""

def non_nan_or_dash(s):
    return s if not pd.isnan(s) else "-"
for i in range(len(df)):
    name = df.iloc[i][0].replace(" ", "&nbsp;")
    categ = df.iloc[i][11]
    tech = df.iloc[i][1]
    area = non_nan_or_dash(df.iloc[i][2].round(1))
    freq = non_nan_or_dash(df.iloc[i][3].round(1))
    volt = non_nan_or_dash(df.iloc[i][4].round(1))
    pow  = non_nan_or_dash(df.iloc[i][5].round(1))
    gops = non_nan_or_dash(df.iloc[i][6].round(1))
    eff  = non_nan_or_dash(df.iloc[i][7].round(1))
    dtype = df.iloc[i][9]
    maturity = df.iloc[i][10]
    doi = df.iloc[i][19]
    html_content += f"""
    <tr>
        <td><b><i>{symbols[i]}</i></b></td>
        <td>{name}</td>
        <td>{categ}</td>
        <td>{tech}</td>
        <td>{area}</td>
        <td>{pow}</td>
        <td>{gops}</td>
        <td>{eff}</td>
        <td>{dtype}</td>
        <td>{maturity}</td>
        <td><a href="https://doi.org/{doi}">{doi}</a></td>
    </tr>
    """

html_content += """
    </tbody>
</table>
"""

# Write the HTML content to a file
with open("plot_info.html", "w") as file:
    file.write(html_content)

# Generate plot and save
plt.text(1e1, 1.1, "100 GOPS/W", rotation=14)
plt.text(1e1, 1.1e1, "1 TOPS/W", rotation=14)
plt.text(1e1, 1.1e2, "10 TOPS/W", rotation=14)

x = np.asarray([df.iloc[i][5] for i in range(len(df))])
y = np.asarray([df.iloc[i][6] for i in range(len(df))])

adjust_text(anns.tolist(), x, y)
plt.subplots_adjust(bottom=0.2)
plt.savefig("plot.png", dpi=500)
