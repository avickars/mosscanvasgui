import pandas as pd
import os
import shutil
import codecs
from bs4 import BeautifulSoup

from canvas.canvas_class import findSubString, createDirectory, copyDirectory, exists
from moss.mossBarPlotVizualization import mossBarPlot


# This function moves a index.html  (i.e. a moss report), and copies it and all its dependencies to the destination. It also rewrites it a bit to make the output easier to read.
def moveMoss(destination):
    # Copying the moss results
    copyDirectory('html', 'html', destination)

    # Copying the bitmaps
    copyDirectory('bitmaps', 'bitmaps', destination)

    # Copying the general file
    copyDirectory('general', 'general', destination)

    htmlFile = codecs.open(destination + '/html/index.html', 'r')

    # path change
    path = 'html'

    # Reading html into a beautiful soup object
    soup = BeautifulSoup(htmlFile.read(), features="lxml")

    # Extracting the number of lines matched in each comparison
    numLinesMatched = soup.find('table').find_all('td', {'align': 'right'})

    # Extracting each file compared by line
    subReportUrls = soup.find('table').find_all('a')

    reportHTMLTop = f"""
    <!DOCTYPE html>
    <html>
    	<head>
    		<title> Moss Results </title>
    	</head>

    	<body>
    		Moss Results
    		<hr>
    			<a href="general/format.html" target="_top"> How to Read the Results</a>
    			<a href="general/tips.html" target="_top"> Tips</a>
    			<a href="general/faq.html"> FAQ</a>
    			<a href="mailto:aikens@similix.com">Contact</a>
    			<a href="general/scripts.html">Submission Scripts</a>
    			<a href="general/credits.html" target="_top"> Credits</a>
    		<hr>
    		<table>
    			<tbody>
    				<tr>
    					<th>File 1</th>
    					<th>File 2</th>
    					<th>Lines Matched</th>
    				</tr>
    """

    reportHTMLBottom = """
    			</tbody>
    		</table>
    	</body>
    </html>
    """

    for i in range(0, len(subReportUrls), 2):
        nameLeft = subReportUrls[i].contents[0]
        nameLeftAttr = subReportUrls[i].attrs['href']
        leftLocation = path + "/" + nameLeftAttr

        nameRight = subReportUrls[i + 1].contents[0]
        nameRightAttr = subReportUrls[i + 1].attrs['href']
        rightLocation = path + "/" + nameRightAttr

        linesMatched = numLinesMatched[int(i / 2)].contents[0]

        newNameLeft = nameLeft[6:]
        newNameRight = nameRight[6:]

        # newNameLeft = nameLeft[findSubString('/', nameLeft)[-2] + 1:]
        # newNameRight = nameRight[findSubString('/', nameRight)[-2] + 1:]

        reportHTMLTop = reportHTMLTop + f"""<tr><td> <a href={leftLocation}> {newNameLeft} </a> </td>""" + f"""<td> <a href={rightLocation}> {newNameRight} </a> </td>""" + f"""<td align=\"right\">{linesMatched}</td> </tr>"""

    reportHTMLTop = reportHTMLTop + reportHTMLBottom
    mossReport = open(destination + '/mossReport.html', 'wb')
    mossReport.write(reportHTMLTop.encode())
    mossReport.close()


class local:
    def __int__(self):
        self.path = None

    def changePath(self, newPath):
        self.path = newPath

    def getSubmissions(self, extensions, language):
        if extensions is None or language is None or self.path is None:
            return pd.DataFrame(data=[{"Error": 'At least one of Language or File Extension has not been selected'}])

        path = self.path
        forwardSlashLocations = findSubString('/', path)
        fileExtensionsList = extensions.split(',')
        data = pd.DataFrame(columns=['Location', 'fileName'])
        try:
            for file in os.listdir(path):
                try:
                    if os.path.isdir(path + f'/{file}'):
                        for subFile in os.listdir(path + f'/{file}'):
                            if any(subFile.endswith(i) for i in fileExtensionsList):
                                data = data.append({'Location': path + f"/{file}", 'fileName': subFile}, ignore_index=True)
                    else:
                        if any(file.endswith(i) for i in fileExtensionsList):
                            data = data.append({'Location': path, 'fileName': file}, ignore_index=True)
                except TypeError:
                    return pd.DataFrame(data={"Error": 'Invalid Path'})
        except FileNotFoundError:
            return pd.DataFrame(data={"Error": ['Invalid Path']})
        return data

    def moss(self, data, directoryOrFile, languageValue, fileExtensionValue):
        extensions = fileExtensionValue.split(',')

        # Recording the current working directory, it is needed at the bottom
        wd = os.getcwd()

        # Changing the current working directory to moss/
        os.chdir('moss')

        # Deleting Files to make sure we start fresh
        try:
            shutil.rmtree('Files')
        except FileNotFoundError:
            print("Already deleted \"Files\", no worries")

        # Creating the directory
        createDirectory('Files')

        # Iterating through the selected data and copying them over
        for row in data:
            forwardSashes = findSubString('/', row['Location'])
            if directoryOrFile == 'directory':
                createDirectory(f'Files/{row["Location"][forwardSashes[-1] + 1:]}')
                shutil.copy(f'{row["Location"]}/{row["fileName"]}', f'Files/{row["Location"][forwardSashes[-1] + 1:]}')
            else:
                shutil.copy(f'{row["Location"]}/{row["fileName"]}', f'Files')

        if directoryOrFile == 'directory':
            # Setting the command to run moss
            command = f"perl moss.pl -l {languageValue} -d "
            for fileName in os.listdir('Files'):
                for extension in extensions:
                    if exists(f'Files/{fileName}/', extension):
                        command = command + f'Files/{fileName}/*{extension} '
            os.system(command)
        else:
            for extension in extensions:
                command = f"perl moss.pl -l {languageValue} Files/*{extension}"
            os.system(command)

        moveMoss(self.path)

        # Deleting Files to make sure we start fresh
        try:
            shutil.rmtree('Files')
        except FileNotFoundError:
            print("Already deleted \"Files\", no worries")

        mossBarPlot(f'{self.path}/mossReport.html', f'{self.path}/', '', '')

        os.chdir(wd)
