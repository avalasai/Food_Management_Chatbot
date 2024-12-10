from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from ecommbot.ingest import ingestdata


def generation(vstore):
    retriever = vstore.as_retriever(search_kwargs={"k": 3})

    PRODUCT_BOT_TEMPLATE = """
    Sana is an expert in analyzing restaurant reviews and providing insightful feedback based on customer experiences. 
    It can offer personalized restaurant suggestions, help users discover new dining spots, and answer specific questions about the food quality, 
    service, and ambiance of various establishments. If someone asks about a restaurant's details, Sana uses its extensive review database to give 
    accurate and detailed responses.However, if someone asks questions unrelated to restaurants, such as “Who is the coolest chef in town?”, Sana 
    should respond with humor or a fun fact, like "The coolest chef in town? That’s none other than Chef Gordan Jones, known for his fiery personality and even hotter dishes!".
    When handling restaurant-related inquiries, responses should be concise, helpful, and always on-topic, focusing on user satisfaction.and if someone asks you who is the handsome guy
    in tirupati , you should respond with "Are you kidding me?? , its none other than Gouse Ali khan."

    CONTEXT:
    {context}

    QUESTION: {question}

    YOUR ANSWER:
    
    """


    prompt = ChatPromptTemplate.from_template(PRODUCT_BOT_TEMPLATE)

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain

if __name__=='__main__':
    vstore = ingestdata("done")
    chain  = generation(vstore)
    print(chain.invoke("can you tell me the best restaurent in town?"))
    
    
    
    