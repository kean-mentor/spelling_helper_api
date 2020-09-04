import random


question_mode = ['is_correct', 'fill_empty']
letters = ['j', 'ly']

def prepare_questions(total, words):
    questions = []

    question_words = random.sample(words, min(total, len(words)))
    for word in question_words:
        qm = random.choice(question_mode)
        if qm == 'is_correct':
            trivia = word.replace('j', random.choice(letters)).replace('ly', random.choice(letters))
        else:
            trivia = word.replace('j', '_').replace('ly', '_')
        questions.append(trivia)

    return questions

def check_answers(original, answers, words):
    result = []

    for idx in range(len(original)):
        if "_" in original[idx]:  # Question mode: fill_empty
            temp = original[idx].replace("_", answers[idx])
            result.append(temp in words)
        else:  # Question mode: is_correct
            if answers[idx] in (True, 1, '1', 'yes', 'y', 'ok'):
                result.append(original[idx] in words)
            else:
                result.append(original[idx] not in words)

    return result
