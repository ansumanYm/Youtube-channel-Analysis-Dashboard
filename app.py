# Importing all modules.
from pydoc import classname
from turtle import width
import dash
from dash import dcc, html
from flask import Flask
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd



# Initiating the App
server = Flask(__name__)
app = dash.Dash(__name__, server = server, external_stylesheets = [dbc.themes.CYBORG, dbc.icons.BOOTSTRAP])


# Read the Files
comments_data = pd.read_csv('comments_data.csv')
video_detailsDF = pd.read_csv('video_detailsDF.csv')
df_cumsum = pd.read_csv('df_cumsum.csv')



### ------------------------------------Dash components--------------------------------------------


# Headers in Dashboard
Header_component = html.H2("DataScience YouTube Channel Analysis", style = {'color':'darkcyan'}, className = 'text-center')
histogram_header = html.H5("Comment Sentiment Polarity Distribution", style = {'color':'MediumAquamarine'}, className = 'text-center')
heatmap_header = html.H5("Density Heatmap between subjectivity and polarity of comment", style = {'color':'MediumAquamarine'}, className = 'text-center')
barplot_header = html.H5("Number of video uploaded on Different Days", style = {'color':'MediumAquamarine'}, className = 'text-center')
lineplot_header = html.H5("Views cumulative-sum per year", style = {'color':'MediumAquamarine'}, className = 'text-center')
scatterplot_header = html.H5("Best performing videos: Most viewed and Liked", style = {'color':'MediumAquamarine'}, className = 'text-center')



# Text in Dashboard
histogram_note = html.H6("Note: You can deselect channels by clicking on channel title.", style = {'color':'MediumAquamarine'}, className = 'text-left mt-3')
yrrange = html.H6("Select year:", style = {'color':'MediumAquamarine'}, className = 'text-left')
selectchannel_text = html.H6("Select channel:", style = {'color':'MediumAquamarine'}, className = 'text-left')



# Visual Components


comment_histogram = px.histogram(comments_data,  x = "polarity", color = 'channel_title',  barmode='overlay', template ='plotly_dark' 
                )




# Interactive components


channelselect_dropdown = dcc.Dropdown(id='channel-dpdn', multi=True, value=[ 'Data Professor', 'Luke Barousse'], 
                options=[{'label':x, 'value':x}
                for x in sorted(comments_data['channel_title'].unique())]
                
            )
channelselect_dropdown2 = dcc.Dropdown(id='channel-dpdn2', multi=True, value=[ 'Data Professor', 'Luke Barousse'], 
                options=[{'label':x, 'value':x}
                for x in sorted(video_detailsDF['channelTitle'].unique())]
                
            )
channelselect_dropdown3 = dcc.Dropdown(id='channel-dpdn3', multi=True, value=[ 'Data Professor', 'Luke Barousse'], 
                options=[{'label':x, 'value':x}
                for x in sorted(video_detailsDF['channelTitle'].unique())]
                
            )



min_year = video_detailsDF['year_published'].min() 
max_year = video_detailsDF['year_published'].max() 
year_range = dcc.RangeSlider(min_year, max_year, value=[min_year, max_year], step=None,
    marks={int(i):str(i) for i in list(video_detailsDF["year_published"].unique())}, id='year_range_slider')
year_range2 = dcc.RangeSlider(min_year, max_year, value=[min_year, max_year], step=None,
    marks={int(i):str(i) for i in list(video_detailsDF["year_published"].unique())}, id='year_range_slider2')
year_range3 = dcc.Slider(min_year, max_year, value=max_year, step=None,
    marks={int(i):str(i) for i in list(video_detailsDF["year_published"].unique())}, id='year_range_slider3')



# App Layout Design
app.layout = dbc.Container(
    [
        dbc.Row([
            Header_component
        ]),
        dbc.Row([
            dbc.Col([histogram_header, histogram_note, dcc.Graph(id="histogram", figure=comment_histogram)], width = {'size':6}),

            dbc.Col([heatmap_header, channelselect_dropdown, dcc.Graph(id="heatmap", figure={})], width = {'size':6})
        ], justify='around'),
        dbc.Row([
            dbc.Col([barplot_header, dcc.Graph(id="barplot", figure={}), yrrange, year_range3, selectchannel_text, channelselect_dropdown3], width = {'size':3}), 
            dbc.Col([lineplot_header, year_range, dcc.Graph(id="lineplot", figure={})], width = {'size':6}), 
            dbc.Col([scatterplot_header, dcc.Graph(id="scatterplot", figure={}), yrrange, year_range2, selectchannel_text, channelselect_dropdown2], width = {'size':3})
        ]),
        
    ], fluid=True
    
)



#------------------------------------------------ App callback--------------------------------------


@app.callback(
    Output('heatmap', 'figure'),
    Input('channel-dpdn', 'value')
)
def update_graph(channel_selected):
    heatmap_df = comments_data[comments_data['channel_title'].isin(channel_selected)]
    comment_heatmap = px.density_heatmap(heatmap_df, y = 'subjectivity', x = "polarity",  template ='plotly_dark' )
    return comment_heatmap


@app.callback(
    Output('lineplot', 'figure'),
    Input('year_range_slider', 'value')
)
def update_graph(year_range):
    lineplot_df = df_cumsum[(df_cumsum['year_published'] >= year_range[0]) & (df_cumsum['year_published'] <= year_range[1])]
    lineplot = px.line(lineplot_df, x='published_date', y="viewcount_cumsum", height=350, color='channelTitle',  line_shape= 'linear',
             labels = dict(published_date = "per year", viewcount_cumsum = "Video views cumulative sum"), template ='plotly_dark'
             )
    lineplot.update_layout(
        margin=dict( b=20, t=40))
    return lineplot


@app.callback(
    Output('scatterplot', 'figure'),
    [Input('year_range_slider2', 'value'),
    Input('channel-dpdn2', 'value')
    ]
)
def update_graph(year_range, channel_selected):
    scatter_df1 = video_detailsDF[(video_detailsDF['year_published'] >= year_range[0]) & (video_detailsDF['year_published'] <= year_range[1])]
    scatter_df = scatter_df1[scatter_df1['channelTitle'].isin(channel_selected)]
    
    scatterplot = px.scatter(scatter_df, y = 'viewCount', x = "likeCount", height = 300,  hover_name= 'title',
                    labels = dict(viewCount = "Views per video", commentCount = "Likes per video"), template ='plotly_dark'
                    )
    scatterplot.update_layout(
    margin=dict( r=10, t=50, b = 10))

    return scatterplot


@app.callback(
    Output('barplot', 'figure'),
    [Input('year_range_slider3', 'value'),
    Input('channel-dpdn3', 'value')
    ]
)
def update_graph(year, channel_selected):
    bar1 = video_detailsDF[video_detailsDF['year_published'] == year]
    bar_df = bar1[bar1['channelTitle'].isin(channel_selected)]
    barplot = px.histogram(bar_df, x = "dayofweek", height = 300, template ='plotly_dark',
                    labels=dict(dayofweek = 'Days of Week')
                    )
    barplot.update_layout(
        margin=dict( r=10, t=50))

    return barplot


# Run the App
if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0", port=8080)
