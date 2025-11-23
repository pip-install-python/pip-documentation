"""
IABS Combined PDF Viewer Page
Displays the Texas Real Estate Commission Information About Brokerage Services document
"""
import dash_mantine_components as dmc
from dash import html, register_page, callback, Output, Input
from dash_iconify import DashIconify
import dash_pdf
from pathlib import Path

from lib.constants import PAGE_TITLE_PREFIX

register_page(
    __name__,
    "/trec-combined.pdf",
    title=PAGE_TITLE_PREFIX + "IABS Combined - Texas Real Estate Commission",
)


def layout():
    """Create the PDF viewer layout"""
    # Read the PDF file as bytes
    pdf_path = Path("assets/advertising/IABS-combined.pdf")
    pdf_bytes = pdf_path.read_bytes()

    return dmc.Container(
        size="xl",
        py="xl",
        children=[
            # Header Section
            dmc.Paper(
                p="lg",
                mb="lg",
                withBorder=True,
                radius="md",
                children=[
                    dmc.Stack(
                        gap="md",
                        children=[
                            dmc.Group(
                                justify="space-between",
                                align="center",
                                children=[
                                    dmc.Group(
                                        gap="sm",
                                        align="center",
                                        children=[
                                            DashIconify(
                                                icon="mdi:file-pdf-box",
                                                width=32,
                                                color="#EF4444"
                                            ),
                                            dmc.Title(
                                                "Information About Brokerage Services",
                                                order=2,
                                                style={"margin": 0}
                                            ),
                                        ]
                                    ),
                                    html.A(
                                        dmc.Button(
                                            "Download PDF",
                                            leftSection=DashIconify(icon="mdi:download", width=18),
                                            variant="light",
                                            color="blue",
                                            size="sm",
                                        ),
                                        href="/assets/advertising/IABS-combined.pdf",
                                        download="IABS-combined.pdf",
                                        target="_blank",
                                        style={"textDecoration": "none"},
                                    ),
                                ]
                            ),
                            dmc.Text(
                                "Texas Real Estate Commission (TREC) disclosure document required for all real estate transactions. "
                                "This document provides information about types of real estate license holders, broker duties, "
                                "and representation options.",
                                size="sm",
                                c="dimmed",
                            ),
                            dmc.Divider(),
                            dmc.Group(
                                gap="xl",
                                children=[
                                    dmc.Group(
                                        gap="xs",
                                        children=[
                                            DashIconify(icon="mdi:file-document-outline", width=16, color="gray"),
                                            dmc.Text("2 Pages", size="sm", c="dimmed"),
                                        ]
                                    ),
                                    dmc.Group(
                                        gap="xs",
                                        children=[
                                            DashIconify(icon="mdi:calendar", width=16, color="gray"),
                                            dmc.Text("Updated: 11-2-2015", size="sm", c="dimmed"),
                                        ]
                                    ),
                                    dmc.Group(
                                        gap="xs",
                                        children=[
                                            DashIconify(icon="mdi:office-building", width=16, color="gray"),
                                            dmc.Text("TREC Form IABS 1-0", size="sm", c="dimmed"),
                                        ]
                                    ),
                                ]
                            ),
                        ]
                    )
                ]
            ),

            # PDF Viewer Section
            dmc.Paper(
                p="xl",
                withBorder=True,
                radius="md",
                style={
                    "backgroundColor": "var(--mantine-color-gray-0)",
                    "minHeight": "600px",
                },
                id="pdf-viewer-container",
                children=[
                    html.Div(
                        id="pdf-viewer-wrapper",
                        children=[
                            dash_pdf.PDF(
                                id="pdf-viewer",
                                data=pdf_bytes,
                                buttonClassName="pdf-nav-button",
                                labelClassName="pdf-page-label",
                                controlsClassName="pdf-controls",
                            )
                        ]
                    )
                ]
            ),

            # Footer Info Section
            dmc.Paper(
                p="md",
                mt="lg",
                withBorder=True,
                radius="md",
                children=[
                    dmc.Stack(
                        gap="sm",
                        children=[
                            dmc.Group(
                                gap="xs",
                                children=[
                                    DashIconify(icon="mdi:information-outline", width=20, color="blue"),
                                    dmc.Title("About This Document", order=4, style={"margin": 0}),
                                ]
                            ),
                            dmc.Text(
                                "This form is provided by the Texas Real Estate Commission (TREC) and must be given to "
                                "all prospective buyers, tenants, sellers, and landlords at the first substantive dialogue "
                                "with a real estate professional.",
                                size="sm",
                            ),
                            dmc.List(
                                size="sm",
                                spacing="xs",
                                children=[
                                    dmc.ListItem("Explains types of real estate license holders (Brokers and Sales Agents)"),
                                    dmc.ListItem("Outlines minimum duties required by law"),
                                    dmc.ListItem("Describes different representation options (Owner Agent, Buyer Agent, Intermediary)"),
                                    dmc.ListItem("Provides information about the Real Estate Recovery Trust Account"),
                                ]
                            ),
                            dmc.Group(
                                gap="md",
                                mt="sm",
                                children=[
                                    dmc.Anchor(
                                        dmc.Button(
                                            "Visit TREC Website",
                                            leftSection=DashIconify(icon="mdi:open-in-new", width=16),
                                            variant="light",
                                            size="xs",
                                        ),
                                        href="https://www.trec.texas.gov",
                                        target="_blank",
                                    ),
                                    dmc.Anchor(
                                        dmc.Button(
                                            "Check License Status",
                                            leftSection=DashIconify(icon="mdi:shield-check-outline", width=16),
                                            variant="light",
                                            size="xs",
                                            color="green",
                                        ),
                                        href="https://www.trec.texas.gov",
                                        target="_blank",
                                    ),
                                ]
                            ),
                        ]
                    )
                ]
            ),
        ]
    )


# Theme-aware callback for PDF container background
@callback(
    Output("pdf-viewer-container", "style"),
    Input("color-scheme-storage", "data"),
)
def update_pdf_container_theme(theme):
    """Update PDF container background based on theme"""
    if theme == "dark":
        return {
            "backgroundColor": "var(--mantine-color-dark-6)",
            "minHeight": "600px",
        }
    return {
        "backgroundColor": "var(--mantine-color-gray-0)",
        "minHeight": "600px",
    }