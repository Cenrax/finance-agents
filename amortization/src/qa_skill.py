from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient
from src.tools.tools_read_pdf import read_pdf, read_pdf_and_answer_questions
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
)

pdf_agent = AssistantAgent(
    name="assistant",
    model_client=model_client,
    tools=[read_pdf, read_pdf_and_answer_questions],
    system_message="Use tools to find specific answers to questions about PDF documents. Do not return the entire PDF content.",
)

# List of questions
questions = [
    "Does the lease transfer ownership of the underlying asset to the lessee by the end of the lease term?",
    "Does the lease grant the lessee an option to purchase the underlying asset that the lessee is reasonably certain to exercise?",
]

async def assistant_run() -> None:
    # Format the questions as a numbered list
    formatted_questions = "\n".join([f"{i+1}. {q}" for i, q in enumerate(questions)])
    
    # Call the custom function directly with the proper parameters
    try:
        
        response = await pdf_agent.on_messages(
            [TextMessage(
                content=f"Find specific answers to these questions from the PDF document. Do NOT return the entire document content:\n{formatted_questions}\nThe pdf file is located at data/agreement.pdf",
                source="user"
            )],
            cancellation_token=CancellationToken(),
        )
        print("Answers to your questions:")
        print(response)
    except Exception as e:
        print(f"Error extracting answers: {str(e)}")
        
        # Fallback: Use the agent approach if the direct function call fails
        print("\nTrying alternative approach...")
        answers = await read_pdf_and_answer_questions(
            pdf_path="data/agreement.pdf",
            questions=formatted_questions
        )
        print(answer)

if __name__ == "__main__":
    asyncio.run(assistant_run())
