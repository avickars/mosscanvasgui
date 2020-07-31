import dash_table
import pandas as pd
from canvas.canvas_class import canvas
import dash_bootstrap_components as dbc
import dash_html_components as html

# df = getSubmissions(None, None, None, None, 'canvas/')
#
# def getSubmissions


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

