def from_request_to_format_data(res_answer, res_question):
    data = {}

    q_id = res_answer['question_id']
    a_id = res_answer['answer_id']
    data['answer_id'] = res_answer['answer_id']
    data['question_id'] = q_id

    data['is_accepted'] = res_answer['is_accepted']
    data['answer_score'] = res_answer['score']
    data['answer_last_activity_date'] = res_answer['last_activity_date']
    data['answer_creation_date'] = res_answer['creation_date']
    data['answer_body'] = res_answer['body']

    data['tags'] = res_question['tags']
    data['is_answered'] = res_question['is_answered']
    data['question_view_count'] = res_question['view_count']
    data['answer_count'] = res_question['answer_count']
    data['question_score'] = res_question['score']
    data['question_last_activity_date'] = res_question['last_activity_date']
    data['question_creation_date'] = res_question['creation_date']
    data['question_title'] = res_question['title']
    data['question_body'] = res_question['body']

    return data