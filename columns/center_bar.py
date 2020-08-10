import dash_table


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
