import streamlit as st
import asyncio
from manager import Manager
from translate import translateIfNeeded


if 'manager' not in st.session_state:
    st.session_state.manager = Manager()

manager = st.session_state.manager

st.set_page_config(layout="wide")

st.title("Jornada Mastera")
searchSubject = st.text_input("Digite o assunto para pesquisar artigos e patentes:", "hyperthyroidism")
yearsToSearch = st.number_input("Digite o número de anos para pesquisar:", min_value=1, max_value=20, value=5)
limitRecent = st.number_input("Digite o número de artigos e patentes mais recentes para buscar:", min_value=1, max_value=20, value=5)
if st.button("Buscar Artigos e Patentes"):
    with st.spinner("Buscando dados..."):
        searchSubject = asyncio.run(translateIfNeeded(searchSubject))
        print(f"Searching for: {searchSubject}")
        pubMedResponseData = manager.getDataFromPubmed(searchSubject, rangeYears=yearsToSearch, mostRecentLimit=limitRecent)
        pubMedResponseData = manager.getDataFromPubmed(searchSubject, rangeYears=yearsToSearch, mostRecentLimit=limitRecent)
        googlePatentsResponseData = manager.getDataFromSerp(searchSubject, rangeYears=yearsToSearch, mostRecentLimit=limitRecent)
        
    st.success("Busca concluída com sucesso!")
    st.subheader("Resultado Final")
    
    articlePlotData = pubMedResponseData.get('plotData', {})
    articlePlotData.pop('total', None)  # Remove total from plotData for display


    googlePatentsArticlePlotData = googlePatentsResponseData.get('plotData', {})
    googlePatentsArticlePlotData.pop('total', None)  # Remove total from plotData for display
    
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("Dados buscados do [PubMed](https://pubmed.ncbi.nlm.nih.gov/).")
        

        st.subheader("Contagem de Artigos por Ano")
        st.markdown("**Nota:** Se o gráfico não aparecer, clique na área do gráfico para exibi-lo.")
        st.bar_chart(data=articlePlotData, use_container_width=True)
        
        
        st.subheader("Artigos Mais Recentes")
        mostRecentArticles = pubMedResponseData.get('mostRecent', [])
        if mostRecentArticles:
            st.write(f"Exibindo {len(mostRecentArticles)} artigos recentes.")
            for article in mostRecentArticles:
                st.markdown(f"**Título:** {article.get('title', 'N/A')}")
                st.markdown(f"**Autores:** {article.get('authors', 'N/A')}")
                st.markdown(f"**Revista:** {article.get('journal', 'N/A')}")
                st.markdown(f"**DOI:** {article.get('doi', 'N/A')}")
                with st.expander("Resumo"):
                    st.write(article.get('abstract', 'N/A'))
                st.markdown(f"**Data de Publicação:** {article.get('pubDate', 'N/A')}")
                st.write("---")
        else:
            st.write("Nenhum artigo recente encontrado.")

    with col2:
        st.markdown("Dados buscados do [Google Patents](https://patents.google.com/) com [SerpApi](https://serpapi.com/).")
        
        st.subheader("Contagem de Patentes por Ano")
        st.bar_chart(data=googlePatentsArticlePlotData, use_container_width=True)

        st.write(f"Exibindo {len(googlePatentsResponseData.get('mostRecent', []))} patentes recentes.")
        mostRecentPatents = googlePatentsResponseData.get('mostRecent', [])
        if mostRecentPatents:
            for patent in mostRecentPatents:
                st.markdown(f"**Título:** {patent.get('title', 'N/A')}")
                st.markdown(f"**Número de Publicação:** {patent.get('publicationNumber', 'N/A')}")
                st.markdown(f"**Cessionário:** {patent.get('assignee', 'N/A')}")
                st.markdown(f"**Data de Prioridade:** {patent.get('priorityDate', 'N/A')}")
                with st.expander("Fragmento"):
                    st.write(patent.get('snippet', 'N/A'))
                with st.expander("Status por País/Data de Concessão"):
                    #countryStatus is a dict in string format, so we convert it to a dict before displaying
                    countryStatus = patent.get('countryStatus', 'N/A')
                    if isinstance(countryStatus, str) and countryStatus != 'N/A':
                        countryStatus = eval(countryStatus)
                    st.write(countryStatus)
                st.markdown(f"**Citações Anteriores:** {patent.get('forwardCitations', 0)}")
                st.markdown(f"**Data de Publicação:** {patent.get('publicationDate', 'N/A')}")
                st.markdown(f"**Link da Patente:** {patent.get('patentLink', 'N/A')}")
                st.write("---")
