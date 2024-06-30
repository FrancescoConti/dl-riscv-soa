import numpy as np
import pandas as pd
import plotly.express as px

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

# Create the interactive plot
fig = px.scatter(dfclean, 
                 x=dfclean.columns[5], 
                 y=dfclean.columns[6], 
                 hover_name=dfclean.columns[1], 
                 log_x=True, 
                 log_y=True,
                 title="Interactive Data Plot")

# Save the interactive plot as an HTML file
fig.write_html('plot.html')

# Also save the dataframe as an HTML table
dfclean.to_html('table.html', index=False)
