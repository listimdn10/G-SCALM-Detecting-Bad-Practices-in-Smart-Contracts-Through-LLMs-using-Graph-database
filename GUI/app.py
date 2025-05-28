import streamlit as st
from openai import OpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from neo4j import GraphDatabase
import os
from langchain_neo4j import Neo4jVector

# Set OpenAI key
os.environ["OPENAI_API_KEY"]="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"
client = OpenAI()

# Neo4jVector requires the Neo4j database credentials

url = "neo4j+s://1fe0454c.databases.neo4j.io"
username = "neo4j"
password = "E8rUVyDPMhcSDq2_Vngae2rNsTgp7_qYfxvjwl9rN7g"



# Load embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
behaviors_index = Neo4jVector.from_existing_graph(
    embedding=embeddings,
    url=url,
    username=username,
    password=password,
    index_name="Behavior_index",
    node_label="Behavior",
    text_node_properties=["text"],
    embedding_node_property="embedding"
)

# Neo4j driver
driver = GraphDatabase.driver(url, auth=(username, password))

# GPT Function
def analyze_functional_semantics(code):
    prompt = f"""
    What is the purpose of the above code snippet? Please summarize in this format:
    Abstract purpose:
    
    Detail Behaviors: 1. ... 2. ... 3...

    Code:
    {code}
    """
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert in Solidity vulnerability analysis."},
            {"role": "user", "content": prompt},
        ],
    )
    return completion.choices[0].message.content

def get_related_vulnerabilities(behavior_text):
    def query(tx):
        result = tx.run(
            """
            MATCH (b:Behavior)-[:EXPOSES]->(v:Vulnerability)
            WHERE b.text = $text
            RETURN v.text AS vuln
            """, text=behavior_text
        )
        return [record["vuln"] for record in result]

    with driver.session() as session:
        return session.execute_read(query)

# --- Streamlit UI ---
st.set_page_config(page_title="Smart Contract Vulnerability Analyzer", layout="wide")
st.title("🔍 Smart Contract Vulnerability Analyzer")

solidity_code = st.text_area("Paste your Solidity code:", height=300)

if st.button("Analyze"):
    if not solidity_code.strip():
        st.warning("Please paste Solidity code first.")
    else:
        with st.spinner("Analyzing with GPT..."):
            analysis_result = analyze_functional_semantics(solidity_code)
            st.subheader("🔎 Functional Semantics")
            st.code(analysis_result)

        with st.spinner("Searching related behaviors..."):
            docs_with_score = behaviors_index.similarity_search_with_score(analysis_result, k=2)
            for doc, score in docs_with_score:
                st.write(f"**Similarity Score:** {score:.2f}")
                st.write(doc.page_content)
                st.markdown("---")

                behavior_text = doc.page_content.strip().removeprefix("text:").strip()
                vulnerabilities = get_related_vulnerabilities(behavior_text)

                if vulnerabilities:
                    st.markdown("**🔐 Related Vulnerabilities:**")
                    for v in vulnerabilities:
                        st.markdown(f"- {v}")
                else:
                    st.info("No related vulnerabilities found.")

