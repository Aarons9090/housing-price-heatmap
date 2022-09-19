import pandas as pd
import plotly.express as px

df = pd.read_csv("houses.csv")

fig = px.density_mapbox(df, lat="lat", lon="lon", z="price", mapbox_style="stamen-terrain", opacity=0.7,
                        color_continuous_scale=[[0, 'green'], [0.3, 'green'], [0.9, 'yellow'], [1.0, 'red']],
                        range_color=[100000,400000]
                        )

fig.show()
