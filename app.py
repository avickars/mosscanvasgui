import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from canvas.canvas_class import canvas, getPath
from columns.left_bar import settings, courses, assignments, languages, fileExtensions, baseFiles
from columns.center_bar import dtTable
from columns.right_bar3 import execute, results, mossSideBar, results2
from dash.dependencies import Input, Output, State
from local.local_class import local
import os

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

canvasObject = canvas()

localObject = local()

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
            courses(canvasObject), html.Br(), assignments(), html.Br(), languages(), html.Br(), fileExtensions(), html.Br(), baseFiles(), html.Br(), settings(canvasObject)
        ], id="col-1", className="column"), className="col-outer", id="col-outer1"),
        html.Div(html.Div(children=[dtTable()], id="col-2"), className="col-outer", id="col-outer2"),
        html.Div(html.Div(children=[execute(), html.Br(), mossSideBar(), html.Br(), html.Br(), results(), results2()], id="col-3", className='column'),
                 className="col-outer", id="col-outer3")
    ])
], id="base")


# Callback for left column side bar collapse
@app.callback(
    [Output(f"collapse-{i}", "is_open") for i in range(1, 7)],
    [Input(f"group-{i}-toggle", "n_clicks") for i in range(1, 7)],
    [State(f"collapse-{i}", "is_open") for i in range(1, 7)],
)
def toggle_accordion(n1, n2, n3, n4, n5, n6, is_open1, is_open2, is_open3, is_open4, is_open5, is_open6):
    ctx = dash.callback_context
    if not ctx.triggered:
        return False, False, False, False, False, False
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "group-1-toggle" and n1:
        return not is_open1, False, False, False, False, False
    elif button_id == "group-2-toggle" and n2:
        return False, not is_open2, False, False, False, False
    elif button_id == "group-3-toggle" and n3:
        return False, False, not is_open3, False, False, False
    elif button_id == "group-4-toggle" and n4:
        return False, False, False, not is_open4, False, False
    elif button_id == "group-5-toggle" and n5:
        return False, False, False, False, not is_open5, False
    elif button_id == "group-6-toggle" and n6:
        return False, False, False, False, False, not is_open6
    else:
        return False, False, False, False, False, False


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


