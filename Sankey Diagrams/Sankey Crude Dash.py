import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

data = pd.read_csv('C:\Temp\Projects\AA-CrudeCostingAdjustment\Bob\Data Cleaned.csv')
df = data[data['Price Type'].isin(['laid in price'])].drop('Price Type', axis=1)

df = df[['ABBRV', 'API Gravity', 'Sulfur',
       'Purchase Region']].drop_duplicates(subset='ABBRV').dropna()


df1 = df.copy()
df1['Crudes'] = 'Crudes'

df2 = df1.groupby(['Crudes','Purchase Region'], as_index=False).size().reset_index()
df3 = df1.groupby(['Purchase Region','Sulfur'], as_index=False).size().reset_index()
df4 = df1.groupby(['Sulfur','API Gravity'], as_index=False).size().reset_index()

df2.columns = ['a', 'b', 'Quantity']
df3.columns = ['a', 'b', 'Quantity']
df4.columns = ['a', 'b', 'Quantity']
df5 = df2.append(df3)
df6 = df5.append(df4)

app = dash.Dash(__name__)

def genSankey(df,cat_cols=[],value_cols='',title='Sankey Diagram'):
  # maximum of 6 value cols -> 6 colors
  colorPalette = ['#FFD43B','#646464','#4B8BBE','#306998','#306998','#306998','#306998','#306998','#306998','#306998','#306998','#306998','#306998','#306998']
  labelList = []
  colorNumList = []
  for catCol in cat_cols:
      labelListTemp =  list(set(df[catCol].values))
      colorNumList.append(len(labelListTemp))
      labelList = labelList + labelListTemp
      
  # remove duplicates from labelList
  labelList = list(dict.fromkeys(labelList))
  
  # define colors based on number of levels
  colorList = []
  for idx, colorNum in enumerate(colorNumList):
      colorList = colorList + [colorPalette[idx]]*colorNum
      
  # transform df into a source-target pair
  for i in range(len(cat_cols)-1):
      if i==0:
          sourceTargetDf = df[[cat_cols[i],cat_cols[i+1],value_cols]]
          sourceTargetDf.columns = ['source','target','count']
      else:
          tempDf = df[[cat_cols[i],cat_cols[i+1],value_cols]]
          tempDf.columns = ['source','target','count']
          sourceTargetDf = pd.concat([sourceTargetDf,tempDf])
      sourceTargetDf = sourceTargetDf.groupby(['source','target']).agg({'count':'sum'}).reset_index()
      
  # add index for source-target pair
  sourceTargetDf['sourceID'] = sourceTargetDf['source'].apply(lambda x: labelList.index(x))
  sourceTargetDf['targetID'] = sourceTargetDf['target'].apply(lambda x: labelList.index(x))
  
  # creating the sankey diagram
  fig = go.Figure(data=[go.Sankey(
      node = dict(
          pad = 15,
          thickness = 20,
          line = dict(color = "black", width = 0.5),
          label = labelList,
          color = colorList
      ),
      link = dict(
            source = sourceTargetDf['sourceID'],
            target = sourceTargetDf['targetID'],
            value = sourceTargetDf['count']
      )
  )])

  return fig

app.layout = html.Div([
    dcc.Graph(id="graph", 
              figure = genSankey(df=df6,cat_cols=['a','b'],value_cols='Quantity',title='Sankey Diagram x Profit')
              )
])




app.run_server(use_reloader=False)
