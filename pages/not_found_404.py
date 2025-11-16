import dash_mantine_components as dmc
from dash import html, register_page, dcc

from lib.constants import PAGE_TITLE_PREFIX

register_page(
    __name__,
    "/404",
    title=PAGE_TITLE_PREFIX + "404 - Page Not Found",
)

layout = html.Div(
    id="not-found-container",
    children=[
        dmc.Stack(
            align="center",
            justify="center",
            gap="lg",
            style={
                "height": "calc(100vh - 130px)",  # Subtract header (70px) and footer (60px)
                "position": "relative",
                "padding": "20px",
            },
            children=[
                dmc.Title(
                    "404",
                    order=1,
                    id="not-found-title",
                    className="glitch-text",
                    style={
                        "fontSize": "clamp(60px, 12vw, 150px)",  # Reduced from 200px max
                        "fontWeight": 900,
                        "margin": 0,
                        "textShadow": "0 0 20px rgba(99, 102, 241, 0.5)",
                    }
                ),

                dmc.Text(
                    "Oops! This page got lost in the digital void",
                    size="lg",
                    ta="center",
                    id="not-found-subtitle",
                    style={
                        "fontSize": "clamp(14px, 2.5vw, 20px)",  # Reduced from 24px max
                        "maxWidth": "500px",
                        "padding": "0 20px",
                    }
                ),

                dmc.Group(
                    gap="md",
                    justify="center",
                    style={"padding": "0 20px"},
                    children=[
                        dmc.Anchor(
                            dmc.Button(
                                "Go Home",
                                size="md",  # Changed from lg to md
                                variant="gradient",
                                gradient={"from": "indigo", "to": "cyan"},
                                className="home-button-404",
                                style={
                                    "fontSize": "clamp(13px, 2vw, 16px)",
                                }
                            ),
                            href="/",
                            style={"textDecoration": "none"},
                        ),
                    ]
                ),
            ]
        ),
    ],
    style={
        "height": "calc(100vh - 130px)",  # Exact height to prevent overflow
        "overflow": "hidden",
        "position": "relative",
    }
)