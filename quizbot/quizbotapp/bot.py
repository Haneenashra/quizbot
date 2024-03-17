from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST

def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses

def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    # Retrieve the correct answer for the current question
    correct_answer = PYTHON_QUESTION_LIST[current_question_id]['answer']

    # Validate the user's answer
    if answer.strip().lower() == correct_answer.lower():
        # Store the user's answer in the session
        session['answers'][current_question_id] = answer.strip().lower()
        return True, ""  # Success
    else:
        return False, "Sorry, your answer is incorrect. Please try again."  # Error

def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    total_questions = len(PYTHON_QUESTION_LIST)

    # Check if current_question_id is valid and not the last question
    if current_question_id is None or current_question_id < total_questions - 1:
        next_question_id = current_question_id + 1
        next_question = PYTHON_QUESTION_LIST[next_question_id]['question']
        return next_question, next_question_id
    else:
        # If current_question_id is the last question, return None
        return None, -1

def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    answers = session.get('answers', {})
    total_questions = len(PYTHON_QUESTION_LIST)
    correct_answers = 0

    # Calculate the number of correct answers
    for question_id, question_data in enumerate(PYTHON_QUESTION_LIST):
        if question_id in answers and answers[question_id] == question_data['answer']:
            correct_answers += 1

    # Calculate the score
    score = (correct_answers / total_questions) * 100

    # Format the final response message
    final_response = f"Congratulations! You have completed the quiz.\n"
    final_response += f"Total questions: {total_questions}\n"
    final_response += f"Correct answers: {correct_answers}\n"
    final_response += f"Your score: {score:.2f}%\n"

    return final_response
