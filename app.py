import streamlit as st
import asyncio
from manager import Manager
from translate import translateIfNeeded


if 'manager' not in st.session_state:
    print("Creating new Manager instance")
    st.session_state.manager = Manager()

manager = st.session_state.manager

st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center;'>Jornada Mastera</h1>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    searchSubject = st.text_input("Digite o assunto para pesquisar artigos e patentes (Uso de nomes científicos geralmente oferece melhores resultados):", "Câncer")
    yearsToSearch = st.number_input("Digite o número de anos para pesquisar:", min_value=3, max_value=10, value=5)
    limitRecent = st.number_input("Digite o número de artigos e patentes mais recentes para buscar:", min_value=3, max_value=10, value=5)
    searchButton = st.button("Buscar Artigos e Patentes", use_container_width=True)

if searchButton:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.spinner("Buscando dados... Isso demora um pouco"):
            searchSubject = asyncio.run(translateIfNeeded(searchSubject))
            print(f"Searching for: {searchSubject}")
            
            pubMedResponseData = manager.getDataFromPubmed(searchSubject, rangeYears=yearsToSearch, mostRecentLimit=limitRecent)
            googlePatentsResponseData = manager.getDataFromSerp(searchSubject, rangeYears=yearsToSearch, mostRecentLimit=limitRecent)
            
            articlePlotData = pubMedResponseData.get('plotData', {})
            totalArticles = articlePlotData.pop('total', None)  # Remove total from plotData for display

            googlePatentsPlotData = googlePatentsResponseData.get('plotData', {})
            totalPatents = googlePatentsPlotData.pop('total', None)  # Remove total from plotData for display

            gapScore = manager.calculateGapScore(articlePlotData.copy(), googlePatentsPlotData.copy())
            geminiData = f"""All data for search {searchSubject}:\n
              Articles: {articlePlotData}\n
              Total Articles: {totalArticles}\n
              Recent Articles: {pubMedResponseData.get('mostRecent', [])}\n
              Patents: {googlePatentsPlotData}\n
              Total Patents: {totalPatents}\n
              Recent Patents: {googlePatentsResponseData.get('mostRecent', [])}\n
              Gap Score: {gapScore*100}"""
            geminiResponse = manager.getModelResponse(geminiData)

        st.success("Busca concluída com sucesso!")
        st.subheader("Resultado Final")
        st.markdown(f"**Gap Score:** {(gapScore*100):.2f}")
        
        st.markdown(f"### Análise e resumo gerado pelo Gemini")
        st.markdown(geminiResponse)

       

    col1, col2 = st.columns(2)

    with col1:
        st.title("Artigos")
        st.markdown("Dados buscados do [PubMed](https://pubmed.ncbi.nlm.nih.gov/).")
        

        st.subheader("Contagem de Artigos por Ano")
        st.markdown(f"**Total de Artigos Encontrados:** {totalArticles if totalArticles is not None else 0}")
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
        st.title("Patentes")
        st.markdown("Dados de patentes relacionadas buscados do [Google Patents](https://patents.google.com/) com [SerpApi](https://serpapi.com/).")
        
        st.subheader("Contagem de Patentes por Ano")
        st.markdown(f"**Total de Patentes Encontradas:** {totalPatents if totalPatents is not None else 0}")
        st.markdown("**Nota:** Se o gráfico não aparecer, clique na área do gráfico para exibi-lo.")
        st.bar_chart(data=googlePatentsPlotData, use_container_width=True)

        st.subheader("Patentes Recentes")
        mostRecentPatents = googlePatentsResponseData.get('mostRecent', [])
        if mostRecentPatents:
            st.write(f"Exibindo {len(mostRecentPatents)} patentes recentes.")
            for patent in mostRecentPatents:
                st.markdown(f"**Título:** {patent.get('title', 'N/A')}")
                st.markdown(f"**Número de Publicação:** {patent.get('publicationNumber', 'N/A')}")
                st.markdown(f"**Cessionário:** {patent.get('assignee', 'N/A')}")
                st.markdown(f"**Data de Prioridade:** {patent.get('priorityDate', 'N/A')}")
                with st.expander("Trecho"):
                    st.write(patent.get('snippet', 'N/A'))
                with st.expander("Status por País"):
                    #countryStatus is a dict in string format, so we convert it to a dict before displaying
                    countryStatus = patent.get('countryStatus', 'N/A')
                    if isinstance(countryStatus, str) and countryStatus != 'N/A':
                        try:
                            countryStatus = eval(countryStatus)
                        except:
                            pass # Keep as string if eval fails
                    st.write(countryStatus)
                st.markdown(f"**Citações Anteriores:** {patent.get('forwardCitations', 0)}")
                st.markdown(f"**Data de Publicação:** {patent.get('publicationDate', 'N/A')}")
                st.markdown(f"**Link da Patente:** {patent.get('patentLink', 'N/A')}")
                st.write("---")
        else:
            st.write("Nenhuma patente recente encontrada.")

