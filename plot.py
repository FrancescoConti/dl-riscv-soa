import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Read the Excel file
dataframe = pd.read_excel('data.xlsx')

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
    color_discrete_map=color_map,
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
fig.add_annotation(x=1e1, y=1.1, text="100 GOPS/W", showarrow=False, yshift=10, xshift=-20, font=dict(size=10, color="black"))
fig.add_annotation(x=1e1, y=1.1e1, text="1 TOPS/W", showarrow=False, yshift=10, xshift=-20, font=dict(size=10, color="black"))
fig.add_annotation(x=1e1, y=1.1e2, text="10 TOPS/W", showarrow=False, yshift=10, xshift=-20, font=dict(size=10, color="black"))

# Generate alphabetic symbols for annotations
def generate_alphabetic_symbols(n):
    import itertools, string
    letters = string.ascii_lowercase + string.ascii_uppercase
    result = []
    length = 1
    while len(result) < n:
        for combo in itertools.product(letters, repeat=length):
            result.append(''.join(combo))
            if len(result) == n:
                return result
        length += 1
    return result

symbols = generate_alphabetic_symbols(len(dfclean))

# Add annotations to the markers
for i, row in dfclean.iterrows():
    symbol = symbols[i]
    fig.add_annotation(
        x=row[dfclean.columns[5]],
        y=row[dfclean.columns[6]],
        text=f"<b>{symbol}</b>",
        showarrow=False,
        yshift=10
    )

# Save the interactive plot as an HTML file
fig.write_html('plot.html')

# Also save the dataframe as an HTML table
dfclean.to_html('table.html', index=False)
