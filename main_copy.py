import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate
from tec_docs import *
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from system_messages import *
import os

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
tecnicos = ['(Selecione um técnico)','Sika', "MC Bauchemie", "Viapol", "Vedacit", "Dryko", "Denver"]

if 'tecnico_selecionado' not in st.session_state:
    st.session_state['tecnico_selecionado'] = None
if 'chat_memory' not in st.session_state:
    st.session_state['chat_memory'] = ConversationBufferMemory()

#configuração da side bar
def sidebar():
  st.sidebar.image('./img/logo.jpg')
  tabs = st.sidebar.tabs(['Técnicos'])
  with tabs[0]:
    tecnico = st.sidebar.selectbox('Lista de técnicos', tecnicos)
    confirm = st.sidebar.button("Confirmar", type='primary')

  #configuração para parecer a primeira mensagem e de reset do histórico
  if tecnico != '(Selecione um técnico)' and tecnico != st.session_state['tecnico_selecionado'] and confirm:
        st.session_state['chat_memory'] = ConversationBufferMemory()  # Resetar a memória
        st.session_state['tecnico_selecionado'] = tecnico
        st.session_state['tecnico'] = tecnico
        mensagem = f'Seja bem-vindo a VX AI! Sou seu técnico em impermeabilização especialista dos produtos {tecnico}. Em que posso ajudar hoje?'
        st.session_state['chat_memory'].chat_memory.add_ai_message(mensagem)
        st.rerun()

#função para tratar do funcionamento e memória do chat
def chat():
  tec = st.session_state.get('tecnico')

  for msg in st.session_state['chat_memory'].chat_memory.messages:
        if msg.type == "human":
            st.chat_message("user").write(msg.content)
        elif msg.type == "ai":
            st.chat_message("assistant").write(msg.content)
       
  input_human = st.chat_input('Coloque aqui sua dúvida')

  #se o usuário digitar algo novo, precisamos que isso apareça no histórico também
  #então adicionamos essa mensagem em nossa lista inicial
  if input_human:
    st.session_state['input_human']=input_human
    chain_tec(tec)
       
    chain = st.session_state.get('chain')
    chat = st.chat_message('human')
    chat.markdown(input_human)

    chat = st.chat_message('ai')
    awnser = chat.write_stream(chain.stream({
      "input": input_human,
      "chat_history": st.session_state['chat_memory']
      })) 
    st.session_state['chat_memory'].chat_memory.add_user_message(input_human)
    st.session_state['chat_memory'].chat_memory.add_ai_message(awnser)

# Função para fazer o procedimento de RAG
def pdf_load(documentos, input_human):

  fichas = []
  hf_embeedings_model = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')

  for pdf_path in documentos:
        # Carregar documento
        loader = PyPDFLoader(pdf_path)
        fichas.extend(loader.load())
  
  vectordb = FAISS.from_documents(documents=fichas, embedding=hf_embeedings_model)
  retriever = vectordb.as_retriever()
  relevant_docs = retriever.invoke(input_human)  # Recuperar contexto relevante
  context = "\n".join([doc.page_content for doc in relevant_docs]) 
 
  return context

#configuração da chain
def chain_tec(tec):
    input_user = st.session_state.get('input_human')
    if input_user== None:
       input_user = ''

    chat = ChatGroq(model='llama3-8b-8192', api_key='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')

    if tec == 'Sika':
      system_message = sika_message.format(context=pdf_load(documentos_Sika, input_user))

    if tec == 'MC Bauchemie':
       system_message = mc_message.format(context=pdf_load(documentos_mc, input_user))
    
    if tec == 'Viapol':
      system_message = viapol_message.format(context=pdf_load(documentos_viapol, input_user))

    if tec == 'Vedacit':
       system_message = vedacit_message.format(context=pdf_load(documentos_vedacit, input_user))

    if tec == 'Denver':
      system_message = denver_message.format(context=pdf_load(documentos_denver, input_user))

    if tec == 'Dryko':
       system_message = dryko_message.format(context=pdf_load(documentos_dryko, input_user))

    template = ChatPromptTemplate.from_messages([('system', system_message), 
                                                ('placeholder', '{{chat_history}}'), 
                                                ('user', '{input}'),
                                                ])
    chain = template | chat
    st.session_state['chain'] = chain

def main():
  st.header('Seja Bem-vindo a VX AI!', divider="red")
  chat()
  sidebar()

if __name__ == '__main__':
  main()