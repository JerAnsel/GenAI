import os
import dotenv
import openai

def setup() -> str:
    key = os.environ.get("OPENAI_KEY", None)
    if not key:
        print("Error: An OpenAI API key must be supplied as an environment variable to continue.") 
        raise EnvironmentError("An OpenAI API key must be supplied as an environment variable to continue.")
    openai.api_key = key

    camp_details_prompt = ("Create a fictional Summer Camp named GenAI. Describe in detail"
                           " everything the camp offers, as well as camp values, policies, location, dates,"
                           " pricing, and age range.")

    camp_details = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": camp_details_prompt}],
        temperature=0
        )["choices"][0]["message"]["content"]

    return camp_details

def routing(user_message: str) -> str:

    routing_prompt = ("You are an assistant tasked with helping users sign up for a summer camp. Given the following message "
                      "from a user, determine whether they are asking for information about the summer camp or are "
                      "discussing registration for said camp. Respond with a single word, either 'info' or 'registration' "
                      "respectively.  The message: ")

    route = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": routing_prompt + user_message}],
        temperature=0
        )["choices"][0]["message"]["content"]
    
    return route

def answer_question(user_message: str, camp_details: str, conversation_history: list[dict]) -> str:
    
    info_prompt = ("You are an assistant tasked with answering questions about a fictitious summer camp with the following details:\n"
                   f"{camp_details}")
    
    answer = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages= [{"role": "user", "content": info_prompt}] + conversation_history
                  + [{"role": "user", "content": (f"Answer the following question about the summer camp: {user_message} If the answer is not provided in the "
                  "camp details refer them to the camp website. If there are any queries unrelated to the camp state that you "
                  "cannot help with that topic.")}],
        temperature=0
        )["choices"][0]["message"]["content"]
 
    print(f"GenAI Chatbot: {answer}")
    return answer
    

def register_user(user_message: str, camp_details: str, conversation_history: list[dict]) -> str:

    registration_prompt = ("You are an assistant tasked with registering children to a fictitious summer camp. The following details are "
                   "required for registration: Child's Name, Age, Dietary Restrictions, Parent's Name, Parent's Phone Number and "
                   "Parent's Email.")
    
    answer = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation_history + [{"role": "user", "content": registration_prompt + user_message}],
        temperature=0
        )["choices"][0]["message"]["content"]
    
    print(f"GenAI Chatbot: {answer}")
    return answer

def create_message(user: bool, content: str) -> dict:
    return {"role": "user" if user else "assistant", "content": content}

if __name__ == '__main__':

    dotenv.load_dotenv()
    camp_details = setup()
    conversation_history = []
    print(camp_details)
        
    while True:
        user_message = input("User: ")
        conversation_history.append(create_message(user=True, content=user_message))
        route = routing(user_message=user_message)

        if route == 'info':
            response = answer_question(user_message=user_message, camp_details=camp_details, conversation_history=conversation_history)
            conversation_history.append(create_message(False, response))

        elif route == 'registration':
            response = register_user(user_message=user_message, camp_details=camp_details, conversation_history=conversation_history)
            conversation_history.append(create_message(False, response))
        
        else:
            response = "Sorry, I can only help with topics related to GenAI summer camp. Is there anything else I can help you with?"
