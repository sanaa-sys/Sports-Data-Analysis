#The dataset attached is real historical match day attendance data (from the last few years).
##https://www.zerohanger.com/reasons-why-afl-is-popular-in-australia-and-beyond-124447/#:~:text=Sports%20come%20in%20a%20variety,under%20and%20from%20other%20countries. 

#The data set includes:
#Team
#Round
#Season
#Home/Away
#Final score
#Date
#Time
#Venue
#Attendance
#Opposition Team
#Win/loss (result)
#Ladder position at the end of that round
#Games won in last 5
import pandas as pd
import numpy as np
from dash import Dash, html
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import dash_core_components as dcc

df = pd.read_excel('Dataset - DA Internship project.xlsx')
# Display the first 5 rows
print("First 10 rows:")
print(df.head(10))

# Convert "Final Score" to numeric (assuming it's an integer)
df['Final Score'] = pd.to_numeric(df['Final Score'], errors='coerce')

# Convert "Actual Crowd" to numeric (assuming it's an integer)
df['Actual Crowd'] = pd.to_numeric(df['Actual Crowd'], errors='coerce')

# Convert "Ladder Position" to numeric (assuming it's an integer)
df['Ladder Position'] = pd.to_numeric(df['Ladder Position'], errors='coerce')

# Convert "Games Won in last 5 played" to numeric (assuming it's an integer)
df['Games Won in last 5 played'] = pd.to_numeric(df['Games Won in last 5 played'], errors='coerce')

# Display column details
print("\nColumn Details:")
df.info()

print("\nDescribe:")
print(df.describe())

#Missing values
print("\nTo see number of missing values of all rows")
print(df.isnull().sum())

rows_with_missing_values = df[df.isna().any(axis=1)]

# Display the rows with missing values
#there are 3113 missing values,  
print("\nTo see rows with missing values")
print(rows_with_missing_values)

#Remove values with missing date and venue, as date and venue are very important  attributes for a match 
df.dropna(subset=['Date', 'Venue'], inplace=True)
df = df[(df['Venue'] != 0) & (df['Date'] != 0)]
#See missing values for corresponding columns
print(df.isnull().sum())
#for games last played, ladder position and final score, replace with mean
df['Final Score'].fillna(df['Final Score'].mean(), inplace=True)
df['Ladder Position'].fillna(df['Ladder Position'].mean(), inplace=True)
df['Games Won in last 5 played'].fillna(df['Games Won in last 5 played'].mean(), inplace=True)


#By this stage data has been processed, lets start making visualizations.
print("\nDescribe:")
print(df.describe())
#Actual crowd: Min: 0, max: 100024
#Score: Min: 14, Max: 233

#Visualisation 1
vis1 = df.groupby(['Team'])['Actual Crowd'].mean().reset_index()

fig1 = px.bar(
    vis1,
    x='Team',
    y='Actual Crowd',
    title='Average Attendance by Team',
    template = 'plotly_dark'
)

# Customizations
fig1.update_xaxes(title='Team')  # X-axis label
fig1.update_yaxes(title='Average Attendance')  # Y-axis label

#Visualisation 2
vis2 = df.groupby(['Venue', 'Season'])['Actual Crowd'].mean().reset_index()

fig2 = px.bar(
    vis2,
    x='Venue',
    y='Actual Crowd',
    color='Season',
    title='Average Attendance by Venue and Season',
    template = 'plotly_dark'
)

# Customizations
fig2.update_xaxes(title='Venue')  # X-axis label
fig2.update_yaxes(title='Average Attendance')  # Y-axis label

#Visualisation 3
vis3 = df.groupby(['Time','Day'])['Actual Crowd'].mean().reset_index()



fig3 = px.scatter(
    df,
    x='Final Score',
    y='Actual Crowd',
    color='Round',
    title='Relationship Between Final Scores and Attendance in each round',
    animation_frame='Season',  # Specify the column to use for animation (sorting)
    animation_group='Round',  # Specify the column to use for grouping
    template = 'plotly_dark'
)

# Customizations
fig3.update_xaxes(title='Final Score')  # X-axis label
fig3.update_yaxes(title='Average Crowd')  # Y-axis label

# Show the plot
#fig1.show()

# Display the grouped data
#print(vis1)

load_figure_template("darkly")

app=Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
image_path = 'assets/download.jfif'

app.layout = dbc.Container([
    html.H1("Australian Footbal League statistics over the years", className="text-center", style = {'marginBottom':'60px', 'marginTop':'30px'}),
    dbc.Row(
           [dbc.Col(html.H5(
            children=(
              " For Australians, AFL is the real deal alongside cricket and rugby. It was founded in 1850 in Melbourne and is deeply rooted in Australian tradition. "
               " The rules for the game ensure maximum game time which makes it a high-octane game that is more exciting due to several adrenaline rush moments. The competitiveness of the sport has gotten better over the years and the pace with which it is played keeps everyone glued to the action."
               " There are currently 18 clubs spread across the mainland Australian states."
            ),
        ), style = {'marginLeft':'50px', 'marginBottom':'60px','textAlign': 'center'}),
           dbc.Col(html.Img(src=image_path), style = {'marginLeft':'50px', 'marginRight':'50px', 'textAlign': 'center'})
    ]), 
    dbc.Row(
       [
       dbc.Col(dcc.Graph(id = 'graph1', figure = fig1), width = 8, style = {'margin-left':'15px', 'margin-top':'7px', 'margin-right':'15px','marginBottom':'60px'}),
       dbc.Col(html.H5(
            children=(
             "This is a simple bar chart that shows attendance by each team. It can be seen that teams like Collingwood and Essendon have the most attendance."
            ),
        ),  width = 2, style = { 'textAlign': 'center', 'marginBottom':'60px'})
      ]),
      dbc.Row(
       [
       dbc.Col(dcc.Graph(id = 'graph2', figure = fig2), width = 8, style = {'margin-left':'15px', 'margin-top':'7px', 'margin-right':'15px', 'marginBottom':'60px'}),
       dbc.Col(html.H5(
            children=(
             "The stacked bar chart shows average attendance by each venue along with the season. It has two categorical values, venue and and one numerical variable which is actual crowd. "
             "The legend and hover are useful in drawing insights such as MCG is the most popular venue in all years."
            ),
        ),  width = 2, style = { 'textAlign': 'center', 'marginBottom':'60px'})
      ]),
   dbc.Row(
       [
       dbc.Col(dcc.Graph(id = 'graph3', figure = fig3), width = 8, style = {'margin-left':'15px', 'margin-top':'7px', 'margin-right':'15px', 'marginBottom':'60px'}),
       dbc.Col(html.H5(
            children=(
             "This scatter plot is the most interesting visualizations as it shows correlation between attendance and and final score in each round over the years. It can be seen that the Finals and the ending rounds drew more crowd in all years."
            ),
        ),  width = 2, style = { 'textAlign': 'center', 'marginBottom':'60px'})
      ]),

])



if __name__ == '__main__':
    app.run(debug=True)