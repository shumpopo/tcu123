import random


def love():
    response = ["Confidence is attractive. Hold eye contact, smile, and show you're comfortable with yourself.",
                "A good sense of humor can go a long way. Playful teasing or witty remarks can make conversations fun.",
                "Show genuine interest by actively listening and responding to what they say. Ask questions and engage in the conversation.",
                "Sincere compliments about their personality, style, or achievements can make them feel special.",
                "Pay attention to your body language. Subtle gestures like leaning in, mirroring their movements, or gentle touches can create a connection.",
                "Pay attention to their reactions. If they seem uncomfortable or uninterested, respect their boundaries.",
                "Use subtle flirtatious gestures like maintaining eye contact, smiling, or a light touch on the arm if the situation allows.",
                "Authenticity is key. Let your true personality shine through rather than trying to be someone you're not."][
        random.randrange(7)]
    return response


def broken():
    response = ["Talk to your partner about how you're feeling. Sometimes, simply discussing your feelings openly can bring new perspectives and ideas.",
                "Explore new activities together. It could be a hobby, a class, or even a trip. Exploring something new can reignite excitement.",
                " Focus on personal growth, both individually and as a couple. This could involve setting goals, learning something new, or working on mutual interests."][
        random.randrange(3)]
    return response


def unknown():
    response = ["Could you please re-phrase that? ",
                "...",
                "Sounds about right.",
                "What does that mean?"][
        random.randrange(4)]
    return response
