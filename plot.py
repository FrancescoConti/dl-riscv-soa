import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from adjustText import adjust_text
import matplotlib
import itertools
import string

def create_table(dataframe):

    # Clean the data
    dataframe = dataframe.replace("-", "NaN")
    dataframe.columns = dataframe.columns.astype(str)
    dataframe[dataframe.columns[5]] = dataframe[dataframe.columns[5]].apply(pd.to_numeric, errors='coerce')
    dataframe[dataframe.columns[6]] = dataframe[dataframe.columns[6]].apply(pd.to_numeric, errors='coerce')
    dataframe[dataframe.columns[7]] = dataframe[dataframe.columns[7]].apply(pd.to_numeric, errors='coerce')
    dataframe[dataframe.columns[7]] = dataframe[dataframe.columns[6]] / dataframe[dataframe.columns[5]] * 1000

    # Drop NaN values
    dfclean = dataframe.dropna(subset=[dataframe.columns[5], dataframe.columns[6]])

    # round efficiency to 3 significant digits
    Nsig = 3
    import math
    dfclean[dataframe.columns[7]] = dfclean[dataframe.columns[7]].apply(lambda x: x if pd.isna(x) else round(x, Nsig-int(math.floor(math.log10(abs(x))))))

    # Add labels to the markers
    df = dfclean.sort_values(by=dfclean.columns[5])

    # Create HTML table content
    html_content = """
    <table id="data-table" class="display" style="width:100%">
        <thead>
            <tr>
                <th>Name</th>
                <th>Architecture</th>
                <th>Tech.</th>
                <th>Area [mm2]</th>
                <th>Power [mW]</th>
                <th>Perf. [GOPS]</th>
                <th>Eff. [GOPS/W]</th>
                <th>Data Type</th>
                <th>IMC</th>
                <th>Maturity</th>
                <th>Source</th>
            </tr>
        </thead>
        <tbody>
    """

    def non_nan_or_dash(s):
        return s if s != "NaN" and s != "nan" else "-"
    def yes_or_no(s):
        return "yes" if s == "x" else "no"

    for i in range(len(df)):
        name = df.iloc[i][0].replace(" ", "&nbsp;")
        categ = df.iloc[i][11]
        tech = df.iloc[i][1]
        area = non_nan_or_dash(df.iloc[i][2])
        freq = non_nan_or_dash(df.iloc[i][3])
        volt = non_nan_or_dash(df.iloc[i][4])
        pow  = non_nan_or_dash(df.iloc[i][5])
        gops = non_nan_or_dash(df.iloc[i][6])
        eff  = non_nan_or_dash(df.iloc[i][7])
        # arch = non_nan_or_dash(df.iloc[i][11])
        imc  = yes_or_no(df.iloc[i][17])
        dtype = df.iloc[i][9]
        maturity = df.iloc[i][10]
        doi = df.iloc[i][19]
        html_content += f"""
        <tr>
            <td>{name}</td>
            <td>{categ}</td>
            <td>{tech}</td>
            <td>{area}</td>
            <td>{pow}</td>
            <td>{gops}</td>
            <td>{eff}</td>
            <td>{dtype}</td>
            <td>{imc}</td>
            <td>{maturity}</td>
            <td><a href="https://doi.org/{doi}">{doi}</a></td>
        </tr>
        """

    html_content += """
        </tbody>
    </table>
    """

    # Write the HTML content to a file
    with open("table.html", "w") as file:
        file.write(html_content)

