from googlePatents import getDataFromSerpApi
from apiCalls import getDataFromPubmedApi
from db import Database
from gapCalc import calculateGapScore
from gemini import callModel

class Manager:
    def __init__(self):
        self._db = Database()
        self._session = None
        with self._db.connect() as connection:
            #self._db.connect()
            result = self._db.executeQuery("INSERT INTO session (started) VALUES (NOW()) RETURNING id")
            if result and len(result) > 0:
                self._session = result[0][0]
            else:
                raise Exception("Failed to create a new session in the database.")
            
            self._db.close(connection)
        print(f"Session started with ID: {self._session}")

    def getSessionId(self):
        return self._session
    
    def getDataFromSerp(self, subject: str, rangeYears: int = 5, mostRecentLimit: int = 5) -> dict:
        inputDict = {
            "subject": subject,
            "rangeYears": rangeYears,
            "mostRecentLimit": mostRecentLimit
        }
        inputStr = str(inputDict).replace("'", '"')
        try:
            data = getDataFromSerpApi(subject, rangeYears, mostRecentLimit)
            dataStr = str(data).replace("'", '"') 
            with self._db.connect() as connection:
                self._db.executeQuery(f"INSERT INTO action (sessionId, action, inputs, result, time) VALUES ({self._session}, 'getDataFromSerpApi', '{inputStr}', '{dataStr}', NOW())")
                self._db.close(connection)
            return data
        except Exception as e:
            print(f"An error occurred while fetching data from SerpApi: {e}")
            with self._db.connect() as connection:
                self._db.executeQuery(f"INSERT INTO action (sessionId, action, inputs, result, time) VALUES ({self._session}, 'getDataFromSerpApi', '{inputStr}', 'error: {e}', NOW())")
                self._db.close(connection)
            data = {}

    def getDataFromPubmed(self, subject: str, rangeYears: int = 5, mostRecentLimit: int = 5) -> dict:
        inputDict = {
            "subject": subject,
            "rangeYears": rangeYears,
            "mostRecentLimit": mostRecentLimit
        }
        inputStr = str(inputDict).replace("'", '"')
        try:
            data = getDataFromPubmedApi(subject, rangeYears, mostRecentLimit)
            dataStr = str(data).replace("'", '"') 
            with self._db.connect() as connection:
                self._db.executeQuery(f"INSERT INTO action (sessionId, action, inputs, result, time) VALUES ({self._session}, 'getDataFromPubmedApi', '{inputStr}', '{dataStr}', NOW())")
                self._db.close(connection)
            return data
        except Exception as e:
            print(f"An error occurred while fetching data from PubMed API: {e}")
            with self._db.connect() as connection:
                self._db.executeQuery(f"INSERT INTO action (sessionId, action, inputs, result, time) VALUES ({self._session}, 'getDataFromPubmedApi', '{inputStr}', 'error: {e}', NOW())")
                self._db.close(connection)
            data = {}
    def calculateGapScore(self, articlesByYear: dict, patentsByYear: dict) -> dict:
        inputDict = {
            "articlesByYear": articlesByYear,
            "patentsByYear": patentsByYear
        }
        inputStr = str(inputDict).replace("'", '"')
        try:
            gapScore = calculateGapScore(articlesByYear, patentsByYear)
            gapScoreStr = str(gapScore)
            with self._db.connect() as connection:
                self._db.executeQuery(f"INSERT INTO action (sessionId, action, inputs, result, time) VALUES ({self._session}, 'gapCalc', '{inputStr}', '{gapScoreStr}', NOW())")
                self._db.close(connection)
            return gapScore
        except Exception as e:
            print(f"An error occurred while calculating the gap score: {e}")
            with self._db.connect() as connection:
                self._db.executeQuery(f"INSERT INTO action (sessionId, action, inputs, result, time) VALUES ({self._session}, 'gapCalc', '{inputStr}', 'error: {e}', NOW())")
                self._db.close(connection)
            return -1
    def getModelResponse(self, data: str) -> str:
        inputDict = {
            "data": data
        }
        inputStr = str(inputDict).replace("'", '"')
        try:
            response = callModel(data).text.strip()
            responseStr = str(response)
            with self._db.connect() as connection:
                self._db.executeQuery(f"INSERT INTO action (sessionId, action, inputs, result, time) VALUES ({self._session}, 'getModelResponse', '{inputStr}', '{responseStr}', NOW())")
                self._db.close(connection)
            return response
        except Exception as e:
            print(f"An error occurred while calling the model: {e}")
            with self._db.connect() as connection:
                self._db.executeQuery(f"INSERT INTO action (sessionId, action, inputs, result, time) VALUES ({self._session}, 'getModelResponse', '{inputStr}', 'error: {e}', NOW())")
                self._db.close(connection)
            return ""