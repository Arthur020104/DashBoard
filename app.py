import streamlit as st
from apiCalls import getDataFromPubmedApi
from googlePatents import getDataFromSerpApi
from translate import translateIfNeeded

st.set_page_config(layout="wide")

st.title("PubMed Article Data Fetcher")
searchSubject = st.text_input("Enter the subject to search for articles:", "hyperthyroidism")
yearsToSearch = st.number_input("Enter the number of years to look back:", min_value=1, max_value=20, value=5)
limitRecent = st.number_input("Enter the number of most recent articles to fetch:", min_value=1, max_value=20, value=5)

if st.button("Fetch Articles"):
    with st.spinner("Fetching articles..."):
        searchSubject = translateIfNeeded(searchSubject)
        pubMedResponseData = getDataFromPubmedApi(searchSubject, rangeYears=yearsToSearch, mostRecentLimit=limitRecent)
        googlePatentsResponseData = getDataFromSerpApi(searchSubject, rangeYears=yearsToSearch, mostRecentLimit=limitRecent)
        
    st.success("Articles fetched successfully!")
    st.subheader("Final Result")
    
    articlePlotData = pubMedResponseData.get('plotData', {})
    articlePlotData.pop('total', None)  # Remove total from plotData for display


    googlePatentsArticlePlotData = googlePatentsResponseData.get('plotData', {})
    googlePatentsArticlePlotData.pop('total', None)  # Remove total from plotData for display
    
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("Data fetched from [PubMed](https://pubmed.ncbi.nlm.nih.gov/).")
        

        st.subheader("Article Count by Year")
        st.bar_chart(data=articlePlotData, use_container_width=True)
        
        
        st.subheader("Most Recent Articles")
        mostRecentArticles = pubMedResponseData.get('mostRecent', [])
        if mostRecentArticles:
            st.write(f"Displaying {len(mostRecentArticles)} recent articles.")
            for article in mostRecentArticles:
                st.markdown(f"**Title:** {article.get('title', 'N/A')}")
                st.markdown(f"**Authors:** {article.get('authors', 'N/A')}")
                st.markdown(f"**Journal:** {article.get('journal', 'N/A')}")
                st.markdown(f"**DOI:** {article.get('doi', 'N/A')}")
                with st.expander("Abstract"):
                    st.write(article.get('abstract', 'N/A'))
                st.markdown(f"**Published Date:** {article.get('pubDate', 'N/A')}")
                st.write("---")
        else:
            st.write("No recent articles found.")

    with col2:
        st.markdown("Data fetched from [Google Patents](https://patents.google.com/) with [SerpApi](https://serpapi.com/).")
        
        st.subheader("Patents Count by Year")
        st.bar_chart(data=googlePatentsArticlePlotData, use_container_width=True)

        st.write(f"Displaying {len(googlePatentsResponseData.get('mostRecent', []))} recent patents.")
        mostRecentPatents = googlePatentsResponseData.get('mostRecent', [])
        if mostRecentPatents:
            for patent in mostRecentPatents:
                st.markdown(f"**Title:** {patent.get('title', 'N/A')}")
                st.markdown(f"**Publication Number:** {patent.get('publicationNumber', 'N/A')}")
                st.markdown(f"**Assignee:** {patent.get('assignee', 'N/A')}")
                st.markdown(f"**Priority Date:** {patent.get('priorityDate', 'N/A')}")
                with st.expander("Snippet"):
                    st.write(patent.get('snippet', 'N/A'))
                with st.expander("Country Status/Grant Date"):
                    #countryStatus is a dict in string format, so we convert it to a dict before displaying
                    countryStatus = patent.get('countryStatus', 'N/A')
                    if isinstance(countryStatus, str) and countryStatus != 'N/A':
                        countryStatus = eval(countryStatus)
                    st.write(countryStatus)
                st.markdown(f"**Forward Citations:** {patent.get('forwardCitations', 0)}")
                st.markdown(f"**Publication Date:** {patent.get('publicationDate', 'N/A')}")
                st.markdown(f"**Patent Link:** {patent.get('patentLink', 'N/A')}")
                st.write("---")
