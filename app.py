import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from htmlTemplates import css, bot_template, user_template
from langchain_core.messages import HumanMessage, AIMessage

#Função para juntar todo o texto do pdf em uma unica variável, um object texto que vai conter todo o texto do documento de forma corrida
def juntar_texto(pdfs):
    texto = ""
    for pdf in pdfs:
        leitor_pdf = PdfReader(pdf)
        for pagina in leitor_pdf.pages:
            conteudo = pagina.extract_text()
            if conteudo:  # evita erro se a página não tiver texto extraível
                texto += conteudo + "\n"
    return texto

# Função que separa a variável texto em chunks de 1000 caracteres. o argumento chunk_overlap impede que uma chunk finalizada no meio da frase não seja interrompida no meio,
# de forma que atrapalhe a criação dos embeddings)
def separar_chunks(texto):
    separador_texto = CharacterTextSplitter(separator='\n', chunk_size=1000, chunk_overlap=200, length_function=len)
    chunks = separador_texto.split_text(texto)
    return chunks

# Função que "monta" o banco de dados de embeddings, utilizando as proprias da OpenAI. Ou seja, o algoritmo apenas separa as chunks e envia para a openai, que vai gerar as embeddingsz
def montar_vectorstore(chunks_texto):
    embeddings = OpenAIEmbeddings()
    #embeddings = HuggingFaceEmbeddings(model_name='Qwen/Qwen3-Embedding-0.6B',  model_kwargs={"device": "cpu"}, encode_kwargs={"normalize_embeddings": True}) #Tentei rodar localmente, mas ficou muito lento
    vectorstore = FAISS.from_texts(texts = chunks_texto, embedding=embeddings) 
    return vectorstore

#Permite que a conversa seja contínua, e não resete após uma unica pergunta
def continua_conversa(vectorstore, model_name="gpt-4o-mini"):
    llm = ChatOpenAI(model=model_name, temperature=0)

    # Retriever do FAISS
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    # Prompt para reescrever pergunta baseada no histórico da sessão
    contextualize_q = ChatPromptTemplate.from_messages([
        ("system", "Reescreva a pergunta como uma pergunta independente. "
                   "Use o histórico da conversa como contexto, mas não responda ainda."),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ])
    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q)

    # Prompt de QA final
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", "Responda usando apenas o contexto fornecido. "
                   "Se não houver informação suficiente, diga que não encontrou nos documentos."),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}\n\n[Contexto]\n{context}")
    ])
    doc_chain = create_stuff_documents_chain(llm, qa_prompt)

    # Cadeia final de conversa
    conversa_chain = create_retrieval_chain(history_aware_retriever, doc_chain)

    return conversa_chain


def user_input(pergunta_user):
    if not st.session_state.conversa:
        st.error("Envie os PDFs e clique em Enviar para iniciar a conversa.")
        return

    # 1) Registra a pergunta no histórico (UI + cadeia)
    st.session_state.messages.append(("human", pergunta_user))
    st.session_state.chat_history.append(HumanMessage(content=pergunta_user))

    # 2) Invoca a cadeia (use a chave 'input' e passe o chat_history)
    resp = st.session_state.conversa.invoke({
        "input": pergunta_user,
        "chat_history": st.session_state.chat_history
    })
    answer = resp["answer"]

    # 3) Registra a resposta no histórico
    st.session_state.messages.append(("ai", answer))
    st.session_state.chat_history.append(AIMessage(content=answer))

    # 4) Renderiza todo o histórico (ou só a última resposta, se preferir)
    for role, content in st.session_state.messages:
        template = user_template if role == "human" else bot_template
        st.write(template.replace("{{MSG}}", content), unsafe_allow_html=True)



def main():
    load_dotenv() #garante que a api key vai ser carregada

    ##Criando a interface visual
    st.set_page_config(page_title='Conversando com Múltiplos PDFs', page_icon=':books:') #Título da página

    st.write(css, unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []          # para renderizar na UI (tuplas)
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []      # para a cadeia (LangChain Messages)
    if "conversa" not in st.session_state:
        st.session_state.conversa = None
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None

    st.header('Conversando com Múltiplos PDFs :books:')
    pergunta_user = st.text_input('Digite uma pergunta a respeito de seus documentos:')

    if pergunta_user:
        user_input(pergunta_user)

    with st.sidebar: #Função para criação e multiplas alterações da barra lateral (subtítulo da barra lateral, mensagem para inserção de arquivos e botão para )
        st.subheader('Seus Documentos') 
        pdfs = st.file_uploader('Insira seus PDFs aqui: ', accept_multiple_files=True, type='pdf') #permite inserir multiplos arquivos e limitando apenas a uploads de pdf
        if st.button('Enviar'):
            with st.spinner('Enviando...'):
                texto_bruto = juntar_texto(pdfs)

                chunks_texto = separar_chunks(texto_bruto)

                vectorstore = montar_vectorstore(chunks_texto)

                st.session_state.vectorstore = vectorstore
                st.session_state.conversa = continua_conversa(st.session_state.vectorstore)
                st.success("Documento pronto!")

    



if __name__ == "__main__": 
    main()


