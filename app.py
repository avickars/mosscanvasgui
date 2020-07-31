import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from canvas.canvas_class import canvas
from sidebars.sidebar1 import settings, courses, assignments, languages, fileExtensions
from sidebars.sidebar2 import dtTable
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
canvasObject = canvas()

navBar = dbc.Navbar(children=[
    html.A(
        # Use row and col to control vertical alignment of logo / brand
        dbc.Row(
            [
                dbc.Col(html.Img(src=app.get_asset_url('/CMPTLogo.png'), alt="Image N/A", height="30px")),
                dbc.Col(dbc.NavbarBrand("CS Assignment Similarity Checker", className="ml-2")),
            ],
            align="center",
            no_gutters=True,
        ),
    )
],
    color="darkred",
    dark=True,
)

# App layout
app.layout = html.Div(children=[
    html.Div(id="row-1", children=[navBar]),
    html.Div(id="row-2", children=[
        html.Div(html.Div(children=[
            courses(canvasObject), html.Br(), assignments(), html.Br(), languages(), html.Br(), fileExtensions(), html.Br(), settings(canvasObject)
        ], id="col-1", className="column"), className="col-outer", id="col-outer1"),
        html.Div(html.Div(children=[dtTable()], id="col-2"), className="col-outer", id="col-outer2")
    ])
], id="base")


# Callback for side bar collapse
@app.callback(
    [Output(f"collapse-{i}", "is_open") for i in range(1, 6)],
    [Input(f"group-{i}-toggle", "n_clicks") for i in range(1, 6)],
    [State(f"collapse-{i}", "is_open") for i in range(1, 6)],
)
def toggle_accordion(n1, n2, n3, n4, n5, is_open1, is_open2, is_open3, is_open4, is_open5):
    ctx = dash.callback_context
    if not ctx.triggered:
        return False, False, False, False, False
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "group-1-toggle" and n1:
        return not is_open1, False, False, False, False
    elif button_id == "group-2-toggle" and n2:
        return False, not is_open2, False, False, False
    elif button_id == "group-3-toggle" and n3:
        return False, False, not is_open3, False, False
    elif button_id == "group-4-toggle" and n4:
        return False, False, False, not is_open4, False
    elif button_id == "group-5-toggle" and n5:
        return False, False, False, False, not is_open5
    else:
        return False, False, False, False, False


# Toggle far sidebar->settings->modal
@app.callback(
    Output("canvas-key-modal", "is_open"),
    [Input("open-canvas-key-modal", "n_clicks"), Input("close-canvas-key-model", "n_clicks")],
    [State("canvas-key-modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# Dynamically update the courses in the course drop down when the API key changes
@app.callback(
    Output('course-dropdown', 'options'),
    [Input('canvas-api-key', 'value')]
)
def updateCoursesDropdown(value):
    canvasObject.changeKey(value)
    return canvasObject.getCourses()


# Dynamically update assignment dropdown based on course dropdown
@app.callback(
    dash.dependencies.Output('assignment-dropdown', 'options'),
    [dash.dependencies.Input('course-dropdown', 'value')]
)
def updateAssignmentsDropdown(value):
    # print("In up Assignments")
    # print(value)
    return canvasObject.getAssignments(value)

# Changes the datatable when one of the outputs is changed
@app.callback(
    [Output('datatable', 'data'), Output('datatable', 'columns')],
    # Output('temp', 'children'),
    [Input('course-dropdown', 'value'),
     Input('assignment-dropdown', 'value'),
     Input('language-dropdown', 'value'),
     Input('fileExtension-input', 'value')]
)
def updateTableData(courseNumber, assignmentNumber, languageValue, fileExtensionValue):
    df = canvasObject.getSubmissions(courseNumber, assignmentNumber, languageValue, fileExtensionValue)
    return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]


# Start the Dash server
if __name__ == '__main__':
    app.run_server(debug=True)
