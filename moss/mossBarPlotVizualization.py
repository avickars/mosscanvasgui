from bs4 import BeautifulSoup
import pandas as pd
import codecs
import plotly.graph_objects as go
import statistics as stat


def sections(arg):
    if arg > 80:
        return '80%'
    elif 80 >= arg > 60:
        return '60% - 80%'
    elif 60 >= arg > 45:
        return '45% - 60%'
    elif 45 >= arg > 30:
        return '30% - 45%'
    elif 30 >= arg > 15:
        return '15% - 30%'
    else:
        return '0% - 15%'


def mossBarPlot(reportLocation, barplotDestination, courseName, assignmentName):
    print("Loc: ", reportLocation)
    print("Dest: ", barplotDestination)
    # Getting Moss html report
    htmlFile = codecs.open(reportLocation, 'r')

    # Setting the destination of the report
    destination = barplotDestination
    if courseName == '' or assignmentName =='':
        plotTitle = 'Moss Distribution'
    else:
        plotTitle = f'{courseName} -- {assignmentName} -- Moss Distribution'

    fileName = "mossBarplot.html"

    # Reading html into a beautiful soup object
    soup = BeautifulSoup(htmlFile.read(), features="lxml")

    # Finding the table rows
    dataHTML = soup.find('table').find_all('tr')

    # Creating the dataframe to score the information
    data = pd.DataFrame(columns=["student1", "student1_percent", "student2", "student2_percent", "numLines"])

    # Scraping the report
    for dataIndv in dataHTML:
        dataByLine = dataIndv.find_all('a')
        numLines = dataIndv.find_all('td', {'align': 'right'})
        # Testing for an empty list
        if not dataByLine:
            continue
        s1 = dataByLine[0].contents[0]
        s2 = dataByLine[1].contents[0]
        newData = {"student1": s1[0:s1.find('(')],
                   "student1_percent": int(s1[s1.find('(') + 1:s1.find('%')]),
                   "student2": s2[0:s2.find('(')],
                   "student2_percent": int(s2[s2.find('(') + 1:s2.find('%')]),
                   "numLines": int(numLines[0].contents[0])}
        data = data.append(newData, ignore_index=True)

    data['mean'] = data.apply(lambda row: stat.mean([row['student1_percent'], row['student2_percent']]), axis=1)

    data['group'] = data.apply(lambda row: sections(row['mean']), axis=1)

    dataByGroup = data.groupby('group', as_index=False).size().reset_index()
    if plotTitle == "":
        plotTitle = "Moss Assignment Similarity Breakdown"

    fig = go.Figure(go.Bar(
        x=dataByGroup['group'],
        y=dataByGroup['size'],
        text=dataByGroup['group'],
        hovertemplate='<b> %{text}</b> <br> Count: %{y} <extra></extra>',
        marker_color="darkred"
    ))

    fig.update_layout(
        xaxis=dict(
            title="Assignment Similarity"
        ),
        yaxis=dict(
            title="Count"
        ),
        title=plotTitle
    )

    fig.write_html(destination + fileName)