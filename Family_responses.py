import random


def family():
    response = ["yadfsfsd","ewwaffgddas"][
        random.randrange(2)]
    return response


def unknown():
    response = ["Could you please re-phrase that? ",
                "...",
                "Sounds about right.",
                "What does that mean?"][
        random.randrange(4)]
    return response