# Toggle far sidebar->base-file->modal
@app.callback(
    Output("base-file-modal", "is_open"),
    [Input("open-base-file-modal", "n_clicks"), Input("close-base-file-model", "n_clicks")],
    [State("base-file-modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# Toggle far sidebar->file-extensions->modal
@app.callback(
    Output("file-ext-modal", "is_open"),
    [Input("open-file-ext-modal", "n_clicks"), Input("close-file-ext-model", "n_clicks")],
    [State("file-ext-modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# Dynamically update the courses in the course drop down when the API key changes
@app.callback(
    Output('course-dropdown', 'options'),
    [Input('canvas-api-key', 'value'),
     Input('semester-year', 'value'),
     Input('semester-season', 'value')]
)
def updateCoursesDropdown(value, semesterYear, semesterSeason):
    canvasObject.changeKey(value)
    return canvasObject.getCourses(semesterYear, semesterSeason)


# Dynamically update assignment dropdown based on course dropdown
@app.callback(
    dash.dependencies.Output('assignment-dropdown', 'options'),
    [dash.dependencies.Input('course-dropdown', 'value')]
)
def updateAssignmentsDropdown(value):
    return canvasObject.getAssignments(value)


# Changes the datatable when one of the outputs is changed
@app.callback(
    [Output('datatable', 'data'), Output('datatable', 'columns')],
    [Input('course-dropdown', 'value'),
     Input('assignment-dropdown', 'value'),
     Input('language-dropdown', 'value'),
     Input('fileExtension-input', 'value'),
     Input('local-select', 'value'),
     Input("assignment-path", 'value'),
     Input('base-file-textarea', 'value'),
     Input('semester-year', 'value'),
     Input('semester-season', 'value')]
)
def updateTableData(courseNumber, assignmentNumber, languageValue, fileExtensionValue, localCanvasValue, assignmentPath, baseFile, semesterYear, semesterSeason):
    if localCanvasValue == 'canvas':
        df = canvasObject.getSubmissions(courseNumber, assignmentNumber, languageValue, fileExtensionValue, semesterYear, semesterSeason)
        return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]
    else:
        localObject.changePath(assignmentPath)
        df = localObject.getSubmissions(fileExtensionValue, languageValue, baseFile)
        return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]


# This callback updates the run button to be clickable when there is data contained in the data table.
@app.callback(
    [Output('download-button', 'disabled'), Output('run-moss', 'disabled')],
    [Input('datatable', "derived_virtual_data"), Input('local-select', 'value')]
)
def enableExecuteButton(rows, localCanvas):
    if localCanvas == 'canvas':
        if rows is None:
            return True, True

        for row in rows:
            if row != {'Error': 'At least one of Course, Assignment, Language, or File Extension has not been selected'} and row != {'Error': "No Canvas Key or Invalid Canvas Key "
                                                                                                                                              "Detected"}:
                return False, False
        return True, True
    else:
        if rows is None:
            return True, True
        for row in rows:
            if row == {"Error": 'At least one of Language or File Extension has not been selected or you have entered an Invalid Base File'} or row == {"Error": 'Invalid Path'}:
                return True, True
        return True, False


# This call back downloads the assignments
@app.callback(
    Output("results", "children"),
    [
        Input("download-button", "n_clicks"),
        Input('datatable', "derived_virtual_data"),
        Input('datatable', "derived_virtual_selected_rows"),
        Input('course-dropdown', 'value'),
        Input('assignment-dropdown', 'value'),
        Input('fileExtension-input', 'value')
    ]
)
def getSubmissionData(numClicks, data, selectedRows, courseValue, assignmentValue, fileExtensionValue):
    if numClicks is None:
        print("Not executed ")
        return f"Clicked 0 times."
    if numClicks > 0:
        if len(selectedRows) > 0:
            canvasObject.downloadSubmissions([data[i] for i in selectedRows], courseValue, assignmentValue, fileExtensionValue)
        else:
            canvasObject.downloadSubmissions(data, courseValue, assignmentValue, fileExtensionValue)
        return f"Clicked {numClicks} times."


@app.callback(
    [Output('moss-report-link', 'children'),
     Output('moss-report-link', 'href'),
     Output('moss-report-link', 'style'),
     Output('moss-barplot-link', 'children'),
     Output('moss-barplot-link', 'href'),
     Output('moss-barplot-link', 'style')
     ],
    [Input('course-dropdown', 'value'),
     Input('assignment-dropdown', 'value'),
     Input("results2", "children"),
     Input('local-select', 'value'),
     Input("assignment-path", 'value')
     ]
)
def mossReportLink(courseNumber, assignmentNumber, resultsDummyValue, localSelect, assignmentPath):
    if localSelect == 'canvas':
        reportLink, barplotLink = getPath(canvasObject.getCanvas(), assignmentNumber, courseNumber)
        if reportLink == '/' and barplotLink == '/':
            return ['No Moss Report Detected'], \
                   reportLink, \
                   {'cursor': 'default', 'pointer-events': 'none', 'text-decoration': 'none', 'color': 'grey'}, \
                   ['No Bar Plot Detected'], \
                   barplotLink, \
                   {'cursor': 'default', 'pointer-events': 'none', 'text-decoration': 'none', 'color': 'grey'}
        elif reportLink != '/' and barplotLink == '/':
            return ['mossReport.html'], \
                   reportLink, \
                   {"color": "darkred"}, \
                   ['No Bar Plot Detected'], \
                   barplotLink, \
                   {'cursor': 'default', 'pointer-events': 'none', 'text-decoration': 'none', 'color': 'grey'}
        elif reportLink == '/' and barplotLink != '/':
            return ['No Moss Report Detected'], \
                   reportLink, \
                   {'cursor': 'default', 'pointer-events': 'none', 'text-decoration': 'none', 'color': 'grey'}, \
                   ['mossBarplot.html'], \
                   barplotLink, \
                   {"color": "darkred"}
        else:
            print("reportLink: ", reportLink)
            return ['mossReport.html'], \
                   reportLink, \
                   {"color": "darkred"}, \
                   ['mossBarplot.html'], \
                   barplotLink, \
                   {"color": "darkred"}
    else:
        if os.path.exists(assignmentPath + '/mossReport.html') and os.path.exists(assignmentPath + '/mossBarplot.html'):
            print(assignmentPath + 'mossReport.html')
            return ['mossReport.html'], \
                   'file://' + assignmentPath + '/mossReport.html', \
                   {"color": "darkred"}, \
                   ['mossBarplot.html'], \
                   'file://' + assignmentPath + '/mossBarplot.html', \
                   {"color": "darkred"}
        elif os.path.exists(assignmentPath + '/mossReport.html') and not os.path.exists(assignmentPath + '/mossBarplot.html'):
            return ['mossReport.html'], \
                   'file://' + assignmentPath + '/mossReport.html', \
                   {"color": "darkred"}, \
                   ['No Bar Plot Detected'], \
                   '/', \
                   {'cursor': 'default', 'pointer-events': 'none', 'text-decoration': 'none', 'color': 'grey'}
        elif not os.path.exists(assignmentPath + '/mossReport.html') and os.path.exists(assignmentPath + '/mossBarplot.html'):
            return ['No Moss Report Detected'], \
                   '/', \
                   {'cursor': 'default', 'pointer-events': 'none', 'text-decoration': 'none', 'color': 'grey'}, \
                   ['mossBarplot.html'], \
                   'file://' + assignmentPath + '/mossBarplot.html', \
                   {"color": "darkred"}
        else:
            return ['No Moss Report Detected'], \
                   '/', \
                   {'cursor': 'default', 'pointer-events': 'none', 'text-decoration': 'none', 'color': 'grey'}, \
                   ['No Bar Plot Detected'], \
                   '/', \
                   {'cursor': 'default', 'pointer-events': 'none', 'text-decoration': 'none', 'color': 'grey'}


# This call back executes when the run button is clicked.  It will download the assignments and then run them through Moss.
@app.callback(
    Output("results2", "children"),
    [
        Input("run-moss", "n_clicks"),
        Input('datatable', "derived_virtual_data"),
        Input('datatable', "derived_virtual_selected_rows"),
        Input('course-dropdown', 'value'),
        Input('assignment-dropdown', 'value'),
        Input('language-dropdown', 'value'),
        Input('fileExtension-input', 'value'),
        Input('local-select', 'value'),
        Input('directory-select', 'value'),
        Input('base-file-textarea', 'value')
    ]
)
def executeFileSimilarity(numClicks, data, selectedRows, courseValue, assignmentValue, languageValue, fileExtensionValue, localDirectory, fileDirectory, baseFiles):
    if data is not None and len(data) > 0:
        if "Error" in data[0].keys():
            return f"Clicked 0 times."
    if localDirectory == 'canvas':
        if numClicks is None:
            return f"Clicked 0 times."
        if numClicks > 0:
            if len(selectedRows) > 0:
                canvasObject.moss([data[i] for i in selectedRows], courseValue, assignmentValue, languageValue, fileExtensionValue, baseFiles)
                return f"Clicked {numClicks} times."
            else:
                canvasObject.moss(data, courseValue, assignmentValue, languageValue, fileExtensionValue, baseFiles)
                return f"Clicked {numClicks} times."
    else:
        if numClicks is None:
            print("Not executed ")
            return f"Clicked 0 times."
        if len(selectedRows) > 0:
            localObject.moss([data[i] for i in selectedRows], fileDirectory, languageValue, fileExtensionValue, baseFiles)
            return f"Clicked {numClicks} times."
        else:
            localObject.moss(data, fileDirectory, languageValue, fileExtensionValue, baseFiles)
            return f"Clicked {numClicks} times."


# Callback for right side bar collapse
@app.callback(
    [Output(f"right-collapse-{i}", "is_open") for i in range(1, 3)],
    [Input(f"right-group-{i}-toggle", "n_clicks") for i in range(1, 3)],
    [State(f"right-collapse-{i}", "is_open") for i in range(1, 3)],
)
def toggle_accordion(n1, n2, is_open1, is_open2):
    ctx = dash.callback_context
    if not ctx.triggered:
        return False, False
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "right-group-1-toggle" and n1:
        return not is_open1, False
    elif button_id == "right-group-2-toggle" and n2:
        return False, not is_open2
    else:
        return False, False


# If the use wants to run Moss on local assignments, this toggle will disable all canvas related things
@app.callback(
    [Output("assignment-path", "disabled"),
     Output("canvas-api-key", "disabled"),
     Output("group-1-toggle", "disabled"),
     Output("group-3-toggle", "disabled"),
     Output('directory-select', 'options'),
     Output('semester-season', "disabled"),
     Output('semester-year', "disabled")],
    [Input('local-select', 'value')]
)
def toggleLocal(value):
    if value == 'local':
        return False, True, True, True, [{'label': 'By File', 'value': 'File'}, {'label': 'By Directory', 'value': 'directory'}], True, True
    else:
        return True, False, False, False, [{'label': 'By File', 'value': 'File', 'disabled': True}, {'label': 'By Directory', 'value': 'directory', 'disabled': True}], False, False


# Toggle far Right_bar->settings->modal
@app.callback(
    Output("local-modal", "is_open"),
    [Input("open-local-model", "n_clicks"), Input("close-local-model", "n_clicks")],
    [State("local-modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# Start the Dash server
if __name__ == '__main__':
    app.run_server(debug=True)
