import pandas as pd
import os


def directoryTraveller(path, data):
    for file in os.listdir(path):
        if os.path.isdir(path + f'/{file}'):
            directoryTraveller(path + f'/{file}', destination)
            shutil.rmtree(location + f'/{file}')
        else:
            try:
                shutil.move(location + f'/{file}', destination)
            except shutil.Error:
                print("Unable to move file")


class local:
    def __int__(self):
        self.path = None

    def changePath(self, newPath):
        self.path = newPath

    def getSubmissions(self, extensions, language):
        if extensions is None or language is None or self.path is None:
            return pd.DataFrame(data=[{"Error": 'At least one of Language or File Extension has not been selected'}])

        path = self.path
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


# localObject = local()
# localObject.changePath('/home/aidan/Downloads/testFile')
# #
# localObject.getSubmissions('.py,.zip,.txt', '')
