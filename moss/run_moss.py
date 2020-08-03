import os
from pathlib import Path


def mossCanvas(data, language, extensions):
    print("In Moss")
    wd = os.getcwd()
    os.chdir('moss')
    students = [i['name'].replace(" ", "_").replace("-", "") for i in data]
    print(students)

    # command = f"perl moss.pl -l {language} -d "
    # entries = Path(directory[5:])
    # for fileName in os.listdir(entries):
    #     if fileName not in students:
    #         continue
    #     for extension in extensions.split(','):
    #         if extension == '.zip':
    #             continue
    #         command = command + f'{directory[5:]}/{fileName}/*' + extension + " "
    # os.system(command)
    # os.chdir(wd)
