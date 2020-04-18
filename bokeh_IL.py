import json
import geopandas as gpd

from pathlib import Path

from bokeh.io import output_file, show

from bokeh.models import (CDSView, ColorBar, ColumnDataSource,
                          CustomJS, CustomJSFilter,
                          GeoJSONDataSource, HoverTool,
                          LinearColorMapper, LogColorMapper, Slider)
from bokeh.layouts import column, row, widgetbox
from bokeh.palettes import brewer, Viridis6
from bokeh.plotting import figure

from gspread_pandas import Spread, Client
from oauth2client.service_account import ServiceAccountCredentials

script_folder = Path("C:/Users/farha/Google Drive/XS/Git/NicksNewsUpdater/")
creds_path = "C:/Users/farha/Desktop/ExProc-Creds.json"
geo_folder = Path(script_folder / "geo_data")
backup_folder = Path(script_folder / "backup")
idph_csv_folder = Path(script_folder / "idph_csv")

# Data Links
gsheet_zip_link = "https://docs.google.com/spreadsheets/d/11P36C4z4B2vIXSfgchfAwWfLRnUD0zqg0Ki-MWCiC58/edit#gid=0"
gsheet_county_link = "https://docs.google.com/spreadsheets/d/1sbLLUOqEv_s2eOh3iQyWRw7JOB8rixfu1oBXgPy8zP8/edit#gid=0"
gsheet_totals_link = "https://docs.google.com/spreadsheets/d/1MWNebArAjjTTtJdxQcnUakShSbADhccx3xw28L2Nflo/edit#gid=0"
idph_stats_zip_wksht_key = "11P36C4z4B2vIXSfgchfAwWfLRnUD0zqg0Ki-MWCiC58"
idph_stats_county_wksht_key = "1sbLLUOqEv_s2eOh3iQyWRw7JOB8rixfu1oBXgPy8zP8"
idph_stats_totals_wksht_key = "1MWNebArAjjTTtJdxQcnUakShSbADhccx3xw28L2Nflo"

# Shape Files acquired from : https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html
# Read in shapefile
geo_data = gpd.read_file(geo_folder / 'cb_2018_us_county_500k.shp')
geo_data_il = geo_data.loc[geo_data.STATEFP == "17"]

# Input GeoJSON source that contains features for plotting
geosource = GeoJSONDataSource(geojson=geo_data_il.to_json())

# Create figure object.
p = figure(title='Lead Levels in Water Samples, 2018',
           plot_height=1100,
           plot_width=600,
           toolbar_location='below',
           tools="pan, wheel_zoom, box_zoom, reset")
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
# Add patch renderer to figure.
states = p.patches('xs', 'ys', source=geosource,
                   fill_color=None,
                   line_color='gray',
                   line_width=0.25,
                   fill_alpha=1)
# Create hover tool
p.add_tools(HoverTool(renderers=[states],
                      tooltips=[('County', '@NAME'),
                                ('Population', '@POPESTIMATE2018')]))
show(p)

# %%

palette = tuple(reversed(palette))

counties = {
    code: county for code, county in geo_data_il.items()
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

# %%
## Helpful lines of code:
p = figure(x_axis_type="datetime", x_axis_label='Date', y_axis_label='US Dollars')
from bokeh.models import ColumnDataSource

src_data = ColumnDataSource(dataframehere)

from bokeh.models import HoverTool

hover = HoverTool(tooltips=None, mode='hline')
plot = figure(tools=[hover, 'crosshair'])
