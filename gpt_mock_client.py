import os
from typing import Iterable
import asyncio

import gradio_client
from log import log
from gradio_client import Client
import ast


class Document:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class GPTMockClient:
    def __init__(self):
        self.chat_client = None

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
        response = f"""PROMPT: {prompt} \n\n\nMocked Response"""
        return response
