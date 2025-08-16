import streamlit as st
from apiCalls import getDataFromPubmedApi

st.set_page_config(layout="wide")

st.title("PubMed Article Data Fetcher")
searchSubject = st.text_input("Enter the subject to search for articles:", "cancer")
yearsToSearch = st.number_input("Enter the number of years to look back:", min_value=1, max_value=20, value=5)
limitRecent = st.number_input("Enter the number of most recent articles to fetch:", min_value=1, max_value=20, value=5)

if st.button("Fetch Articles"):
    with st.spinner("Fetching articles..."):
        finalData = getDataFromPubmedApi(searchSubject, rangeYears=yearsToSearch, mostRecentLimit=limitRecent)
    st.success("Articles fetched successfully!")
    st.subheader("Final Result")
    plotData = finalData.get('plotData', {})
    plotData.pop('total', None)  # Remove total from plotData for display
    
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("Data fetched from [PubMed](https://pubmed.ncbi.nlm.nih.gov/).")
        
        st.subheader("Article Count by Year")
        st.bar_chart(data=plotData, use_container_width=True)
        
        
        st.subheader("Most Recent Articles")
        most_recent_articles = finalData.get('mostRecent', [])
        if most_recent_articles:
            st.write(f"Displaying {len(most_recent_articles)} recent articles.")
            for article in most_recent_articles:
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
        st.markdown("Data fetched from [PubMed](https://pubmed.ncbi.nlm.nih.gov/).")
        
        st.subheader("Article Count by Year")
        st.bar_chart(data=plotData, use_container_width=True)
        
        st.subheader("Raw Data")
        st.json(finalData)

