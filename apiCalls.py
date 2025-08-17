import requests
import datetime as dt
from xml.etree import ElementTree
import time

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def articleToDict(articleXml) -> dict:

    def getText(element, path):
        found = element.find(path)
        return found.text if found is not None else 'N/A'

    # Extract basic info
    title = getText(articleXml, ".//ArticleTitle")
    journal = getText(articleXml, ".//ISOAbbreviation")
    doi = getText(articleXml, ".//ArticleId[@IdType='doi']")
    abstractElement = articleXml.find(".//AbstractText")
    abstract = abstractElement.text if abstractElement is not None else 'N/A'

    # Extract publication date
    pubDate = None
    pubDateElement = articleXml.find(".//PubDate")
    if pubDateElement is not None:
        try:
            yearText = getText(pubDateElement, "Year")
            monthText = getText(pubDateElement, "Month")
            dayText = getText(pubDateElement, "Day")
            
            year = int(yearText) if yearText != 'N/A' else None
            
            # Month generally comes as a string, but if comes as number we handle it
            if monthText != 'N/A':
                try:
                    month = dt.datetime.strptime(monthText, "%b").month
                except ValueError:
                    try:
                        month = int(monthText)
                    except ValueError:
                        month = None
            
            day = int(dayText) if dayText != 'N/A' else 1
            
            if year and month:
                pubDate = dt.date(year, month, day)
        except (ValueError, TypeError):
            pubDate = None

    # Extract authors
    authorsList = []
    authorElements = articleXml.findall(".//Author")
    for author in authorElements:
        lastName = getText(author, "LastName")
        firstName = getText(author, "ForeName")
        if lastName:
            authorsList.append(f"{lastName} {firstName}")
    authorsStr = ', '.join(authorsList) if authorsList else 'N/A'


    return {'title': title, 'authors': authorsStr, 'pubDate': pubDate, 'journal': journal, 'doi': doi, 'abstract': abstract}

def getDataFromPubmedApi(subject: str, rangeYears: int = 5, mostRecentLimit: int = 5) -> dict:
    data = {'plotData': {}, 'mostRecent': []}
    currentYear = dt.datetime.now().year
    startYear = currentYear - rangeYears

    #get the count of articles for each year in the range
    for year in range(startYear, currentYear + 1):
        try:
            query = f'({subject}) AND ("{year}"[pdat])'
            
            params = {"db": "pubmed", "term": query, "rettype": "count"}
            
            tree = fetchApi(f"{BASE_URL}esearch.fcgi", params)
            count = int(tree.find("Count").text)
            data['plotData'][year] = count
            
            time.sleep(0.4) 

        except Exception as e:
            print(f"An error occurred while fetching article count for {year}: {e}")
            data['plotData'][year] = 0
    
    data['plotData']['total'] = sum(data['plotData'].values())

    #Get the most recent articles
    if mostRecentLimit > 0:
        try:
            # Get the Ids of the most recent articles
            fullRangeQuery = f'({subject})'
            
            esearchParams = {"db": "pubmed", "term": fullRangeQuery, "sort": "pub date", "retmax": mostRecentLimit}

            
            esearchTree = fetchApi(f"{BASE_URL}esearch.fcgi", esearchParams)
            idList = [elem.text for elem in esearchTree.findall(".//Id")]

            if not idList:
                return data

            # fetch all article data for the Ids
            articles = fetchArticlesWithId(idList)
            data['mostRecent'] = articles
            

        except Exception as e:
            print(f"An error occurred while fetching recent articles: {e}")
            data['mostRecent'] = []

    return data

def fetchApi(url: str, params: dict) -> ElementTree.Element:
    response = requests.get(url, params=params)
    response.raise_for_status()
    return ElementTree.fromstring(response.content)

    
def fetchArticlesWithId(idList: list) -> list:
    articles = []
    if not idList:
        return articles

    try:
        efetchParams = {"db": "pubmed", "id": ",".join(idList), "retmode": "xml"}
        efetchTree = fetchApi(f"{BASE_URL}efetch.fcgi", efetchParams)
        
        articlesXml = efetchTree.findall(".//PubmedArticle")
        for articleXml in articlesXml:
            articles.append(articleToDict(articleXml))
        
    except (requests.exceptions.RequestException, ElementTree.ParseError, AttributeError):
        return []

    return articles
if __name__ == "__main__":
    searchSubject = "crispr gene editing"
    yearsToSearch = 2
    limitRecent = 5

    finalData = getDataFromPubmedApi(searchSubject, rangeYears=yearsToSearch, mostRecentLimit=limitRecent)
    
    print("\n--- Final Result ---")
    print(finalData)
