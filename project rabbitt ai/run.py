import streamlit as st
import pandas as pd
import json
from agent import create_pd_agent, query_pd_agent

def decode_response(response: str) -> dict:
    return json.loads(response)

def write_response(response_dict: dict):
    if "answer" in response_dict:
        st.write(response_dict["answer"])

    if "chart" in response_dict:
        st.image("./chart_image/chart.png")

    if "table" in response_dict:
        data = response_dict["table"]
        df = pd.DataFrame(data["data"], columns=data["columns"])
        st.table(df)

st.title("🤔 Chat with your CSV 📊")

st.write("Please upload your CSV and metadata file below.")

csv_data = st.file_uploader("Upload your CSV file.")

query = st.text_area("Please let me know your query.")

if st.button("Submit Query", type="primary"):
    agent = create_pd_agent(csv_data)

    response = query_pd_agent(agent=agent, query=query)
    decoded_response = decode_response(response)
    write_response(decoded_response)
