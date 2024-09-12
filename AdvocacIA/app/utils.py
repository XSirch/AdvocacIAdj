from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from django.conf import settings
from langchain_core.messages import HumanMessage

def gerar_e_verificar_documento(cliente, servico, data, detalhes, model="gpt-4o-mini-2024-07-18"):
    """
    Gera e verifica um documento jurídico usando LangChain e a API do OpenAI.
    """
    # Verifique se a chave da API está configurada corretamente
    if not settings.OPENAI_API_KEY:
        raise ValueError("OpenAI API key is not set. Please check your environment variables.")
    
    # Instancie o modelo de chat com a chave da API
    llm = ChatOpenAI(api_key=settings.OPENAI_API_KEY, model_name=model)
    
    # Define o template de prompt para gerar o documento
    generate_prompt = PromptTemplate.from_template(
        "Você é um assistente jurídico especializado em criar documentos legais. Crie um {servico} para o cliente {cliente} com data {data}. Detalhes do caso: {detalhes}. Pesquise na internet por processos similares e leis para ter suporte jurídico."
    )
    
    # Gera o documento usando o método invoke
    mensagem_gerar = HumanMessage(content=generate_prompt.format(cliente=cliente, servico=servico, data=data, detalhes=detalhes))
    resultado_gerar = llm.invoke([mensagem_gerar])
    documento_gerado = resultado_gerar.content.strip()
    
    # Define o template de prompt para verificar o documento
    verification_prompt = PromptTemplate.from_template(
        "Verifique o seguinte documento jurídico para garantir que ele faz sentido no contexto jurídico e contém referências adequadas às leis: \n\n{documento}\n\n"
        "Responda 'Aprovada, sem novas observações' se a peça é adequada, ou 'Não' se não for. "
        "Caso a resposta seja 'Não', justifique e sugira quais pontos ou leis devem ser revisadas."
    )
    
    # Verifica o documento usando o método invoke
    mensagem_verificar = HumanMessage(content=verification_prompt.format(documento=documento_gerado))
    resultado_verificar = llm.invoke([mensagem_verificar])
    verificacao = resultado_verificar.content.strip()
    
    return documento_gerado, verificacao, generate_prompt.template