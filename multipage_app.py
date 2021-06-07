#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from iso3166 import countries

import plotly.express as px
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import dash
import dash_bootstrap_components as dbc


# In[111]:


# Load Data
data = pd.read_excel("data/transcripts.xlsx", index_col=0)
data = data[data.country != '.DS']
weights=pd.read_excel("data/lda_df_weights_update.xlsx", index_col=0)
df_merged = weights


# In[112]:


intro_words = "\t"
with open('intro.txt') as this_file:
    for a in this_file.read():
        if "\n" in a:
            intro_words += "\n \t"
        else:
            intro_words += a

method_words = "\t"
with open('methods.txt') as this_file:
    for a in this_file.read():
        if "\n" in a:
            method_words += "\n \t"
        else:
            method_words += a


# In[113]:


# year = np.array(data["year"].unique())
drop_values = data.country.unique()
topic_list={"International Diplomacy":"Topic 1","War and Power":"Topic 2","Conflict in Africa":"Topic 3","Middle Eastern Terrorism":"Topic 4","Climate Change":"Topic 5","Communism":"Topic 6"}

topics = pd.read_excel("data/topic_trend.xlsx", index_col=0)
topic_values = topics.Topic.unique()


# In[117]:



# Build App
app = JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])



# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Navigate", className="display-4"),
        html.Hr(),
        html.P(
            "bla bla", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Introduction", href="/", active="exact"),
                dbc.NavLink("Naive Counter", href="/page-1", active="exact"),
                dbc.NavLink("General Results", href="/page-2", active="exact"),
                dbc.NavLink("Country Specific Results", href="/page-3", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return [
            html.H1('Modern Data Analytics Project:'),
            html.H2('Politicians and Climate Change'),
            html.Br(),
            html.Div(dcc.Markdown(intro_words)),
            html.Div('{} countries are represented in these speeches.'.format(len(data['country'].unique()))),
            html.Br(),
            html.H3('Methdology'),
            html.Div(dcc.Markdown(method_words)),
            html.Img(src=app.get_asset_url('word_cloud_LDA.png'))
        ]
    elif pathname == "/page-1":
        return [
            
            html.H1("Naive Counter"),
            html.Div("A very basic way to investigate the content of these speeches is by searching for a specific term."),
            html.Div("This of course ignores any contextual differences in meaning the word might have."),
            html.Br(),
            html.Strong("Search: "),
            dcc.Input(id='term_select', type='text', debounce=True, value='people', required=True),
            html.Br(),
            html.Br(),
            html.Div(id='naive_text', children=[]), #, style={'color': 'blue', 'fontSize': 14}
            dcc.Graph(id="naive_graph", figure={})
            
            
            
        ]
    elif pathname == "/page-2":
        return [
    
            html.H1('Overall trends'),
            html.Div("Please select any topics you wish to explore."),
            
            dcc.Dropdown(
                id='general_dropdown',
                options=[
                    {'label': i, 'value': i} for i in topic_values
                    ],
                multi=True,
                value=['Topic 1']
                ),
            
             dcc.Graph(id='general_graph', figure={})
        ]
    elif pathname == "/page-3":
        return [

            dcc.Dropdown(
                id='country_dropdown',
                options=[
                    {'label': i, 'value': i} for i in drop_values
                    ],
                value = 'ALB',
                placeholder='Select a country'
                ),
            
             dcc.Dropdown(
                id='topic_dropdown',
                options=[
                    {'label': i, 'value': i} for i in topic_list.keys()
                    ],
                value = 'ALB'
                ),
            
            dcc.Graph(id='country_graph', figure={})   
            
        ]
    
######################################################################################
################################### Naive Counter ####################################
######################################################################################

@app.callback(
    Output(component_id='naive_text', component_property='children'),
    Output(component_id='naive_graph', component_property='figure'),
    Input('term_select', 'value'))

def update_graph(term_select):
    
    dffff = data
  
    
    # loop-de-loop that does the counting
    term = term_select.lower()
    count = np.empty(0)
    
    for i in data_filtered.index:
        count = np.append(count, word_tokenize(dffff["transcript"][i].lower()).count(term))
    
    scatter = px.scatter(dffff, x=year, y=count, trendline="lowess",
                        trendline_color_override="red")
    scatter.update_layout(
        yaxis = dict(
        showgrid = True,
        zeroline = True,
        showline = True,
        gridcolor = 'lightgrey'),
        xaxis_title="",
        yaxis_title='Mentions',
        plot_bgcolor="#fff")
    
#     container = 'Number of times "{}" was mentioned in a given year'.format(term_select)
    container = html.P(children=[
        html.Span('Number of times '),
        html.Strong(term_select),
        html.Span(' was mentioned in a given year')
    ])
    
    return container, scatter


######################################################################################
#################################### General Page ####################################
######################################################################################

@app.callback(
    Output(component_id='general_graph', component_property='figure'),
    [dash.dependencies.Input('general_dropdown', 'value')])

def update_output(value):
    dff = topics
    data_filtered = dff[dff.Topic.isin(value)]
    
    fig = px.line(data_filtered, x="year", y="prevalence", color='Topic').update_layout(
    yaxis = dict(
    showgrid = True,
    zeroline = True,
    showline = True,
    gridcolor = 'lightgrey'),
    xaxis_title="",
    yaxis_title='Prevalence',
    plot_bgcolor="#fff")
    
    return fig


######################################################################################
#################################### Country Page ####################################
######################################################################################

@app.callback(
    Output(component_id='country_graph', component_property='figure'),
    Input('country_dropdown', 'value'),
    Input('topic_dropdown', 'value'))

def update_output_div(country_dropdown, topic_dropdown):
    
    dfff = df_merged
    data_filtered = dfff.loc[dfff['country'] == country_dropdown]
    year = np.array(data_filtered["year"].unique())
    weights=np.array(data_filtered[topic_list[topic_dropdown]])

    scatter = px.scatter(x=year, y=weights, trendline="lowess",
                        trendline_color_override="red")
    scatter.update_xaxes(range=[min(df_merged["year"]),max(df_merged["year"])])
    scatter.update_layout(
    yaxis = dict(
    showgrid = True,
    zeroline = True,
    showline = True,
    gridcolor = 'lightgrey'),
    xaxis_title="",
    yaxis_title='Prevalence',
    plot_bgcolor="#fff")
    
       
    return scatter
        




# Run app and display result inline in the notebook
app.run_server(mode='jupyterlab', debug=False,dev_tools_ui=False,dev_tools_props_check=False)


# In[17]:


dfff = df_merged
dfff.head(2)


# In[19]:


data_filtered = dfff.loc[dfff['country'] == "ALB"]


# In[25]:


year = np.array(data_filtered["year"].unique())
len(year)


# In[24]:


weights=np.array(data_filtered[topic_list['International Diplomacy']])
len(weights)


# In[ ]:


#             html.Iframe(src=app.get_asset_url("lda.html"),
#                                             style=dict(position="center", left="0", top="0", width="1210px", height='780px', transform= "scale(0.8)"))


# In[ ]:


# If the user tries to reach a different page, return a 404 message
return dbc.Jumbotron(
    [
        html.H1("404: Not found", className="text-danger"),
        html.Hr(),
        html.P(f"The pathname {pathname} was not recognised..."),
    ]
)

