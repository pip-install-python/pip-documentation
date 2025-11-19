import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import html

excluded_links = [
    "/404",
    "/styles-api",
    "/style-props",
    "/dash-iconify",
    "/migration",
    "/learning-resources",
    "/analytics",  # Analytics pages have their own section
    "/analytics/traffic",
]

category_data = {
    "Components": {"icon": "line-md:document-list"},
    # "Resources": {"icon": "line-md:medical-services-twotone"},
    "Analytics": {"icon": "line-md:cloud-alt-print-twotone-loop"},
}


def create_nav_link(icon, text, href, external=False):
    """Create a styled navigation link with icon"""
    return dmc.Anchor(
        dmc.Group(
            [
                DashIconify(icon=icon, width=18),
                dmc.Text(text, size="sm", fw=500),
            ],
            gap="sm",
        ),
        href=href,
        target="_blank" if external else None,
        className="navbar-link",
        underline=False,
    )


def create_nav_section(title, links):
    """Create a navigation section with a title and links (used for mobile)"""
    return dmc.Stack(
        [
            dmc.Divider(
                label=[
                    DashIconify(
                        icon=category_data[title]["icon"],
                        height=23,
                        style={"color": "light-dark(rgb(28, 126, 214), #74c0fc)"}
                    ),
                    dmc.Text(
                        title,
                        ml=5,
                        size="sm",
                        fw=500,
                        style={"color": "light-dark(rgb(28, 126, 214), #74c0fc)"}
                    ),
                ],
                labelPosition="left",
                style={"borderColor": "light-dark(rgb(28, 126, 214), #74c0fc)"}
            ),
            dmc.Stack(links, gap="xs"),
        ],
        gap="sm",
    )


def create_nav_section_accordion(title, links):
    """Create an accordion navigation section (used for desktop/tablet)"""
    return dmc.AccordionItem(
        value=title.lower(),
        children=[
            dmc.AccordionControl(
                dmc.Group(
                    [
                        DashIconify(
                            icon=category_data[title]["icon"],
                            height=20,
                        ),
                        dmc.Text(
                            title,
                            size="sm",
                            fw=500,
                        ),
                    ],
                    gap="sm",
                )
            ),
            dmc.AccordionPanel(
                dmc.Stack(links, gap="xs", pt="xs")
            ),
        ],
    )


def get_page_links(data):
    """Extract and order page links from data"""
    # Define the desired order for documentation pages
    page_order = [
        "Getting Started",
        "Custom Directives",
        "AI/LLM Integration",
        "Interactive .md",
        "Data Visualization",
    ]

    # Create a mapping of page names to their links
    page_dict = {}
    for entry in data:
        if entry["path"] not in excluded_links and entry["path"] != "/":
            link = create_nav_link(
                entry.get("icon", "fluent:document-24-regular"),
                entry["name"],
                entry["path"]
            )
            page_dict[entry["name"]] = link

    # Order the links according to page_order
    page_links = []
    for page_name in page_order:
        if page_name in page_dict:
            page_links.append(page_dict[page_name])

    # Add any remaining pages that aren't in the specified order
    for name, link in page_dict.items():
        if name not in page_order:
            page_links.append(link)

    return page_links


def get_analytics_links():
    """Get analytics section links"""
    return [
        create_nav_link(
            "fluent:money-24-regular",
            "Api Cost",
            "/analytics"
        ),
        create_nav_link(
            "fluent:data-bar-vertical-24-regular",
            "Traffic",
            "/analytics/traffic"
        ),
    ]


def create_content_desktop(data):
    """Create desktop navbar content with accordion sections"""
    page_links = get_page_links(data)
    analytics_links = get_analytics_links()

    return dmc.ScrollArea(
        offsetScrollbars=True,
        type="scroll",
        style={"height": "100%"},
        children=dmc.Stack(
            [
                # Home link
                create_nav_link(
                    "line-md:home-alt-twotone",
                    "Index",
                    "/"
                ),
                create_nav_link(
                    "streamline-pixel:content-files-favorite-book",
                    "Docs Boilerplate",
                    "https://dash-documentation-boilerplate.onrender.com/"
                ),

                # Accordion for sections
                dmc.Accordion(
                    value="components",  # Components section open by default
                    chevronPosition="left",
                    variant="separated",
                    children=[
                        # Documentation Pages Section
                        create_nav_section_accordion(
                            "Components",
                            page_links
                        ),

                        # Analytics Section
                        create_nav_section_accordion(
                            "Analytics",
                            analytics_links
                        ),
                    ],
                ),
            ],
            gap="xs",
            p="md",
        ),
    )


def create_content_mobile(data):
    """Create mobile navbar content with simple sections (no accordion)"""
    page_links = get_page_links(data)
    analytics_links = get_analytics_links()

    return dmc.ScrollArea(
        offsetScrollbars=True,
        type="scroll",
        style={"height": "100%"},
        children=dmc.Stack(
            [
                # Home link
                create_nav_link(
                    "line-md:home-alt-twotone",
                    "Index",
                    "/"
                ),
                create_nav_link(
                    "streamline-pixel:content-files-favorite-book",
                    "Docs Boilerplate",
                    "https://dash-documentation-boilerplate.onrender.com/"
                ),

                # Documentation Pages Section
                create_nav_section(
                    "Components",
                    page_links
                ),

                # Analytics Section
                create_nav_section(
                    "Analytics",
                    analytics_links
                ),
            ],
            gap="xs",
            p="md",
        ),
    )


def create_navbar(data):
    """Create the main application navbar (desktop/tablet with accordion)"""
    return dmc.AppShellNavbar(
        children=create_content_desktop(data),
        style={"borderRight": "1px solid #03c7e5"}
    )


def create_navbar_drawer(data):
    """Create mobile drawer navigation (without accordion)"""
    return dmc.Drawer(
        id="components-navbar-drawer",
        overlayProps={"opacity": 0.55, "blur": 3},
        zIndex=1500,
        offset=8,
        radius="md",
        withCloseButton=False,
        size="280px",
        children=create_content_mobile(data),
        trapFocus=False,
        position="left",
    )
