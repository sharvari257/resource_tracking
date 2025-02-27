import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import mysql.connector
import pandas as pd
import plotly.express as px

# Database connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='pass123',
    auth_plugin='mysql_native_password'
)

# Create a cursor object for SQL queries
cur = conn.cursor()
cur.execute("USE python_db;")

# Fetch data from the database
def fetch_data():
    cur.execute("SELECT col_dateTime, min_usage, max_usage, avg_usage FROM usage_tbl;")
    rows = cur.fetchall()
    df = pd.DataFrame(rows, columns=['DateTime', 'Min Usage', 'Max Usage', 'Avg Usage'])
    df['DateTime'] = pd.to_datetime(df['DateTime'])  # Convert to datetime
    return df

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("CPU Usage Dashboard"),
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=pd.to_datetime('2024-12-01'),
        end_date=pd.to_datetime('today'),
        display_format='YYYY-MM-DD'
    ),
    dcc.Dropdown(
        id='usage-type-dropdown',
        options=[
            {'label': 'Min Usage', 'value': 'Min Usage'},
            {'label': 'Max Usage', 'value': 'Max Usage'},
            {'label': 'Avg Usage', 'value': 'Avg Usage'}
        ],
        value='Avg Usage'  # Default value
    ),
    dcc.Graph(id='usage-graph')
])

# Callback to update the graph based on user input
@app.callback(
    Output('usage-graph', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('usage-type-dropdown', 'value')]
)
def update_graph(start_date, end_date, usage_type):
    df = fetch_data()
    filtered_df = df[(df['DateTime'] >= start_date) & (df['DateTime'] <= end_date)]
    
    fig = px.line(filtered_df, x='DateTime', y=usage_type, title=f'{usage_type} Over Time')
    fig.update_layout(xaxis_title='Date Time', yaxis_title=usage_type)
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

# Close the cursor and connection when done
cur.close()
conn.close()