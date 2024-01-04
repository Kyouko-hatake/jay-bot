import json
import io
import nltk
from difflib import get_close_matches
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob
import spacy

nltk.download('punkt')
nltk.download('stopwords')
nlp = spacy.load("fr_core_news_sm")

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        data: dict = json.load(file)
    return data

memory = []
history = []

stop_words = set(stopwords.words('french'))
stemmer = SnowballStemmer('french')
vectorizer = TfidfVectorizer()
knowledge_base = load_knowledge_base('knowledge_base.json')
questions_text = [q["question"] for q in knowledge_base["questions"]]
vectorizer.fit(questions_text)
current_context = {"last_question": None, "last_answer": None}

def get_intent(user_input):
    doc = nlp(user_input)
    return doc.cats

def preprocess_text(text):
    words = word_tokenize(text.lower())
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
    stemmed_words = [stemmer.stem(word) for word in filtered_words]
    return ' '.join(stemmed_words)

def calculate_similarity(question1, question2):
    question1_vector = vectorizer.transform([question1])
    question2_vector = vectorizer.transform([question2])
    similarity = cosine_similarity(question1_vector, question2_vector)
    return similarity[0][0]

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    user_question_processed = preprocess_text(user_question)
    best_match = max(questions, key=lambda question: calculate_similarity(user_question_processed, question))
    similarity = calculate_similarity(user_question_processed, best_match)
    return best_match if similarity > 0.5 else None

def ajouter_nouvelle_question_et_memoire(user_input: str, knowledge_base: dict, memory: list):
    nouvelle_question = user_input
    nouvelle_reponse = input("Nouvelle réponse : ")
    knowledge_base["questions"].append({"question": nouvelle_question, "answer": nouvelle_reponse})
    save_knowledge_base('knowledge_base.json', knowledge_base)
    memory.append({"question": nouvelle_question, "answer": nouvelle_reponse})

    print("Jay: Merci, Hikari! J'ai appris une nouvelle réponse!")

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]

def get_answer(user_input: str, knowledge_base: dict, memory: list) -> None:
    blob = TextBlob(user_input)
    user_intent = get_intent(user_input)
    best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

    if "greeting" in user_intent:
        print("Jay: Bonjour! Comment puis-je t'aider aujourd'hui?")
    elif "farewell" in user_intent:
        print("Jay: Au revoir! Reviens bientôt.")
    elif best_match:
        current_context["last_question"] = best_match
        answer = get_answer_for_question(best_match, knowledge_base)
        current_context["last_answer"] = answer
        print(f'Jay: {answer}')
    elif "preferences" in user_intent:
        print("Jay: Mes préférences ? Je suis passionné par la musique, surtout le metal. Et toi?")
    else:
        sentiment = blob.sentiment.polarity

        if sentiment > 0.5:
            print("Jay: Tu sembles de bonne humeur !")
        elif sentiment < -0.5:
            print("Jay: Est-ce que quelque chose ne va pas ?")
        else:
            print("Jay: Je ne comprends pas bien. Peux-tu reformuler?")

        for entry in memory:
            if entry["question"] in user_input:
                answer = entry["answer"]
                print(f"Jay: Je me souviens, la réponse est {answer}")
                enregistrer_interaction_dans_historique(user_input, answer, history)
                return

        print("Jay: Je ne connais pas la réponse. Peux-tu m'apprendre ?")
        new_answer = input('Tape la réponse ou "Passe" pour passer: ')

        if new_answer.lower() != 'passer':
            knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
            save_knowledge_base('knowledge_base.json', knowledge_base)
            memory.append({"question": user_input, "answer": new_answer})
            print(f"Jay: Merci, Hikari! J'ai appris une nouvelle réponse!")
            current_context["last_question"] = user_input
            current_context["last_answer"] = new_answer
            enregistrer_interaction_dans_historique(user_input, new_answer, history)

    get_answer_for_question(user_input, knowledge_base)

def enregistrer_interaction_dans_historique(user_input: str, answer: str, history: list):
    history.append({"user_input": user_input, "answer": answer})

def chat_bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    while True:
        user_input: str = input('Hikari: ')

        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'apprendre':
            ajouter_nouvelle_question_et_memoire(user_input, knowledge_base, memory)
            continue

        get_answer(user_input, knowledge_base, memory)

if __name__ == '__main__':
    chat_bot()