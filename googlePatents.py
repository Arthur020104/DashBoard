from serpapi import GoogleSearch
import os
from dotenv import load_dotenv
import datetime as dt

load_dotenv()
def getDataFromSerpApi(subject: str, rangeYears: int = 5, mostRecentLimit: int = 5) -> dict:
    data = {'plotData': {}, 'mostRecent': []}
    currentYear = dt.datetime.now().year
    startYear = currentYear - rangeYears
    result = None
    for year in range(startYear, currentYear + 1):
        result = fetchApi(subject, year, year)
        if "search_information" in result:
            data['plotData'][year] = result["search_information"].get("total_results", 0)

    data['plotData']['total'] = sum(data['plotData'].values())
   
    #get most recent patents
    #publication_number, title, assignee, priority_date, country_status/grant_date, cpc, forward_citations
    try:
        mostRecent = fetchApi(subject, currentYear, currentYear)
        if "organic_results" in mostRecent:
            for patentData in mostRecent["organic_results"]:
                patentInfo = {
                    "title": patentData.get("title", "N/A"),
                    "publicationNumber": patentData.get("publication_number", "N/A"),
                    "assignee": patentData.get("assignee", "N/A"),
                    "priorityDate": patentData.get("priority_date", "N/A"),
                    "countryStatus": patentData.get("country_status", "N/A"),
                    "forwardCitations": patentData.get("forward_citations", 0),
                    "publicationDate": dt.datetime.strptime(patentData.get("publication_date", "N/A"), "%Y-%m-%d") if patentData.get("publication_date") else "N/A",
                    "patentLink": patentData.get("patent_link", "N/A"),
                    "snippet": patentData.get("snippet", "N/A")
                }
                data['mostRecent'].append(patentInfo)
            data['mostRecent'].sort(key=lambda x: x.get('publicationDate', dt.datetime.min), reverse=True)
            
            data['mostRecent'] = data['mostRecent'][:mostRecentLimit]
    except Exception as e:
        print(f"An error occurred while fetching most recent patents: {e}")
        data['mostRecent'] = []
    
    return data
def fetchApi(query: str, rangeYearsLower: int, rangeYearsUpper: int, adicionalParams: dict = None) -> dict:
    params = {
        "engine": "google_patents",
        "q": query,
        "after": f"publication:{rangeYearsLower}0101",  
        "before": f"publication:{rangeYearsUpper}1231",  
        "api_key": os.getenv("SERPAPI_KEY")  
    }
    if adicionalParams:
        params.update(adicionalParams)
    
    search = GoogleSearch(params)
    results = search.get_dict()
    
    return results

if __name__ == "__main__":
    searchSubject = "coffee"
    yearsToSearch = 1
    limitRecent = 5

    finalData = getDataFromSerpApi(searchSubject, rangeYears=yearsToSearch, mostRecentLimit=limitRecent)
    
    print("\n--- Final Result ---")
    print(finalData['mostRecent'][0])