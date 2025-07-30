import streamlit as st

st.title('CV Scoring App')
job_description = st.text_area('Введите описание вакансии')
cv = st.text_area('Введите описание резюме')
if st.button('Score CV'):
    st.write('CV scored with 80%')
    st.write(job_description)
    st.write(cv)
		