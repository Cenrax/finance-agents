from markitdown import MarkItDown
from dotenv import load_dotenv
import os
import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import UserMessage

load_dotenv()

model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
)
async def read_pdf(path: str) -> str:
    """Read the contents of the pdf file and returns in markdown"""
    md = MarkItDown() 
    result = md.convert(path)
    
    return result.text_content

async def read_pdf_and_answer_questions(pdf_path: str, questions: str) -> str:
    """Read a PDF and extract answers to specific questions"""
    # First, get the PDF content using the existing tool
    pdf_content = await read_pdf(pdf_path)
    
    # Create a prompt that instructs the model to find specific answers
    prompt = f"""
    I have a PDF document with the following content:
    
    {pdf_content}
    
    Please answer ONLY the following questions based on the document content. 
    For each question, provide a direct answer with the relevant section from the document:
    
    {questions}
    
    Format your response as:
    Question 1: [Question text]
    Answer: [Direct answer]
    Reference: [Relevant text from document]
    
    Question 2: [Question text]
    Answer: [Direct answer]
    Reference: [Relevant text from document]
    """
    
    # Use the model to extract the answers
    response = await model_client.create(
        [UserMessage(content=prompt, source="user")]
    )
    print(response)
    return response.content
