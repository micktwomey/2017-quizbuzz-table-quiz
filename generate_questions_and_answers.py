
import collections
from pprint import pprint

QuestionAndAnswer = collections.namedtuple("QuestionAndAnswer", "question answer")

QUESTION_TEMPLATE = """{qa.question}

"""

ROUND_TEMPLATE = """theme: Zurich, 4

# Round {round}

---

{questions}

---

# End of Round!

## Pass Answer Sheets to the Next Team

"""

ANSWER_TEMPLATE="""{qa.question}

{qa.answer}

"""

QUESTION_AND_ANSWER_TEMPLATE="""theme: Zurich, 4

# Round {round} Answers

---

{answers}

---

# End of Answers!

## Pass the Answer Sheets to the Quizmasters

"""

EXTRAS = {

}

def parse_question(question_and_asnwer):
    return [x.strip() for x in re.split("#+", question_and_asnwer.strip()) if x.strip()][0]

def parse(buffer):
    current = None
    for line in buffer:
        if line.strip() == "---":
            if current is not None:
                question = [current[0]]
                answer = None
                for index, part in enumerate(current[1:]):
                    if part.strip().startswith("#"):
                        answer = current[index+1:]
                        break
                    question.append(part)
                yield QuestionAndAnswer("\n".join(question), "\n".join(answer) if answer else "")
            current = []
        else:
            if line.strip() and current is not None:
                print(repr(line.strip()))
                current.append(line.strip())


def split_into_rounds(questions_and_answers, round_length=10):
    round = []
    for i, question_and_answer in enumerate(questions_and_answers):
        if (i % round_length == 0 and round) or question_and_answer.question.strip() == '# Tie Breakers':
            yield round
            round = []
        round.append(question_and_answer)
    yield round

def main():
    questions_and_answers = list(parse(open("all_questions.md", "r")))

    rounds = []
    for round, questions in enumerate(split_into_rounds(questions_and_answers)):
        pprint((round + 1, questions))
        question_text = "---\n\n".join(QUESTION_TEMPLATE.format(qa=qa) for qa in questions)
        answers_text = "---\n\n".join(ANSWER_TEMPLATE.format(qa=qa) for qa in questions)
        rounds.append((
            ROUND_TEMPLATE.format(
                round=round + 1,
                questions=question_text,
            ),
            QUESTION_AND_ANSWER_TEMPLATE.format(
                round=round + 1,
                answers=answers_text,
            )
        ))

    for i, (round, answers) in enumerate(rounds):
        i = i + 1
        with open("questions/round{}.md".format(i), "w") as buffer:
            buffer.write(round)
        with open("answers/round{}.md".format(i), "w") as buffer:
            buffer.write(answers)

if __name__ == '__main__':
    main()