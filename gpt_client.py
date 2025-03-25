from log import log, setup_logger
import openai
from dotenv import load_dotenv
import os

load_dotenv() 

class GPTClient:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("API key não encontrada! Verifique o .env.")
        self.client = openai.OpenAI(api_key=api_key)

    def get_suggested_questions(self):
        questions = [
            "Quais são os principais pontos turísticos da cidade?",
            "Qual é a melhor época do ano para visitar?",
            "Quais são as comidas típicas da região?",
            "Quais atividades ou eventos imperdíveis existem na cidade?",
        ]
        icons = ["Edit", "Airplane", "Lightbulb", "Code"]
        suggested_questions = {
            f"sug{i+1}": [question, icons[i]] for i, question in enumerate(questions)
        }
        return suggested_questions

    def query_chat(self, prompt: str, city: str):
        """
        Envia uma solicitação para o modelo GPT-4, com um contexto específico:
        Você se passa por um assistente de viagens, especializado em
        ajudar usuários a explorar destinos turísticos, voos, acomodações, etc.
        """
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"Você é um assistente de viagens especializado em ajudar os usuários a explorar destinos,"
                        f" voos, acomodações, pontos turísticos e gastronomia local. O usuário está perguntando"
                        f" Não precisa colocar uma contextualização antes da mensagem, como 'Claro, aqui está a resposta', ou 'Boa tarde! ...' apenas começe com a resposta"
                        f" {prompt}"
                        f" , incluindo dicas de passeios, cultura local, restaurantes e acomodações."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=1024,
            temperature=0.7,
        )
        log.info(
            "******************************************************************************"
        )
        log.info(response.choices[0].message.content)
        return response.choices[0].message.content
