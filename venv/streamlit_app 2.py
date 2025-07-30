# -*- coding: utf-8 -*-
import requests
import uuid
import streamlit as st

# Получение токена доступа
response = requests.post(
    "https://ngw.devices.sberbank.ru:9443/api/v2/oauth",
    headers = {
        "Authorization": "Basic NzYwYzVhMTctZWJkMC00MGVlLWE2ZTctZWQxNjZjMTMyZmIyOjE0ZmYwYjkyLTk4YjQtNGVkMi04MGFhLTU1NjU1NzBjNTMyNQ==",
        "RqUID": str(uuid.uuid4())
    },
    data = {"scope": "GIGACHAT_API_PERS"},
    verify = True
)
a_token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {a_token}" }
#print(headers)


def request_gpt(system_prompt, user_prompt):
    data = {
        "model": "GigaChat-2",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 1000,
        "temperature": 0
    }

    # Отправка запроса к GigaChat API
    response = requests.post(
        "https://gigachat.devices.sberbank.ru/api/v1/chat/completions",
        json = data,
        headers = headers,
        verify = True
    )

    return response.json()['choices'][0]['message']['content']

st.title('CV Scoring App')
SYSTEM_PROMPT = """
Проскорь кандидата, насколько он подходит для данной вакансии.

Сначала напиши короткий анализ, который будет пояснять оценку.
Отдельно оцени качество заполнения резюме (понятно ли, с какими задачами сталкивался кандидат и каким образом их решал?). Эта оценка должна учитываться при выставлении финальной оценки - нам важно нанимать таких кандидатов, которые могут рассказать про свою работу
Потом представь результат в виде оценки от 1 до 10.
""".strip()
job_description = st.text_area('Введите описание вакансии')
cv = st.text_area('Введите описание резюме')
if st.button('Оценить резюме'):
    with st.spinner('Оцениваем резюме...'):
        response = request_gpt(SYSTEM_PROMPT, f'# ВАКАНСИЯ\n{job_description}\n\n# РЕЗЮМЕ\n{cv}')
    st.write(response)
