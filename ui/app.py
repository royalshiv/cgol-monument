import os, json, streamlit as st, requests
from openai import OpenAI
from client.conway_tool import tool_schema, simulate_word, handle_prompt

st.set_page_config(page_title="CGOL + LLM", layout="centered")
st.title("Conway's Game of Life – LLM Tool")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERVICE_URL = os.getenv("CGOL_SERVICE_URL", "http://127.0.0.1:8000")

with st.sidebar:
    st.write("Service URL:", SERVICE_URL)
    st.write("Model:", "gpt-4o-mini")
    ok = OPENAI_API_KEY is not None
    st.success("OpenAI key found") if ok else st.warning("Set OPENAI_API_KEY")

prompt = st.text_area("Enter any prompt", "How many generations will the word 'monument' return from the Conway tool?")
if st.button("Ask"):
    if not OPENAI_API_KEY:
        st.info("No API key found; using local router.")
        st.code(handle_prompt(prompt))
    else:
        client = OpenAI(api_key=OPENAI_API_KEY)
        tools = [{
            "type": "function",
            "function": tool_schema()
        }]
        # Ask the model
        msg = [{"role": "user", "content": prompt}]
        resp = client.chat.completions.create(model="gpt-4o-mini", messages=msg, tools=tools)
        choice = resp.choices[0]
        # If the model wants to call the tool, do it:
        if choice.finish_reason == "tool_calls":
            for tc in choice.message.tool_calls:
                if tc.function.name == "conway_simulator":
                    args = json.loads(tc.function.arguments)
                    data = simulate_word(args["word"])
                    st.json(data)
        else:
            st.write(choice.message.content)
