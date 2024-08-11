import boto3
from io import BytesIO
from PyPDF2 import PdfReader

from langchain_community.llms.bedrock import Bedrock
from langchain.chains import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document


def get_bedrock_client(serviceName="bedrock-runtime", regionName="us-east-1"):
    bedrock_client = boto3.client(
        service_name=serviceName,
        region_name=regionName
    )
    return bedrock_client


def get_bedrock_model(modelID="ai21.j2-mid-v1", bedrock_client=get_bedrock_client()):
    llm = Bedrock(
        model_id=modelID,
        client=bedrock_client,
        model_kwargs={"maxTokens": 1000, "temperature": 0.0}
    )
    return llm


def load_documents(body):
    file_content = body.read()
    reader = PdfReader(BytesIO(file_content))
    documents = []
    for page in reader.pages:
        doc = Document(
            page_content=page.extract_text()
        )
        documents.append(doc)
    return documents


def get_summary(documents):
    prompt = PromptTemplate(
        input_variables=['input_doc'],
        template="summarize the following in two sentences or less. {input_doc}"
    )
    llm = get_bedrock_model()
    bedrock_chain = LLMChain(llm=llm, prompt=prompt)
    stuff_chain = StuffDocumentsChain(
        llm_chain=bedrock_chain, document_variable_name="input_doc")
    response = stuff_chain.invoke(documents)
    return response["output_text"]

