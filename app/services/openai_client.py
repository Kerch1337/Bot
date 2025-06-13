import os
from datetime import datetime
import openai
from openai import AsyncOpenAI
from openai._exceptions import AuthenticationError, RateLimitError, OpenAIError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.model import Message, Dialogue

openai.api_key = os.getenv("OPENAI_API_KEY")
PROXY_URL = os.getenv("PROXY_URL")
os.environ["http_proxy"] = PROXY_URL
os.environ["https_proxy"] = PROXY_URL

async def get_or_create_dialogue(session: AsyncSession, user):
    result = await session.execute(
        select(Dialogue).join(Dialogue.participants).filter_by(id=user.id)
    )
    dialogue = result.scalar()
    if not dialogue:
        dialogue = Dialogue(participants=[user])
        session.add(dialogue)
        await session.commit()
    return dialogue

async def build_history(session: AsyncSession, dialogue: Dialogue):
    result = await session.execute(
        select(Message)
        .filter_by(dialogue_id=dialogue.id)
        .order_by(Message.sent_at)
    )
    messages = result.scalars().all()
    history = [{"role": "system", "content": "Ты — дружелюбный помощник."}]
    for msg in messages:
        role = "user" if msg.sender.role.name == "USER" else "assistant"
        history.append({"role": role, "content": msg.text})
    return history[-20:]

async def chat_with_gpt(session: AsyncSession, user, prompt: str):
    try:
        dialogue = await get_or_create_dialogue(session, user)

        user_msg = Message(
            text=prompt,
            sender_id=user.id,
            dialogue=dialogue,
            sent_at=datetime.utcnow()
        )
        session.add(user_msg)
        await session.flush()

        messages = await build_history(session, dialogue)
        messages.append({"role": "user", "content": prompt})

        client = AsyncOpenAI()

        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
        )

        reply = response.choices[0].message.content

        assistant_msg = Message(
            text=reply,
            sender_id=user.id,
            dialogue=dialogue,
            sent_at=datetime.utcnow()
        )
        session.add(assistant_msg)
        await session.commit()

        return reply

    except AuthenticationError:
        return "❌ Неверный OpenAI API ключ"
    except RateLimitError:
        return "⚠️ Превышен лимит запросов OpenAI"
    except OpenAIError as e:
        return f"Ошибка OpenAI: {e}"
    except Exception as e:
        return f"🚫 Общая ошибка: {e}"
