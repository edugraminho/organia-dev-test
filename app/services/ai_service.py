import openai
import os
from pydantic import BaseModel


client = openai.OpenAI(
    api_key=os.getenv("MARITACA_API_KEY"),
    base_url="https://chat.maritaca.ai/api",
)


class ReviewDetails(BaseModel):
    """
    Represents the sentiment analysis result for a given review.

    Attributes:
        sentiment (str): The general sentiment classification (e.g., "positive", "negative", "neutral").
        score (float): A sentiment score ranging from -1 (very negative) to 1 (very positive).
        keywords (list[str]): List of key positive and negative words that influenced the sentiment.
        explanation (str): A brief explanation of the sentiment analysis result.
    """

    sentiment: str
    score: float
    keywords: list[str]
    explanation: str


def analyze_review_sentiment(review_text: str) -> dict:
    """
    Analyzes the sentiment of a given customer review using the Maritaca AI model.

    Args:
        review_text (str): The text of the customer review.

    Returns:
        dict: A dictionary containing the sentiment analysis result, including:
            - "sentiment": The detected sentiment ("positive", "negative", or "neutral").
            - "score": A numerical sentiment score (-1 to 1).
            - "keywords": Key positive and negative words influencing the sentiment.
            - "explanation": A short description explaining the sentiment classification.
    """
    prompt = f"""
        Analise o sentimento do comentário a seguir e responda tudo em PORTUGUÊS-BR:
        'sentiment': O sentimento geral do comentário: 'positiva', 'negativa' ou 'neutra';
        'score': Uma pontuação de sentimento de -1 (muito negativa) a 1 (muito positiva);
        'keywords': Uma lista de palavras-chave POSITIVAS e seguindo das NEGATIVAS que ajudaram a determinar o resultado;
        'explanation': Uma breve explicação da análise do sentimento
    """

    completion = client.beta.chat.completions.parse(
        model="sabia-3",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": review_text},
        ],
        response_format=ReviewDetails,
    )
    content = completion.choices[0].message.parsed

    return content.model_dump(by_alias=True)
