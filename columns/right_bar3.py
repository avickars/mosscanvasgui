import dash_bootstrap_components as dbc
import dash_html_components as html


def execute():
    return html.Div(
        dbc.Button("Download",
                   className="sidebarbuttons", id='download-button', disabled=True),
        id="execute-container")


def mossSideBar():
    return dbc.Card(
        [
            dbc.CardHeader(
                dbc.Button("Moss", id="right-group-1-toggle", className="sidebarbuttons"),
                className="sidebarcards"
            ),
            dbc.Collapse(
                dbc.CardBody(children=[
                    dbc.Button("Run", id="run-moss", className="sidebarbuttons", disabled=True)
                ]),
                id="right-collapse-1"
            ),
        ],
        className="card"
    )


def placeHolderToggle():
    return dbc.Card(
        [
            dbc.CardHeader(
                dbc.Button("Moss",
                           id="right-group-2-toggle",
                           className="sidebarbuttons"),
                className="sidebarcards"
            ),
            dbc.Collapse(
                dbc.CardBody(children=[
                    dbc.Button("Run",
                               id="palceholder",
                               className="sidebarbuttons")
                ]),
                id="right-collapse-2"
            ),
        ],
        className="card"
    )


def results():
    return html.Div("Moss Results", id='results')


def results2():
    return html.Div("Moss Results", id='results2')
