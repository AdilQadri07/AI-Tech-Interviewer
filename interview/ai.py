import random, requests, re
from django.conf import settings
from google import genai
from google.genai import Client

client = genai.Client(api_key=settings.GEMINI_API_KEY)

QUESTION_BANK = {

    "HTML": [
        "What is HTML?",
        "What are semantic HTML tags?",
        "Difference between div and span?",
        "What is the purpose of doctype?",
        "Difference between inline and block elements?",
        "What are HTML attributes?",
        "What is the alt attribute?",
        "What are meta tags?",
        "Difference between id and class?",
        "What is accessibility in HTML?",
        "Difference between section and article?",
        "What is HTML5?",
        "What is local storage?",
        "What is session storage?",
        "What is iframe?",
        "What is form validation?",
        "Difference between GET and POST?",
        "What is canvas tag?",
        "What is SEO friendly HTML?",
        "What are data attributes?",
        "What is header tag?",
        "What is footer tag?",
        "What is nav tag?",
        "What is strong tag?",
        "What is em tag?",
        "What is label tag?",
        "What is placeholder attribute?",
        "What is required attribute?",
        "What is role attribute?",
        "What is web accessibility?"
    ],

    "CSS": [
        "What is CSS?",
        "Difference between margin and padding?",
        "What is box model?",
        "What is Flexbox?",
        "What is Grid?",
        "Difference between Flexbox and Grid?",
        "What is responsive design?",
        "What are media queries?",
        "What is position property?",
        "Difference between absolute and relative?",
        "What is z-index?",
        "What is display property?",
        "Difference between none and hidden?",
        "What is pseudo class?",
        "What is pseudo element?",
        "What is specificity?",
        "What is !important?",
        "What is rem and em?",
        "What is vh and vw?",
        "What is overflow?",
        "What is opacity?",
        "What is transform?",
        "What is transition?",
        "What is animation?",
        "What is background-size cover?",
        "What is object-fit?",
        "What is flex-wrap?",
        "What is align-items?",
        "What is justify-content?",
        "What is CSS variable?"
    ],

    "JavaScript": [
        "What is JavaScript?",
        "Difference between var let and const?",
        "What is hoisting?",
        "What is closure?",
        "What is DOM?",
        "What is event bubbling?",
        "What is event delegation?",
        "Difference between == and ===?",
        "What is promise?",
        "What is async await?",
        "What is callback?",
        "What is arrow function?",
        "What is this keyword?",
        "What is prototype?",
        "What is JSON?",
        "What is localStorage?",
        "What is sessionStorage?",
        "What is map function?",
        "What is filter function?",
        "What is reduce function?",
        "What is spread operator?",
        "What is rest operator?",
        "What is destructuring?",
        "What is NaN?",
        "What is setTimeout?",
        "What is setInterval?",
        "What is event loop?",
        "What is scope?",
        "What is lexical scope?",
        "What is ES6?"
    ],

    "Python": [
        "What is Python?",
        "What are Python features?",
        "What are data types in Python?",
        "Difference between list and tuple?",
        "What is dictionary?",
        "What is set?",
        "What is function?",
        "What is lambda function?",
        "What is list comprehension?",
        "What is generator?",
        "What is iterator?",
        "What is OOP?",
        "What is class?",
        "What is object?",
        "What is inheritance?",
        "What is polymorphism?",
        "What is encapsulation?",
        "What is abstraction?",
        "Difference between == and is?",
        "What is mutable and immutable?",
        "What is exception handling?",
        "What is try except?",
        "What is module?",
        "What is package?",
        "What is pip?",
        "What is virtual environment?",
        "What is self keyword?",
        "What is __init__?",
        "What is decorator?",
        "What is multithreading?"
    ],

    "Django": [
        "What is Django?",
        "Explain MVT architecture?",
        "What is Django ORM?",
        "What are models?",
        "What are views?",
        "What are templates?",
        "What is settings.py?",
        "What is urls.py?",
        "What is middleware?",
        "What is migration?",
        "What is makemigrations?",
        "What is migrate?",
        "What is admin panel?",
        "What is superuser?",
        "What is authentication?",
        "What is authorization?",
        "What is CSRF token?",
        "What is session?",
        "What is static files?",
        "What is media files?",
        "What is context processor?",
        "What is login_required?",
        "What is Django Rest Framework?",
        "What is serializer?",
        "What is API?",
        "What is class based view?",
        "What is function based view?",
        "What is signals?",
        "What is pagination?",
        "What is caching?"
    ],

    "MySQL": [
        "What is MySQL?",
        "What is primary key?",
        "What is foreign key?",
        "What is normalization?",
        "What is index?",
        "What is join?",
        "Types of joins?",
        "What is inner join?",
        "What is left join?",
        "What is right join?",
        "What is group by?",
        "What is having?",
        "Difference between where and having?",
        "What is aggregate function?",
        "What is count?",
        "What is sum?",
        "What is max?",
        "What is min?",
        "What is subquery?",
        "What is view?",
        "What is stored procedure?",
        "What is trigger?",
        "What is transaction?",
        "What is commit?",
        "What is rollback?",
        "What is ACID?",
        "What is constraint?",
        "What is unique constraint?",
        "What is not null?",
        "What is default?"
    ],

    "MongoDB": [
        "What is MongoDB?",
        "What is NoSQL?",
        "Difference between SQL and NoSQL?",
        "What is collection?",
        "What is document?",
        "What is BSON?",
        "What is indexing?",
        "What is aggregation?",
        "What is pipeline?",
        "What is replica set?",
        "What is sharding?",
        "What is ObjectId?",
        "What is find()?",
        "What is insertOne()?",
        "What is updateOne()?",
        "What is deleteOne()?",
        "What is projection?",
        "What is limit()?",
        "What is skip()?",
        "What is sort()?",
        "What is embedded document?",
        "What is reference?",
        "What is schema design?",
        "What is TTL index?",
        "What is capped collection?",
        "What is MongoDB Compass?",
        "What is Mongoose?",
        "What is aggregation match?",
        "What is aggregation group?",
        "What is lookup?"
    ],
}


def get_random_question_by_language(language, count=10):
    questions = QUESTION_BANK.get(language, [])

    if not questions:
        return []

    if len(questions) <= count:
        return questions

    return random.sample(questions, count)


def evaluate_full_interview(questions, answers):
    try:
        combined = ""

        for i, (q, a) in enumerate(zip(questions, answers), 1):
            combined += f"""
Question {i}: {q}
Candidate Answer {i}: {a}

"""

        prompt = f"""
You are a Senior FAANG-level Technical Interviewer.

Evaluate each answer strictly.

Rules:
- Score must be between 0 and 10
- Be realistic and critical
- Keep feedback concise (max 2 lines per question)

Format exactly like this:

Q1:
Score: <number>
Feedback: <text>

Q2:
Score: <number>
Feedback: <text>

...

After all questions add:

Overall Summary:
<4-5 lines professional hiring decision summary>

Interview Data:
{combined}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return response.text

    except Exception as e:
        import traceback
        print("GEMINI FULL INTERVIEW ERROR:")
        traceback.print_exc()
        return None