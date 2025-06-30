from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

openai_api_key = "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"

def generate_resume(user_input: str):
    prompt = PromptTemplate(
        input_variables=["experience"],
        template="""
You are a professional resume writer. Based on the following user input, generate a strong ATS-friendly resume in bullet-point format. Include relevant sections like Summary, Skills, Experience, and Education.

User Input:
{experience}

Return the resume in markdown format.
        """
    )

    llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)
    chain = LLMChain(llm=llm, prompt=prompt)

    response = chain.run({"experience": user_input})
    return response
