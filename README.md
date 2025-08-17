
# Inteligência de Mercado e Análise de Inovação


**Link para a aplicação:** [Acesse aqui](https://jornadamastera.streamlit.app/)

### Funcionalidades

* **Interface Interativa:** Permite ao usuário inserir um tópico de pesquisa, definir um período de análise e especificar o número de resultados.
* **Análise Comparativa:** Coleta e processa dados de artigos (PubMed) e patentes (Google Patents) para análise de tendências.
* **Cálculo do Gap Score:** Utiliza regressão linear para analisar as tendências de crescimento de publicações acadêmicas versus registros de patentes, identificando oportunidades de inovação.
* **Geração de Relatório com IA:** Integra-se ao Google Gemini para gerar uma análise qualitativa completa, incluindo resumo executivo, análise do Gap Score e conclusões estratégicas.
* **Visualização de Dados:** Apresenta gráficos de tendências e listas detalhadas dos artigos e patentes mais recentes.
* **Logging de Operações:** Registra todas as consultas e operações em um banco de dados PostgreSQL para rastreabilidade e auditoria.

### Tecnologias Utilizadas

* **Backend:** Python 3.10+
* **Interface Web:** Streamlit
* **Análise de Dados:** NumPy, Pandas
* **Banco de Dados:** PostgreSQL (hospedado na Neon)
* **Acesso ao Banco de Dados:** SQLAlchemy
* **APIs Externas:**
    * PubMed (via `requests`)
    * Google Patents (via `google-search-results` - SerpApi)
    * Google Gemini (via `google-genai`)
* **Utilitários:**
    * `python-dotenv` para gerenciamento de variáveis de ambiente.
    * `googletrans` e `langdetect` para tradução de termos de busca.

### Como Executar o Projeto Localmente

Siga os passos abaixo para configurar e executar a aplicação em seu ambiente local.

**1. Clonar o Repositório**
```
git clone https://github.com/Arthur020104/DashBoard.git
cd DashBoard
```

**2. Criar e Ativar um Ambiente Virtual**
```
python -m venv venv
.\\venv\\Scripts\\activate
```

**3. Instalar as Dependências**
```
pip install -r requirements.txt
```

**4. Configurar Variáveis de Ambiente**
Crie um arquivo chamado `.env` na raiz do projeto e adicione as seguintes variáveis. Substitua os valores de exemplo pelas suas chaves de API e string de conexão.
```
DB_CONNECTION_STRING=DB_URL
SERPAPI_KEY=SUA_SERPAPI_KEY
GEMINI_API_KEY=SUA_GEMINI_API_KEY
```

**5. Executar a Aplicação**
Com o ambiente virtual ativado e as variáveis configuradas, inicie o servidor do Streamlit:
```
streamlit run app.py
```
A aplicação estará disponível em `http://localhost:8501`.

### Configuração do Banco de Dados (PostgreSQL com pgAdmin)

A aplicação está configurada para usar um banco de dados PostgreSQL hospedado na Neon. Para conectar-se a ele usando o pgAdmin, siga os passos:

1.  **Abra o pgAdmin** e clique com o botão direito em `Servers` -> `Create` -> `Server...`.
2.  Na aba **General**, dê um nome para a conexão (ex: `Projeto_Inovacao_Neon`).
3.  Vá para a aba **Connection** e preencha os campos com as informações da sua URL de conexão (`postgresql://user:password@host:port/dbname`):
    * **Host name/address**: `ep-rough-thunder-acwwnm2x-pooler.sa-east-1.aws.neon.tech`
    * **Port**: `5432`
    * **Maintenance database**: `neondb`
    * **Username**: `neondb_owner`
    * **Password**: `npg_Ssl0nj9VZOdy`
4.  Vá para a aba **SSL** e mude a opção **SSL mode** para `Require`. Isso é fundamental para a conexão com a Neon.
5.  Clique em **Save** para finalizar. Agora você pode explorar o banco de dados através do pgAdmin.

### Fontes de Dados e APIs

* **PubMed API**: Utilizada para buscar dados sobre publicações científicas. O acesso é público e não requer chave de API, mas está sujeito a limites de taxa de requisição.
* **Google Patents (via SerpApi)**: Utilizada para buscar dados sobre patentes registradas.
* **Google Gemini API**: Utilizada para a geração do relatório analítico. Requer uma chave de API do Google AI Studio.
