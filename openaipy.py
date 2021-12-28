import os
import openai
import streamlit as st
import time
from googletrans import Translator
translator = Translator()



#YOUR API KEY HERE
openai.api_key = "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"





col1, col2 = st.columns(2)
with col1:
    st.title("Англи бичвэрийг монголоор дүгнэж бичэх (Mongolian Summarization Prototype)")
    
with col2:
    st.image('https://upload.wikimedia.org/wikipedia/commons/e/e2/Inkwell_icon_-_Noun_Project_2512_red.svg', width = 190)

    
col3, col4 = st.columns(2)
with col4:
        st.write("Гол санаа таамаглалт (Summarization) ↓")
with col3:
        with st.expander("Instructions on obtaining an API key"):
         st.write("""
            1. Go to beta.openai.com
            2. Create an account
            3. On the upper right corner, click on your user profile picture.
            4. From the drop down menu, select "View API Keys"
            5. Copy paste your own API key instead of the one on the openaipy.py file.
            6. Run streamlit locally after adjusting API key.
         """)

        context_text = st.text_input(label = "Бичвэрийн сэдэв болон санааг товчоор тайлбарлана уу? (Describe the topic of the writing in short) \n", max_chars = 150)
        prompt_text = st.text_area(label = "Гол санаа гаргах бичвэрийг оруулна уу? (Paste/write the intended writing for summarization):\n", max_chars=1200) + "\n tl;dr: \n"

        number = st.slider("Хэр оновчтой байх вэ? (Accuracy/Creativity) (чөлөөт бичлэг = 1, албан бичиг = 0)", 0, 100)
        number = number / 100
        if st.button("Эхлэх"):        
            merged_text = str(f"This writing is about:{context_text}"+prompt_text)
            response1 = openai.Completion.create(engine="curie", prompt=merged_text, max_tokens=150, echo=False, temperature=number)
            response = openai.Completion.create(
              engine="content-filter-alpha",
              prompt = "<|endoftext|>"+merged_text+"\n--\nLabel:",
              temperature=0,
              max_tokens=1,
              top_p=1,
              frequency_penalty=0,
              presence_penalty=0,
              logprobs=10
            )
            response1 = response1.choices[0].text
            output_label = response.choices[0].text
            toxic_threshold = -0.355
            if output_label == "2":
                logprobs = response["choices"][0]["logprobs"]["top_logprobs"][0]
                if logprobs["2"] < toxic_threshold:
                    logprob_0 = logprobs.get("0", None)
                    logprob_1 = logprobs.get("1", None)
                    if logprob_0 is not None and logprob_1 is not None:
                        if logprob_0 >= logprob_1:
                            output_label = "0"
                        else:
                            output_label = "1"
                    elif logprob_0 is not None:
                        output_label = "0"
                    elif logprob_1 is not None:
                        output_label = "1"
            if output_label not in ["0", "1", "2"]:
                output_label = "2"
                response1 = "Inappropriate/potentially harmful text received, please change"
            translations = translator.translate(response1, dest='mn')
            with col4:
                st.text_area(label = "Mongolian Version",value=translations.text)
                st.text_area(label = "English Version", value = response1)
                
st.caption("by Erdenemunkh - LETU Mongolia, 2021, Fall")