def plot_plotly(dataframe):

    # Clean the data
    dataframe = dataframe.replace("-", "NaN")
    dataframe.columns = dataframe.columns.astype(str)
    dataframe[dataframe.columns[5]] = dataframe[dataframe.columns[5]].apply(pd.to_numeric, errors='coerce')
    dataframe[dataframe.columns[6]] = dataframe[dataframe.columns[6]].apply(pd.to_numeric, errors='coerce')
    dataframe[dataframe.columns[7]] = dataframe[dataframe.columns[7]].apply(pd.to_numeric, errors='coerce')
    dataframe[dataframe.columns[7]] = dataframe[dataframe.columns[6]] / dataframe[dataframe.columns[5]] * 1000

    # Drop NaN values
    dfclean = dataframe.dropna(subset=[dataframe.columns[5], dataframe.columns[6]])

    # Define custom marker styles
    style = ["FP64", "FP32", "FP16", "FP8", "FP4", "INT32", "INT8", "INT4", "INT2 x INT8", "INT2 x INT4", "INT2", "Analog"]
    symbol_map = {s: i for i, s in enumerate(style)}
    color_map = {"silicon": "red", "pre-silicon": "green", "simulation": "blue"}

    # Create the interactive plot
    fig = px.scatter(
        dfclean, 
        x=dfclean.columns[5], 
        y=dfclean.columns[6], 
        hover_name=dfclean.columns[0], 
        log_x=True, 
        log_y=True,
        title="Interactive Data Plot",
        color=dfclean.columns[10],  # Assuming this column represents maturity
        symbol=dfclean.columns[9],  # Assuming this column represents the style labels
        category_orders={
            dfclean.columns[10]: ["silicon", "pre-silicon", "simulation"],  # Order of color categories
            dfclean.columns[9]: style  # Order of symbol categories
        },
        color_discrete_sequence=[
            "orangered", "lime", "blue"],
        symbol_sequence=list(symbol_map.values())
    )

    # Add the dashed lines
    fig.add_trace(go.Scatter(
        x=[1, 1e5], 
        y=[1e-1, 1e4], 
        mode="lines", 
        line=dict(dash="dash", color="black", width=0.7),
        showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=[1, 1e5], 
        y=[1, 1e5], 
        mode="lines", 
        line=dict(dash="dash", color="black", width=0.7),
        showlegend=False
    ))
    fig.add_trace(go.Scatter(
        x=[1, 1e5], 
        y=[1e1, 1e6], 
        mode="lines", 
        line=dict(dash="dash", color="black", width=0.7),
        showlegend=False
    ))

    # Add text annotations for the dashed lines
    fig.add_annotation(x=np.log10(1e1), y=np.log10(1.1), text="100 GOPS/W", showarrow=False, yshift=10, xshift=-20, font=dict(size=10, color="black"))
    fig.add_annotation(x=np.log10(1e1), y=np.log10(1.1e1), text="1 TOPS/W", showarrow=False, yshift=10, xshift=-20, font=dict(size=10, color="black"))
    fig.add_annotation(x=np.log10(1e1), y=np.log10(1.1e2), text="10 TOPS/W", showarrow=False, yshift=10, xshift=-20, font=dict(size=10, color="black"))

    # Update layout for minor ticks, gridlines, and background
    fig.update_layout(
        xaxis=dict(
            minor=dict(ticklen=4, showgrid=True, gridwidth=0.5, gridcolor='lightgrey'),
            # range=[1, 5]
        ),
        yaxis=dict(
            minor=dict(ticklen=4, showgrid=True, gridwidth=0.5, gridcolor='lightgrey'),
            # range=[0, 6]
        ),
        xaxis_type="log",
        yaxis_type="log",
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black')
    )
    fig.update_traces(
        marker=dict(size=10,
        line=dict(width=2,
                color='DarkSlateGrey')),
                selector=dict(mode='markers'))
    # Save the interactive plot as an HTML file
    fig.write_html('plot.html')

def plot_matplotlib(dataframe):
    matplotlib.rcParams.update({
        'font.family':  'sans-serif',
        'font.sans-serif':['Helvetica']
    })

    dataframe = dataframe.replace("-", "NaN")
    dataframe.columns = dataframe.columns.astype(str)
    dataframe[dataframe.columns[5]] = dataframe[dataframe.columns[5]].apply(pd.to_numeric, errors='coerce')
    dataframe[dataframe.columns[6]] = dataframe[dataframe.columns[6]].apply(pd.to_numeric, errors='coerce')
    dataframe[dataframe.columns[7]] = dataframe[dataframe.columns[7]].apply(pd.to_numeric, errors='coerce')
    dataframe[dataframe.columns[7]] = (dataframe[dataframe.columns[6]]/dataframe[dataframe.columns[5]]*1000)

    # round efficiency to 3 significant digits
    Nsig = 3
    import math
    dataframe[dataframe.columns[7]] = dataframe[dataframe.columns[7]].apply(lambda x: x if pd.isna(x) else round(x, Nsig-int(math.floor(math.log10(abs(x))))))

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

    # Generate plot and save
    plt.text(1e1, 1.1, "100 GOPS/W", rotation=14)
    plt.text(1e1, 1.1e1, "1 TOPS/W", rotation=14)
    plt.text(1e1, 1.1e2, "10 TOPS/W", rotation=14)

    x = np.asarray([df.iloc[i][5] for i in range(len(df))])
    y = np.asarray([df.iloc[i][6] for i in range(len(df))])

    adjust_text(anns.tolist(), x, y)
    plt.subplots_adjust(bottom=0.2)
    plt.savefig("plot.png", dpi=500)


# Read the Excel file
dataframe = pd.read_excel('data.xlsx')
plot_plotly(dataframe)
plot_matplotlib(dataframe)
create_table(dataframe)
