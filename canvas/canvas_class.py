import json
from canvasapi import Canvas
from canvasapi.exceptions import Unauthorized, InvalidAccessToken, ResourceDoesNotExist
import pandas as pd
import requests


def readKey(path):
    try:
        with open(f'{path}key.txt', 'r') as json_file:
            data = json.load(json_file)
            return data['key']
    except FileNotFoundError:
        return ""


def auth(path, API_KEY):
    API_URL = "https://canvas.sfu.ca/"
    canvasObject = Canvas(API_URL, API_KEY)
    return canvasObject


class canvas:
    def __init__(self):
        self.__path = 'canvas/'
        self.__key = readKey(self.__path)
        self.__canvas = auth(self.__path, self.__key)

    # Writes the to key.txt. Will create file if not there
    def __writeKey(self):
        data = {"key": self.__key}
        with open('canvas/key.txt', 'w') as outfile:
            json.dump(data, outfile)

    # Returns the key to user
    def getKey(self):
        return self.__key

    # Used to get data for each submission for an assignment.  Called by getSubmissions
    def __submissionData(self, courseNumber, assignmentNumber, canvasID, fileExtensions):
        # Getting the assignment submission for the student by canvasID (using the Canvas API directly, not python overlay)
        urlString = f"https://canvas.sfu.ca/api/v1/courses/{courseNumber}/assignments/{assignmentNumber}/" \
                    f"submissions/{canvasID}?access_token={self.getKey()}"
        url = requests.get(urlString)
        urlData = url.json()

        # Creating a list to store submission data
        studentSubmissions = []

        # Iterating through every file associated with each students respective assignment submission
        try:
            for attachment in urlData['attachments']:
                # Testing if the file is included in the file extensions
                skip = True
                ext = ''
                for extension in fileExtensions:
                    extensionLength = len(extension)
                    if attachment['display_name'][-extensionLength:] == extension:
                        skip = False
                        ext = extension
                        break
                if skip:
                    continue

                # If the file has the appropriate file extension, add it to list
                studentSubmissions.append({'canvasID': urlData['user_id'], 'fileName': attachment['display_name'], 'extension': ext, 'downloadURL': attachment['url']})
        except KeyError:
            # Handling the case where a student submitted nothing (printing it out for logging purposes)
            print("Canvas User: ", canvasID, ", did not submit the assignment")

        # Just returning studentSubmission data, NOTE: it doesn't matter of its empty, will be dropped when added to dataframe
        return studentSubmissions

    # Used to get the students in a course.  Called by getSubmissions
    def __students(self, courseNumber, course):
        # Getting the course users
        users = course.get_users(enrollment_type=['student'], enrollment_state=['active', 'invited'])
        data = []
        for user in users:
            data.append([user.name, user.id])
        studentData = pd.DataFrame(data, columns=['name', 'canvasID'])
        return studentData

    # Excepts new key from user, and changes the key
    def changeKey(self, newKey):
        # Changing key to the new key
        self.__key = newKey

        # Writing it to the file
        self.__writeKey()

        # Authenticating with the new key
        self.__canvas = auth(self.__path, self.__key)

    # Method that queries the API to get a list of the users courses from Canvas
    def getCourses(self):
        # Getting the canvas object
        canvasObject = self.__canvas

        # Querying the courses
        courses = canvasObject.get_courses()
        courseData = []
        try:
            for course in courses:
                try:
                    courseData.append({"label": course.name, "value": course.id})
                except AttributeError:
                    continue
            return courseData
        except InvalidAccessToken:
            return [{"label": "No Canvas Key or Invalid Canvas Key Detected", "value": "Error"}]

    # Getting the assignment names
    def getAssignments(self, courseNumber):
        # Getting the canvas object
        canvasObject = self.__canvas
        try:
            course = canvasObject.get_course(courseNumber)
        except InvalidAccessToken:
            return [{"label": "No Canvas Key or Invalid Canvas Key Detected", "value": "Error"}]
        except Unauthorized:
            return [{"label": "No Course Selected", "value": "Error"}]
        except ResourceDoesNotExist:
            return [{"label": "No Course Selected", "value": "Error"}]
        except TypeError:
            return [{"label": "No Course Selected", "value": "Error"}]

        assignments = course.get_assignments()
        assignmentList = [{"label": i.name, "value": i.id} for i in assignments]
        return assignmentList

    def getSubmissions(self, courseNumber, assignmentNumber, language, fileExtensions):
        # Error handling if no options have been selected or there is a bad canvas key
        if courseNumber is None or assignmentNumber is None or language is None or fileExtensions is None:
            errorData = pd.DataFrame(data={"Error": ['At least one of Course, Assignment, Language, or File Extension has not been selected']})
            if courseNumber == 'Error' or assignmentNumber == 'Error':
                errorData = errorData.append({'Error': "No Canvas Key or Invalid Canvas Key Detected"}, ignore_index=True)
            return errorData

        # Error handling if there is a bad canvas key
        if courseNumber == 'Error' or assignmentNumber == 'Error':
            return pd.DataFrame(data={"Error": ["No Canvas Key or Invalid Canvas Key Detected"]})

        # Getting canvas object
        canvasObject = self.__canvas

        # Getting the course
        course = canvasObject.get_course(courseNumber)

        # Getting the assignment from the course
        # NOTE: The error handler is for when user has selected when course & assignment, and then changes courses, Dash will still call this function with the
        # previous assignmentNumber that does not exist for the newly selected course.
        fileExtensionsList = fileExtensions.split(',')

        try:
            assignment = course.get_assignment(assignmentNumber)
        except ResourceDoesNotExist:
            return pd.DataFrame(data={"Error": ['At least one of Course, Assignment or Language has not been selected']})

        # Getting all of the the submissions
        submissions = assignment.get_submissions()

        # Creating an empty data frame to hold the submission data
        studentsSubmissions = pd.DataFrame(columns=['canvasID', 'fileName', 'extension', 'downloadURL'])

        # Iterating through each submission to get each submissions data
        for submission in submissions:
            studentsSubmissions = studentsSubmissions.append(self.__submissionData(courseNumber,
                                                                                   assignmentNumber,
                                                                                   submission.user_id,
                                                                                   fileExtensionsList),
                                                             ignore_index=True)

        # Getting the names and canvas IDs of all the students in the course
        studentNames = self.__students(courseNumber, course)

        # Doing a right join between the course students and the submissions (if an instructor submitted assignment for student it will be included with no name)
        data = pd.merge(left=studentNames, right=studentsSubmissions, how='right', left_on='canvasID', right_on='canvasID')
        return data
