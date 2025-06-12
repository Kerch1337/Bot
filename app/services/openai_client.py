import os
import openai
from openai import OpenAI
from openai import OpenAIError
from openai._exceptions import AuthenticationError, RateLimitError
from database.model import Message, Dialogue
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")
PROXY_URL = os.getenv("PROXY_URL")
os.environ["http_proxy"] = PROXY_URL
os.environ["https_proxy"] = PROXY_URL

def get_or_create_dialogue(session, user):
    """Получает или создаёт диалог с пользователем"""
    dialogue = session.query(Dialogue).join(Dialogue.participants).filter_by(id=user.id).first()
    if not dialogue:
        dialogue = Dialogue(participants=[user])
        session.add(dialogue)
        session.commit()
    return dialogue

def build_history(session: Session, dialogue: Dialogue):
    """Генерирует список сообщений для OpenAI"""
    messages = session.query(Message).filter_by(dialogue_id=dialogue.id).order_by(Message.sent_at).all()
    history = [{"role": "system", "content": "Ты — дружелюбный помощник."}]
    for msg in messages:
        role = "user" if msg.sender.role.name == "USER" else "assistant"
        history.append({"role": role, "content": msg.text})
    return history[-20:]  # ограничим последние 20 сообщений

def chat_with_gpt(session: Session, user, prompt: str):
    """Отправляет сообщение в GPT и возвращает ответ"""
    try:
        dialogue = get_or_create_dialogue(session, user)

        # Сохраняем сообщение пользователя
        user_msg = Message(
            text=prompt,
            sender_id=user.id,
            dialogue=dialogue,
            sent_at=datetime.utcnow()
        )
        session.add(user_msg)
        session.flush()

        messages = build_history(session, dialogue)
        messages.append({"role": "user", "content": prompt})

        client = OpenAI()

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
        )

        reply = response.choices[0].message.content

        # Сохраняем ответ GPT
        assistant_msg = Message(
            text=reply,
            sender_id=user.id,  # или `None`, если хочешь отличать системные
            dialogue=dialogue,
            sent_at=datetime.utcnow()
        )
        session.add(assistant_msg)
        session.commit()

        return reply

    except AuthenticationError:
        return "❌ Неверный OpenAI API ключ"
    except RateLimitError:
        return "⚠️ Превышен лимит запросов OpenAI"
    except OpenAIError as e:
        return f"Ошибка OpenAI: {e}"
    except Exception as e:
        return f"🚫 Общая ошибка: {e}"
