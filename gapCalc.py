import numpy as np
import datetime as dt

def calculateGapScore(articlesByYear: dict, patentsByYear: dict) -> float:
    # if the current year is not in december, we assume the data is number of articles and patents 
    #will keep up in the same pace, so we do a mean totalOfThisYear/totalMonths * 12
    currentDate = dt.datetime.now()
    if currentDate.month != 12:
        #if we are before day 15, we assume the data is not complete, so we subtract one month
        if currentDate.day < 15:
            currentDate -= dt.timedelta(months=1)
        currentYear = currentDate.year
        
        if currentYear in articlesByYear:
            articlesByYear[currentYear] = int(articlesByYear[currentYear] * (12 / currentDate.month))
        if currentYear in patentsByYear:
            patentsByYear[currentYear] = int(patentsByYear[currentYear] * (12 / currentDate.month))
    # if there are no articles or patents, we return 0
    if not articlesByYear:
        return 0

    #linear regression to get yearly growth in percentage
    def getSlope(dataByYear: dict) -> float:
        if not dataByYear or len(dataByYear) < 2:
            return 0.0
        
        sortedData = sorted(dataByYear.items())
        years = np.array([item[0] for item in sortedData])
        counts = np.array([item[1] for item in sortedData])


        # We add a small epsilon to the denominator to avoid division by zero
        epsilon = 1e-9
        percentageGrowth = (np.diff(counts) / (counts[:-1] + epsilon))
        
        # If we don't have enough data points for growth calculation, return 0
        if len(percentageGrowth) < 1:
            return 0.0
        growthYears = years[1:]

        # If there's only one growth data point, that is our slope (average growth)
        if len(growthYears) < 2:
            return percentageGrowth[0]

        # We calculate the slope of the percentage growth over the years
        slope = np.polyfit(growthYears, percentageGrowth, 1)[0]
        return slope

    articlesSlope = getSlope(articlesByYear)
    patentsSlope = getSlope(patentsByYear)
    print(f"Articles Slope: {articlesSlope}, Patents Slope: {patentsSlope}")

  
    factor = articlesSlope * (1- patentsSlope)
    
    if articlesSlope < 0 and patentsSlope < 0:
        factor = (1- articlesSlope) * (1- patentsSlope)


    #normalize data between -1 and 4
    finalScore = (factor + 1)/ 5
    print(f"Gap Score: {factor}, Final Score: {finalScore}")
    return finalScore
