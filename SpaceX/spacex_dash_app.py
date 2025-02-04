import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Завантаження даних
spacex_df = pd.read_csv("spacex_launch_dash.csv")
sites = spacex_df['Launch Site'].unique()

# Ініціалізація додатку Dash
app = dash.Dash(__name__)

# Макет додатку
app.layout = html.Div([
    html.H1("SpaceX Launch Dashboard", style={'textAlign': 'center'}),
    
    # Випадаюче меню для вибору майданчика
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'Усі майданчики', 'value': 'ALL'}
        ] + [{'label': site, 'value': site} for site in sites],
        value='ALL',
        placeholder="Оберіть майданчик для запуску тут",
        searchable=True
    ),
    
    # Кругова діаграма успішних запусків
    dcc.Graph(id='success-pie-chart'),
    
    # Повзунок діапазону корисного навантаження
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={i: str(i) for i in range(0, 10001, 2000)},
        value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()]
    ),
    
    # Діаграма розсіювання
    dcc.Graph(id='success-payload-scatter-chart')
])

# Зворотний виклик для кругової діаграми
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Успішні запуски за майданчиками')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, names='class', title=f'Успіхи запусків на {entered_site}')
    return fig

# Зворотний виклик для діаграми розсіювання
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'), Input('payload-slider', 'value')]
)
def update_scatter_chart(entered_site, payload_range):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    
    if entered_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
    
    fig = px.scatter(
        filtered_df, x='Payload Mass (kg)', y='class',
        color='Booster Version Category',
        title='Зв’язок між корисним навантаженням і успішністю запусків'
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
