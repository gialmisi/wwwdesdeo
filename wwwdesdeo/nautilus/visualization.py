"""Function to create visual and interactive web elements.
"""
import plotly
import re


def bars_graph(values, mode="relative"):
    solution_nums = list(range(1, len(values)+1))
    objective_values = list(map(list, zip(*values)))

    data = []
    for (ind, val) in enumerate(objective_values):
        data.append({
            "x": solution_nums,
            "y": val,
            "name": "Objective {}".format(ind+1),
            "type": "bar",
            })

    layout = {
        'xaxis': {'title': 'Solutions', 'tick0': 1, 'dtick': 1},
        'yaxis': {'title': 'Objective values'},
        'barmode': mode,
        'title': 'Relative Barmode'
    }

    html_div = plotly.offline.plot({'data': data, 'layout': layout},
                                   output_type='div',
                                   include_plotlyjs=False)
    div_id = re.search("<div id=\"(.+?)\"", html_div).group(1)
    # html_div = .sub(div_id, "myid", res)

    return html_div, div_id
