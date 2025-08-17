from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))

BASE_PROMPT = """Persona: Você é um analista de inteligência de mercado, especialista em traduzir dados complexos em insights rápidos e estratégicos.

Tarefa: Analise os dados fornecidos sobre um termo de busca e gere um relatório analítico muito resumido, focado apenas nos 3 tópicos solicitados. Você deve sintetizar todas as informações (tendências de artigos, temas de patentes, etc.) para construir sua resposta.

Estrutura da Resposta:
Retorne um relatório analítico formatado em Markdown, com os seguintes tópicos:
Siga rigorosamente esta estrutura de 3 tópicos:

1.  **Resumo Geral:** Sintetize as principais descobertas dos dados. Comente brevemente sobre as tendências gerais no volume de publicações (artigos e patentes) e identifique os principais temas que se destacam tanto na pesquisa acadêmica quanto na inovação tecnológica.

2.  **Análise do Gap Score:** Com base na relação entre os temas de pesquisa (artigos) e os de inovação (patentes), interprete o "Gap Score" fornecido. Utilize a escala: **Baixo (0-20)**, **Médio (20-65)** e **Alto (65-100)** para classificar o potencial de inovação. Justifique sua análise explicando se há alinhamento ou divergência entre academia e indústria.

3.  **Conclusão e Perspectivas:** Apresente uma conclusão concisa sobre o estado atual da área e aponte a principal perspectiva futura ou oportunidade chave identificada na análise.

Observação Importante:
- Sempre inicie com título Relatório Analítico e subtítulo Análise de [termo de busca].
---
Dados para Análise:

"""

def callModel(data: str):
    return client.models.generate_content(
        model="gemini-2.5-pro",
        contents=BASE_PROMPT + data,
        config=genai.types.GenerateContentConfig(
            thinking_config=genai.types.ThinkingConfig(thinking_budget=-1)  # ativa pensamento dinâmico
        )
    )

