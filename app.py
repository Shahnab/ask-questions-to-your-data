import streamlit as st
import pandas as pd
import asyncio
import random

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

import sketch
import streamlit.components.v1 as components
from IPython.display import HTML, display
import uuid
import base64
import json

col1, mid, col2= st.columns([1,1,20])
with col1:
    st.image("https://avatars.githubusercontent.com/u/106505054?s=200&v=4", width=70)
with col2:
    st.markdown("# Ask Questions to Data")
st.markdown("###### Streamlit implementation of sketch package in pandas ")


tab1, tab2 = st.tabs(["Ask Questions to Data", "About the Application"])

with tab1:

st.write('')
        
    def upload_data_file():
        st.session_state.file = None
        st.session_state.df = None
        file = st.file_uploader(
            label='Upload Data File',
            type=["csv","xlsx","xls"]
        )
        if file is not None:
            load_data(file)
           
        
    def load_data(file):
        st.session_state.file = file
        df = pd.read_csv(file)
        st.session_state.df = df
        
            
    # Configure session state
    if 'file' not in st.session_state:
        st.session_state.file = None
    if 'df' not in st.session_state:
        st.session_state.df = None

        
    if st.session_state.file is None:
        upload_data_file()


    def to_b64(data):
        return base64.b64encode(json.dumps(data).encode("utf-8")).decode("utf-8")

    if st.session_state.file is not None:
        st.session_state.file.seek(0)

        df = pd.read_csv(st.session_state.file)

        st.header("Uploaded Data:")
        st.dataframe(df)

        with st.form("my_form"):
            request_type = st.radio(
                label="Selection Panel",
                options=['Ask question about the data', 'Generate codes for new analysis'],
                index=0
            )

            request = st.text_area(
                label="Input your request",
                value="",
                height=50,
                max_chars=500
            )

            submitted = st.form_submit_button("Submit")

        if submitted:
            if request_type== 'Ask question about the data':
                if request != "":
                    answer = df.sketch.ask(request, call_display=False)
                    st.code(answer)
            else:
                if request != "":
                    answer1 = df.sketch.howto(request, call_display=False)
                    st.code(answer1)
        
    else:
        st.write('Please upload data file in order to ask questions to it.')

with tab2:
    
    st.title("Demo video")
    st.video('https://youtu.be/hDbTjWqmrJY')
    st.title("About the Package used")
    st.markdown("###### Sketch is an AI code-writing assistant for pandas users that understands the context of the data, greatly improving the relevance of suggestions. Sketch is usable in seconds and doesn't require adding a plugin to IDE.")

    st.title("How it works:")
    st.markdown("###### Sketch uses efficient approximation algorithms (data sketches) to quickly summarize the data, and feed that information into language models. Right now, it does this by summarizing the columns and writing these summary statistics as additional context to be used by the code-writing prompt. In the future, the dev team hopes to feed these sketches directly into custom made data + language foundation models to get more accurate results.")

    st.title("Usecases:")
    st.markdown("###### --- Data Catalogging: General tagging (eg. PII identification), Metadata generation (names and descriptions)")
    st.markdown("###### --- Data Engineering: Data cleaning and masking (compliance), Derived feature creation and extraction")
    st.markdown("###### --- Data Analysis: Data questions, Data Visualizations")

    st.caption("More details available in Github Repository: https://github.com/approximatelabs/sketch")