import streamlit as st
import pandas as pd
import plotly.express as px
import openai
import os

st.set_page_config(page_title="Talking Rabbitt", layout="wide")

st.title("🐰 Talking Rabbitt")
st.subheader("Talk to your business data")

# Get API key from Streamlit secrets
openai.api_key = os.getenv("OPENAI_API_KEY")

uploaded_file = st.file_uploader("Upload your CSV dataset", type=["csv"])

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.success("Dataset uploaded successfully!")

    st.write("### Dataset Preview")
    st.dataframe(df.head())

    question = st.text_input("Ask a question about your data")

    if question:

        prompt = f"""
        You are a data analyst.

        Dataset columns:
        {list(df.columns)}

        User question:
        {question}

        Provide a clear answer.
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        answer = response["choices"][0]["message"]["content"]

        st.write("### AI Insight")
        st.write(answer)

        # Automatic chart
        numeric_cols = df.select_dtypes(include="number").columns

        if len(numeric_cols) > 0:

            x_col = df.columns[0]
            y_col = numeric_cols[0]

            fig = px.bar(df, x=x_col, y=y_col,
                         title=f"{y_col} by {x_col}")

            st.plotly_chart(fig)