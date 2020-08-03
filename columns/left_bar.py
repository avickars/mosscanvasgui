import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from canvas.canvas_class import canvas


# from canvas.canvasKey import readKey
# from canvas.canvasMethods import getCourses, getAssignments


def courses(canvas):
    # we use this function to make the example items to avoid code duplication
    return dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button("Course",
                               id="group-1-toggle",
                               className="sidebarbuttons"),
                    className="headersidebar"),
                className="sidebarcards"
            ),
            dbc.Collapse(
                # dbc.CardBody(children=[dash_table.DataTable(data=readCourseDataFromApp('canvas/'))], id="card-body"),
                dbc.CardBody(children=[dcc.Dropdown(options=canvas.getCourses(),
                                                    id="course-dropdown",
                                                    optionHeight=120)], id="card-body"),
                id="collapse-1"
            ),
        ]
    )


def assignments():
    # we use this function to make the example items to avoid code duplication
    return dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button("Assignment",
                               id="group-3-toggle",
                               className="sidebarbuttons"),
                    className="headersidebar"),
                className="sidebarcards"
            ),
            dbc.Collapse(
                dbc.CardBody(children=[dcc.Dropdown(id="assignment-dropdown")], id="assignment-card-body"),
                id="collapse-3"
            ),
        ]
    )


def languages():
    # we use this function to make the example items to avoid code duplication
    return dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button("Language",
                               id="group-4-toggle",
                               className="sidebarbuttons"),
                    className="headersidebar"),
                className="sidebarcards"
            ),
            dbc.Collapse(
                dbc.CardBody(children=[dcc.Dropdown(id="language-dropdown",
                                                    options=[
                                                        {'label': 'C', 'value': 'c'},
                                                        {'label': 'C++', 'value': 'cc'},
                                                        {'label': 'Java', 'value': 'java'},
                                                        {'label': 'ML', 'value': 'ml'},
                                                        {'label': 'OCaml', 'value': 'ocaml'},
                                                        {'label': 'Ruby', 'value': 'ruby'},
                                                        {'label': 'Pascal', 'value': 'pascal'},
                                                        {'label': 'Ada', 'value': 'ada'},
                                                        {'label': 'Lisp', 'value': 'lisp'},
                                                        {'label': 'Scheme', 'value': 'scheme'},
                                                        {'label': 'Haskell', 'value': 'haskell'},
                                                        {'label': 'Fortran', 'value': 'fortran'},
                                                        {'label': 'Ascii', 'value': 'ascii'},
                                                        {'label': 'VHDL', 'value': 'vhdl'},
                                                        {'label': 'Perl', 'value': 'perl'},
                                                        {'label': 'Matlab', 'value': 'matlab'},
                                                        {'label': 'Python', 'value': 'python'},
                                                        {'label': 'Mips', 'value': 'mips'},
                                                        {'label': 'Prolog', 'value': 'prolog'},
                                                        {'label': 'Spice', 'value': 'spice'},
                                                        {'label': 'CB', 'value': 'vb'},
                                                        {'label': 'C#', 'value': 'csharp'},
                                                        {'label': 'Aodula2', 'value': 'modula2'},
                                                        {'label': 'A8086', 'value': 'a8086'},
                                                        {'label': 'JavaScript', 'value': 'javascript'},
                                                        {'label': 'PLSQL', 'value': 'plsql'},
                                                        {'label': 'Verilog', 'value': 'verilog'},
                                                        {'label': 'TCL', 'value': 'tcl'},
                                                        {'label': 'HC12', 'value': 'hc12'}

                                                    ])], id="language-card-body"),
                id="collapse-4"
            ),
        ]
    )


def fileExtensions():
    return dbc.Card(
        [
            dbc.CardHeader(
                dbc.Button("File Extensions",
                           id="group-5-toggle",
                           className="sidebarbuttons"),
                className="sidebarcards"
            ),
            dbc.Collapse(
                dbc.CardBody(children=[
                    html.H6("File Extensions"),
                    dcc.Input(placeholder="Enter the expected file extensions separated by a comma", id="fileExtension-input", className='user-inputs'),
                    html.Small("NOTE: Only files with specified extensions will be downloaded and run through Moss.  Example: .c,.h"),
                    html.Small("NOTE: If students submitted .zip files, specify this here."),
                ]),
                id="collapse-5"
            ),
        ],
        className="card"
    )


def settings(canvas):
    # we use this function to make the example items to avoid code duplication
    return dbc.Card(
        [
            dbc.CardHeader(
                dbc.Button("Settings",
                           id="group-2-toggle",
                           className="sidebarbuttons"),
                className="sidebarcards"
            ),
            dbc.Collapse(
                dbc.CardBody(children=[
                    html.H6("Canvas Key"),
                    dcc.Input(placeholder="Enter your Canvas Key", id="canvas-api-key", value=canvas.getKey(), className='user-inputs'),
                    html.Small("What is this?", id="open-canvas-key-modal"),
                    dbc.Modal(children=[
                        dbc.ModalHeader("What is a \"Canvas Key?\""),
                        dbc.ModalBody(children=[
                            "A \"Canvas Key\" is a key used in this app to authenticate requests for student assignments.", "\n To generate a key:",
                            html.Ol(children=[
                                html.Li("Click the \"profile\" link in the top right menu bar, or navigate to profile"),
                                html.Li("Under the \"Approved Integrations\" section, click the button to generate a new access token."),
                                html.Li("Once the token is generated, copy and paste it into the \"Canvas Key\" text field")
                            ])]),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close-canvas-key-model", className="ml-auto")
                        ),
                    ], id="canvas-key-modal"),
                    html.Br(),
                    html.Br(),
                    html.H6("Source"),
                    html.Small("What is this?", id="open-local-model"),
                    dbc.Modal(children=[
                        dbc.ModalHeader("What form does this need to be in?"),
                        dbc.ModalBody(children=[
                            "Needs to have the form that:",
                        ]),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close-local-model", className="ml-auto")
                        ),
                    ], id="local-modal"),
                    dcc.RadioItems(
                        options=[{'label': 'Local', 'value': 'local'}, {'label': 'Canvas', 'value': 'canvas'}],
                        id='local-select',
                        value='canvas'
                    ),
                    dbc.RadioItems(
                        options=[{'label': 'By File', 'value': 'File', 'disabled': True}, {'label': 'By Directory', 'value': 'directory', 'disabled': True}],
                        id='directory-select',
                        value='directory'
                    ),
                    dcc.Input(placeholder="path", id="assignment-path", className='user-inputs', disabled=True)
                ]),
                id="collapse-2"
            ),
        ],
        className="card"
    )
