# Chatbot - Leitura de Múltiplos PDFs
📚 Conversando com Múltiplos PDFs

Este projeto implementa um chatbot interativo baseado em Inteligência Artificial que permite ao usuário enviar múltiplos arquivos PDF e fazer perguntas em linguagem natural sobre o conteúdo.

A aplicação utiliza Processamento de Linguagem Natural (PLN) e técnicas de RAG (Retrieval-Augmented Generation) para recuperar trechos relevantes dos documentos e gerar respostas contextualizadas.

🚀 Funcionalidades

- Upload de múltiplos PDFs.

- Extração automática de texto dos documentos.

- Divisão do conteúdo em chunks para melhor indexação.

- Criação de embeddings semânticos com modelos da OpenAI ou Hugging Face (ex.: Qwen3-Embedding).

- Armazenamento vetorial com FAISS para busca por similaridade.

- Respostas conversacionais utilizando LLMs (ex.: ChatGPT / GPT-4o-mini).

- Histórico de conversas mantido durante a sessão no Streamlit.

🛠️ Tecnologias utilizadas

- Python

- Streamlit
 (interface web)

- LangChain
 (orquestração de LLMs e RAG)

- OpenAI e Hugging Face
 (modelos de embeddings e LLMs)

- FAISS
 (busca vetorial eficiente)

- PyPDF2
 (extração de texto de PDFs)

📂 Estrutura do projeto

├── app.py              # Código principal da aplicação (Streamlit)

├── htmlTemplates.py    # Templates de exibição no chat

├── requirements.txt    # Dependências do projeto

└── README.md           # Documentação

▶️ Como executar

Clone este repositório:

git clone https://github.com/seu-usuario/conversando-pdfs.git
cd conversando-pdfs


Crie um ambiente virtual e instale as dependências:

pip install -r requirements.txt


Configure suas chaves de API no arquivo .env:

OPENAI_API_KEY=your_openai_key
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token


Rode a aplicação:

streamlit run app.py

💡 Exemplos de uso

Perguntar sobre artigos científicos em PDF.

Criar resumos automáticos de relatórios.

Usar como assistente pessoal para documentos acadêmicos ou técnicos.
