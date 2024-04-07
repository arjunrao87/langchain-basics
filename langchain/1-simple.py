from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Simple chain invocation
## LLM + Prompt
llm = Ollama(model="mistral")
output = StrOutputParser()
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a skilled technical writer.",
        ),
        ("human", "{user_input}"),
    ]
)
chain = prompt | llm | output

## Winner winner chicken dinner
response = chain.invoke({"user_input": "how can langsmith help with testing?"})
print(":::ROUND 1:::")
print(response)
