import dash_mantine_components as dmc
from dash import get_asset_url

component = dmc.Image(
    radius="md",
    src=get_asset_url("images/mc-label3-head.jpg"),
)