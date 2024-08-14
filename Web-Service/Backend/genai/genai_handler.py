from openai import OpenAI
import os
# genai.configure(api_key=os.getenv('gemini_key'))

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Initialize the OpenAI LLM
fine_tuned_llm = ChatOpenAI(model_name="ft:gpt-3.5-turbo-0125:personal::9tpkCK91", openai_api_key=os.getenv('openai_key'))

llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=os.getenv('openai_key'))

# client = OpenAI(api_key=os.getenv('openai_key'))
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a fashion designer hlping clients coming to you",
        ),
        ("human", "{input}"),
    ]
)
    
def call_openai_api(input_text):    

    try:
        chain = prompt | llm
        message = chain.invoke(
            {
                "input": input_text,
            }
        )
        return message.content
        # response = client.chat.completions.create(
        #     model="gpt-3.5-turbo",
        #     messages = [
        #         {
        #         "role": "user",
        #         "content": input_text
        #         }]
        # )

        # return response.choices[0].message.content
    except Exception as e:
        print(str(e))
        # print(response.prompt_feedback)
        return "what products are you looking for ?"

def call_fine_tuned_openai_api(input_text):    

    try:
        chain = prompt | fine_tuned_llm
        message = chain.invoke(
            {
                "input": input_text,
            }
        )
        return message.content
        
    except Exception as e:
        print(str(e))
        return "what products are you looking for ?"