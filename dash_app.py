import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from loguru import logger
from app import get_all_filters
import pandas as pd

logger.info("Data loading")
df = pd.read_json("data/df.json")
logger.info("Data loaded")
logger.info("Filters creating")
all_filters = get_all_filters(df)
unique_filters = list(all_filters.property.value_counts().index)
logger.info("Filters created")

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [dcc.Input(id="applied_filters", multiple=True, value=None), dcc.Graph(id="fig")]
)


#  @app.callback(Output("fig", "figure"), Input("applied_filters", "value"))
@app.callback(Output("fig", "figure"), Input("applied_filters", "value"))
def update_figure(applied_filters):
    print(applied_filters)
    filtered_df = df.head(10)

    fig = px.scatter(
        filtered_df,
        x="averageweight",
        y="average",
        size="wishing",
        color="recommendations",
        hover_name="name",
        #  log_x=True,
        size_max=55,
    )

    fig.update_layout(transition_duration=500)

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
