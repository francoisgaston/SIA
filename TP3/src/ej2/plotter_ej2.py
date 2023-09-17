import plotly.express as px
import plotly.graph_objects as go
import sys
import pandas as pd
import numpy as np


if __name__ == "__main__":
    with open(f"{sys.argv[1]}", "r") as data_file:
        CSV = pd.read_csv(data_file)
        px.data.iris()
        fig = px.scatter_3d(CSV,x='x1',y='x2',z='x3',color='y')
        w0 = 19.3
        w1 = 2.479
        w2 = -6.2
        w3 = 15.07
        x1v = np.linspace(CSV['x1'].min(), CSV['x1'].max(), 100)
        x2v = np.linspace(CSV['x2'].min(), CSV['x2'].max(), 100)
        x, y = np.meshgrid(x1v, x2v)
        z = (-(x/w1)-(y/w2) - w0)/w3
        fig.add_trace(go.Surface(x=tuple(z),y=tuple(y),z=tuple(z)))
        fig.show()
