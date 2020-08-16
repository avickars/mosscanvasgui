import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from datetime import date


def getSeason():
    month = int(str(date.today())[5:7])
    month = int(month)
    if 9 <= month <= 12:
        return 'fall'
    elif 1 <= month <= 4:
        return 'spring'
    else:
        return 'summer'

def getYear():
    return int(str(date.today())[0:4])




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
                dbc.CardBody(children=[dcc.Dropdown(options=canvas.getCourses(getYear(), getSeason()),
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
                dbc.CardBody(children=[dcc.Dropdown(id="assignment-dropdown", optionHeight=120)], id="assignment-card-body"),
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
                    dcc.Input(placeholder="Enter file extensions separated by a comma", id="fileExtension-input", className='user-inputs'),
                    html.Small("Notes", id="open-file-ext-modal", className="sub-text"),
                    dbc.Modal(children=[
                        dbc.ModalHeader("Notes", className="sub-text"),
                        dbc.ModalBody(children=[
                            html.Ul(children=[
                                html.Li("Only files with specified extensions will be downloaded and run through Moss.  Example: .c,.h"),
                                html.Li("If students submitted .zip files, specify this here."),
                                html.Li("Example: \".py,.zip\".  This will download any python files, as well download any zip files and extract any python files in them")
                            ])]),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close-file-ext-model", className="ml-auto")
                        ),
                    ], id="file-ext-modal"),
                ]),
                id="collapse-5"
            ),
        ],
        className="card"
    )


def baseFiles():
    return dbc.Card(
        [
            dbc.CardHeader(
                dbc.Button("Base Files",
                           id="group-6-toggle",
                           className="sidebarbuttons"),
                className="sidebarcards"
            ),
            dbc.Collapse(
                dbc.CardBody(children=[
                    html.H6("Base Files", style={"font-weight": "bold"}, className="no-bottom-space"),
                    html.Small("What is this?", id="open-base-file-modal", className="sub-text"),
                    dbc.Modal(children=[
                        dbc.ModalHeader("What is a \"Base File?\""),
                        dbc.ModalBody(children=[
                            "A \"Base File\" contains code students are allowed to use in there assignment.  If these exist for the assignment you would like to run Moss on"
                            "enter the path here.  If there are multiple base files, enter them on separate lines"]),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close-base-file-model", className="ml-auto")
                        ),
                    ], id="base-file-modal"),
                    dcc.Textarea(
                        id='base-file-textarea',
                        placeholder="Enter the path to the Base Files separated by a comma",
                        style={'width': '100%', 'height': 300, "overflow": "auto"},
                    ),
                ]),
                id="collapse-6"
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
                    html.H6("Canvas Key", style={"font-weight": "bold"}),
                    dcc.Input(placeholder="Enter your Canvas Key", id="canvas-api-key", value=canvas.getKey(), className='user-inputs'),
                    html.Small("What is this?", id="open-canvas-key-modal", className="sub-text"),
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
                    html.H6("Semester", style={"font-weight": "bold", "margin-bottom": "4px", "margin-top": "6px"}, className="no-bottom-space"),
                    dcc.Dropdown(id="semester-season", disabled=False, options=[{"label":"Summer","value":"summer"},
                                                                                {"label":"Fall","value":"fall"},
                                                                                {"label":"Spring","value":"spring"},
                                                                                {"label":"All Semesters","value":"all"}], value=getSeason()),
                    dcc.Input(id="semester-year", type="number", value=getYear(),style={"width":"100%"}),
                    html.Small("Enter \"0\" for all years"),
                    html.Br(),
                    html.Br(),
                    html.H6("Source", style={"font-weight": "bold"}, className="no-bottom-space"),
                    html.Small("What is this?", id="open-local-model", className="sub-text"),
                    dbc.Modal(children=[
                        dbc.ModalHeader("Local or Canvas"),
                        dbc.ModalBody(children=[
                            "Specify whether you would like to run Moss on assignments on Canvas or on assignments you have already downloaded.  If you would like to "
                            "run Moss on assignments you have already downloaded, the directory on be in one of two forms.  One, a directory with sub-directories that contain"
                            "the files for each student.  If this is the case select \"By Directory\" below.  Two, a directory with all files for every student contained in that "
                            "directory.  If this is the case select \"By File\" ",
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
                        options=[{'label': 'By File', 'value': 'file', 'disabled': True}, {'label': 'By Directory', 'value': 'directory', 'disabled': True}],
                        id='directory-select',
                        value='directory'
                    ),
                    dcc.Input(placeholder="path", id="assignment-path", className='user-inputs', disabled=True, value='')
                ]),
                id="collapse-2"
            ),
        ],
        className="card"
    )
