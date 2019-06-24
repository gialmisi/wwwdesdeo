"""Function to create visual and interactive web elements.
"""
import plotly
import plotly.graph_objs as go
import re


def parallel_axes(values, bounds):
    print(values)
    columns = list(map(list, zip(*values)))
    boundsc = list(map(list, zip(*bounds)))

    parcoords = go.Parcoords()

    # Set the line
    line = {"color": "blue"}

    dimensions = []
    # Set the data
    for (index, coord_vals) in enumerate(columns):
        dimensions.append({
            "range": [min(coord_vals), max(coord_vals)],
            "label": str(index),
            "values": coord_vals,
            })

    parcoords = [go.Parcoords(line=line, dimensions=dimensions)]
    html_div = plotly.offline.plot(parcoords,
                                   include_plotlyjs=False,
                                   output_type="div")
    div_id = re.search("<div id=\"(.+?)\"", html_div).group(1)

    return html_div, div_id


def visual():
    data = [
        go.Parcoords(
            line=dict(color='blue'),
            dimensions=list([
                dict(range=[1, 5],
                     constraintrange=[1, 2],
                     label='A', values=[1, 4]),
                dict(range=[1.5, 5],
                     tickvals=[1.5, 3, 4.5],
                     label='B', values=[3, 1.5]),
                dict(range=[1, 5],
                     tickvals=[1, 2, 4, 5],
                     label='C', values=[2, 4],
                     ticktext=['text 1', 'text 2', 'text 3', 'text 4']),
                dict(range=[1, 5],
                     label='D', values=[4, 2])
            ]),
        )
    ]

    res = plotly.offline.plot(data, include_plotlyjs=False, output_type='div')
    return res
