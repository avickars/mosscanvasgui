import dash_bootstrap_components as dbc
import dash_html_components as html


def execute():
    return html.Div(
        dbc.Button("Run",
                   className="sidebarbuttons",id='execute-button', disabled=True),
        id="execute-container")


def results():
    return html.Div("Moss Results", id='results')
