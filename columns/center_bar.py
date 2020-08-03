import dash_table
import pandas as pd
from canvas.canvas_class import canvas
import dash_bootstrap_components as dbc
import dash_html_components as html

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            dash_table.DataTable(
                id='datatable',
                editable=True,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                column_selectable="single",
                row_selectable="multi",
                row_deletable=True,
                selected_columns=[],
                selected_rows=[],
                page_action="native",
                style_cell_conditional=[
                    {
                        'if': {'column_id': c},
                        'display': 'none'
                    } for c in ['canvasID', 'extension', 'downloadURL']
                ]
            )
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 2!", className="card-text")
        ]
    ),
    className="mt-3",
)

tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="All"),
        dbc.Tab(tab2_content, label="Downloaded")
    ]
)

def tabTable():
    return tabs


def dtTable():
    return dash_table.DataTable(
        id='datatable',
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        style_cell_conditional=[
            {
                'if': {'column_id': c},
                'display': 'none'
            } for c in ['canvasID', 'extension', 'downloadURL']
        ]
    )
