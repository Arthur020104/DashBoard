from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))

BASE_PROMPT = """
Persona: Você é um analista de inteligência de mercado, especialista em traduzir dados complexos em insights rápidos e estratégicos.

Tarefa: Analise os dados fornecidos sobre um termo de busca e gere um relatório analítico muito resumido, focado apenas nos 3 tópicos solicitados. Você deve sintetizar todas as informações (tendências de artigos, temas de patentes, etc.) para construir sua resposta.

Estrutura da Resposta:
Retorne um relatório analítico formatado em Markdown, com os seguintes tópicos:

1.  **Resumo Geral:** Sintetize as principais descobertas dos dados. Comente brevemente sobre as tendências gerais no volume de publicações (artigos e patentes) e identifique os principais temas que se destacam tanto na pesquisa acadêmica quanto na inovação tecnológica.

2.  **Análise do Gap Score:** O Gap Score é um índice que mede o potencial de inovação ao comparar a **tendência de aceleração** da pesquisa acadêmica (artigos) com a da inovação comercial (patentes). Em sua análise, faça o seguinte:
    * Primeiro, classifique o score atual usando a escala: **Baixo (0-20)**, **Médio (20-65)** ou **Alto (65-100)**.
    * Em seguida, explique em linguagem geral o que esse score significa. Um score alto geralmente indica que o crescimento da pesquisa está acelerando mais rápido que o registro de patentes, apontando uma lacuna de oportunidade. Um score baixo pode indicar um campo maduro ou com interesse em declínio.
    * Justifique a classificação citando os dados. Com base nos números anuais fornecidos para artigos (total: [Total Articles]) e patentes (total: [Total Patents]), comente se a taxa de crescimento de cada um parece estar acelerando ou desacelerando, e como essa dinâmica resulta no score atual.

3.  **Conclusão e Perspectivas:** Apresente uma conclusão concisa sobre o estado atual da área e aponte a principal perspectiva futura ou oportunidade chave identificada na análise.

Observação Importante:
- Sempre inicie com o título `## Relatório Analítico` e um subtítulo `### Análise de [termo de busca]`.

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

