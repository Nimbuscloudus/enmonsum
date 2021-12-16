import os
import openai
import streamlit as st
from googletrans import Translator
translator = Translator()

#INSERT YOUR OWN API KEY HERE SINCE EACH ITERATION OF OPENAI COSTS MONEY
openai.api_key = "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"

col1, col2 = st.columns(2)
with col1:
    st.title("Англи бичвэрийг монголоор дүгнэж бичэх")
    
with col2:
    st.image('https://upload.wikimedia.org/wikipedia/commons/e/e2/Inkwell_icon_-_Noun_Project_2512_red.svg', width = 190)

    
col3, col4 = st.columns(2)
with col4:
        st.write("Гол санаа таамаглалт ↓")
with col3:
        context_text = st.text_input(label = "Бичвэрийн сэдэв болон санааг товчоор тайлбарлана уу?? \n", max_chars = 150)
        prompt_text = st.text_area(label = "Гол санаа гаргах бичвэрийг оруулна уу?:\n", max_chars=1200) + "\n tl;dr: \n"

        number = st.slider("Хэр оновчтой байх вэ? (чөлөөт бичлэг = 1, албан бичиг = 0)", 0, 100)
        number = number / 100
        if st.button("Эхлэх"):        
            merged_text = str(f"This writing is about:\n{context_text}\n\n\n"+prompt_text)
            response = openai.Completion.create(engine="curie", prompt=merged_text, max_tokens=50, echo=False, temperature=number)
            response = response.choices[0].text
            translations = translator.translate(response, dest='mn')
            with col4:
                st.text_area(label = "",value=translations.text)
                
st.caption("by Erdenemunkh - LETU Mongolia, 2021, Fall")
