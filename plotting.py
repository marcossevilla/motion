import pandas
from motion import df
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool

plot = figure(x_axis_type="datetime", height=100, width=500, sizing_mode="stretch_both", title="Motion Graph")

hover = HoverTool(tooltips=[("Start", "@Start"), ("End", "@End")])
plot.add_tools(hover)

quadrant = plot.quad(left=df["Start"], right=df["End"], top=1, bottom=0, color="green")

output_file("graph.html")
show(plot)