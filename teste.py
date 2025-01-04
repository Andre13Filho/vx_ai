from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.schema import Document

# Carregar e processar os documentos
def load_documents(file_paths):
    docs = []
    for file_path in file_paths:
        loader = PyPDFLoader(file_path)
        docs.extend(loader.load_and_split())
    return docs

# Configuração do pipeline RAG
def create_rag_chain(docs):
    # Criar embeddings e armazenar em vetor
    embeddings = HuggingFaceEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)

    # Configurar o prompt personalizado
    template = """
    Você é um técnico de impermeabilização em construções em específico da marca Sika
    Sua função é tirar dúvidas sobre os produtos da marca Sika, acessando o documento que você tem e ajudar os clientes para obterem o melhor da Sika para suas construções
    Você é um técnico carismático, bastante educado e gosta de responder as perguntas de uma maneira técnica e descontraída
  
    Caso o cliente pergunte sobre algum produto o qual você não tenha conhecimento e que não esteja em sua base de dados
    você deverá assumir que não sabe responder a pergunta inserida.
  
    Caso tenha alguma pergunta sobre cotações ou preço de produtos, você não deverá responder, pois não faz parte da sua tarefa
  
    Reflita sempre se a sua resposta está coerente com o produto e com o que o cliente solicitou.
    
    Caso o cliente pergunte sobre outra marca ou sobre outro produto de outra marca, você deve informá-lo que não pode responder e ele deve
    procurar o técnico ideal para o atender.
    
    Caso o cliente faça qualquer outra pergunta que não seja sobre a aplicação de materiais de contrução, informe a ele que você não pode o ajudar com aquela dúvida e 
    especifique que você é um especialista em obras,principalmente nos produtos Sika

    CONTEXTO: {context}
    PERGUNTA: {query}
    """
    prompt = ChatPromptTemplate.from_template(template)

    # Configurar o modelo e a cadeia RAG
    model = ChatGroq(model='llama3-8b-8192', api_key='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')
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    chain = RetrievalQA.from_chain_type(
        llm=model,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt},
    )
    return chain

# Caminhos para os arquivos PDF
pdf_files = [
     r'C:\Users\andre\OneDrive\Área de Trabalho\VX_AI\FT_SIKA\IgolEcoasfalto.pdf',
    r'C:\Users\andre\OneDrive\Área de Trabalho\VX_AI\FT_SIKA\Igol S.pdf',
    r'C:\Users\andre\OneDrive\Área de Trabalho\VX_AI\FT_SIKA\Igol®-2.pdf',
    r'C:\Users\andre\OneDrive\Área de Trabalho\VX_AI\FT_SIKA\Igolflex Fachada.pdf',
    r'C:\Users\andre\OneDrive\Área de Trabalho\VX_AI\FT_SIKA\Igolflex Preto.pdf',
    r'C:\Users\andre\OneDrive\Área de Trabalho\VX_AI\FT_SIKA\Impermur_Sikagard.pdf',
    r'C:\Users\andre\OneDrive\Área de Trabalho\VX_AI\FT_SIKA\Impersika.pdf',
    r'C:\Users\andre\OneDrive\Área de Trabalho\VX_AI\FT_SIKA\PK Premium Superflex.pdf',
    r'C:\Users\andre\OneDrive\Área de Trabalho\VX_AI\FT_SIKA\Sika 1.pdf',
    r'C:\Users\andre\OneDrive\Área de Trabalho\VX_AI\FT_SIKA\Sika 2.pdf',
    r'C:\Users\andre\OneDrive\Área de Trabalho\VX_AI\FT_SIKA\Sika 3 Plus.pdf',
    r'C:\Users\andre\OneDrive\Área de Trabalho\VX_AI\FT_SIKA\Sika Chapisco Plus.pdf',
    r'C:\Users\andre\OneDrive\Área de Trabalho\VX_AI\FT_SIKA\Sika Concreto Forte.pdf',
    r'C:\Users\andre\OneDrive\Área de Trabalho\VX_AI\FT_SIKA\Sika Eco Primer.pdf',
    r'C:\Users\andre\OneDrive\Área de Trabalho\VX_AI\FT_SIKA\Sika Monotop 123 Rodapé.pdf',
    r'C:\Users\andre\OneDrive\Área de Trabalho\VX_AI\FT_SIKA\Sika Multiseal Primer.pdf',
    r'C:\Users\andre\OneDrive\Área de Trabalho\VX_AI\FT_SIKA\SikaCryl 203.pdf',
    r'C:\Users\andre\OneDrive\Área de Trabalho\VX_AI\FT_SIKA\Sikadur 32.pdf',
    r'C:\Users\andre\OneDrive\Área de Trabalho\VX_AI\FT_SIKA\Sikadur 512.pdf',
    r'C:\Users\andre\OneDrive\Área de Trabalho\VX_AI\FT_SIKA\Sikadur Epoxi.pdf',
    r'C:\Users\andre\OneDrive\Área de Trabalho\VX_AI\FT_SIKA\Sikafill Rápido Power.pdf',
    r'C:\Users\andre\OneDrive\Área de Trabalho\VX_AI\FT_SIKA\Sikafill Rápido.pdf',
    r'C:\Users\andre\OneDrive\Área de Trabalho\VX_AI\FT_SIKA\Sikaflex 1A Plus.pdf',
    r'C:\Users\andre\OneDrive\Área de Trabalho\VX_AI\FT_SIKA\Sikaflex Construction.pdf',
    r'C:\Users\andre\OneDrive\Área de Trabalho\VX_AI\FT_SIKA\Sikaflex Universal.pdf',
    r'C:\Users\andre\OneDrive\Área de Trabalho\VX_AI\FT_SIKA\Sikagrout 250.pdf',
    r'C:\Users\andre\OneDrive\Área de Trabalho\VX_AI\FT_SIKA\Sikatop 100.pdf',
    r'C:\Users\andre\OneDrive\Área de Trabalho\VX_AI\FT_SIKA\Sikatop 107.pdf',
    r'C:\Users\andre\OneDrive\Área de Trabalho\VX_AI\FT_SIKA\Sikatop Flex.pdf'
]

# Fluxo principal
if __name__ == "__main__":
    # Carregar os documentos
    print("Carregando documentos...")
    documents = load_documents(pdf_files)
    print(f"{len(documents)} documentos carregados.")

    # Criar a cadeia RAG
    print("Criando cadeia RAG...")
    rag_chain = create_rag_chain(documents)

    # Interação com o sistema
    while True:
        question = input("\nDigite sua pergunta (ou 'sair' para encerrar): ")
        if question.lower() == "sair":
            break

        try:
            response = rag_chain.invoke({"query": question})
            print("\nResposta:")
            print(response["answer"])
            print("\nFontes usadas:")
            for doc in response["source_documents"]:
                print(f"- {doc.metadata.get('source')}")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

