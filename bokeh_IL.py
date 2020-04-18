from bokeh.io import output_file, show
from bokeh.plotting import figure

from bokeh.models import LogColorMapper
from bokeh.palettes import Viridis6 as palette
from bokeh.sampledata.unemployment import data as unemployment
from bokeh.sampledata.us_counties import data as counties

palette = tuple(reversed(palette))

counties = {
    code: county for code, county in counties.items() if county["state"] == "il"
}

county_xs = [county["lons"] for county in counties.values()]
county_ys = [county["lats"] for county in counties.values()]

county_names = [county['name'] for county in counties.values()]
county_rates = [unemployment[county_id] for county_id in counties]
color_mapper = LogColorMapper(palette=palette)

data = dict(
    x=county_xs,
    y=county_ys,
    name=county_names,
    rate=county_rates,
)

TOOLS = "pan,wheel_zoom,reset,hover,save"  # other tools - box_zoom

p = figure(
    title="Illinois Unemployment, 2009", tools=TOOLS,
    x_axis_location=None, y_axis_location=None,
    plot_width=400  # Adjust pixel widgth
tooltips = [
    ("Name", "@name"), ("Unemployment rate", "@rate%"), ("(Long, Lat)", "($x, $y)")
])

p.grid.grid_line_color = None
p.hover.point_policy = "follow_mouse"

p.patches('x', 'y', source=data,
          fill_color={'field': 'rate', 'transform': color_mapper},
          fill_alpha=0.7, line_color="white", line_width=0.5)

show(p)

## Helpful lines of code:
p = figure(x_axis_type="datetime", x_axis_label='Date', y_axis_label='US Dollars')
from bokeh.models import ColumnDataSource

src_data = ColumnDataSource(dataframehere)

from bokeh.models import HoverTool

hover = HoverTool(tooltips=None, mode='hline')
plot = figure(tools=[hover, 'crosshair'])
