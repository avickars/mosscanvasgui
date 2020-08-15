import sys
from bs4 import BeautifulSoup
import pandas as pd
import codecs
import plotly.graph_objects as go
import statistics as stat
import plotly.express as px

def sections(arg):
    if arg>80:
        return '80%'
    elif arg<=80 and arg>60:
        return '60% - 80%'
    elif arg<=60 and arg>45:
        return '45% - 60%'
    elif arg<=45 and arg>30:
        return '30% - 45%'
    elif arg <=30 and arg>15:
        return '15% - 30%'
    else:
        return '0% - 15%'


# Getting Moss html report
htmlFile = codecs.open("/home/aidan/Documents/SFU Summer 2020 Co-op/DianaWork/0C120-more CW assigs_MOSS/all_submissions_74/Question_5270/mossReport.html", 'r')

# Setting the destination of the report
destination = "/home/aidan/Documents/SFU Summer 2020 Co-op/DianaWork/0C120-more CW assigs_MOSS/all_submissions_74/Question_5270/"

plotTitle = "All Questions"

fileName = "Submissions_Scatterplot.html"

# Reading html into a beautiful soup object
soup = BeautifulSoup(htmlFile.read(), features="lxml")

# Finding the table rows
dataHTML = soup.find('table').find_all('tr')

# Creating the dataframe to score the information
data = pd.DataFrame(columns=["student1","student1_percent","student2","student2_percent","numLines"])

# Scraping the report
for dataIndv in dataHTML:
    dataByLine = dataIndv.find_all('a')
    numLines = dataIndv.find_all('td', {'align': 'right'})
    # Testing for an empty list
    if not dataByLine:
        continue
    s1 = dataByLine[0].contents[0]
    s2 = dataByLine[1].contents[0]
    newData = {"student1":s1[0:s1.find('(')],
               "student1_percent":int(s1[s1.find('(')+1:s1.find('%')]),
               "student2":s2[0:s2.find('(')],
               "student2_percent":int(s2[s2.find('(')+1:s2.find('%')]),
               "numLines":int(numLines[0].contents[0])}
    data = data.append(newData,ignore_index=True)

if plotTitle == "":
    plotTitle = "Moss Assignment Similarity Breakdown"

fig = go.Figure(go.Scatter(
    x = data["student1_percent"],
    y = data["student2_percent"],
    mode = 'markers',
    hovertemplate = 'Student 1: %{x}% <br> Student 2: %{y}% <extra></extra>',
    marker_color = 'darkred',
    name = "Student v. Student"
))

df1 = data['student1'].str.contains('chegg')
df1 = df1.to_frame()

df2 = data['student1'].str.contains('chegg')
df2 = df2.to_frame()
dataBool = df1.merge(data['student2'].str.contains('chegg'), left_index=True, right_index=True)

# Extracting rows that conatain a chegg solution
dataChegg = pd.concat([data[data['student1'].str.contains('chegg')], data[data['student2'].str.contains('chegg')]])

# Removing duplicates
dataChegg = dataChegg.drop_duplicates()

fig.add_trace(go.Scatter(
    x = dataChegg["student1_percent"],
    y = dataChegg["student2_percent"],
    mode = 'markers',
    marker_color = 'orange',
    hovertemplate = 'Student 1: %{x}% <br> Chegg: %{y}% <extra></extra>',
    name = "Chegg v. Student"
    )
)



fig.update_layout(
    xaxis = dict(
        title = "Student 1 (Similarity Percentage)"
    ),
    yaxis = dict(
        title = "Student 2 (Similarity Percentage)"
    ),
    title = plotTitle
)
fig.write_html(destination + fileName)
