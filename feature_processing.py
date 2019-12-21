import re
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

code_token = {
            "short": "SHORTCODE",
            "long": "LONGCODE"
        }

url_token = "URL"
return_carriage_token = " RC "

# process html code
def html_2_text(html_doc):
    soup = BeautifulSoup(html_doc.lower(), 'html.parser')
    code_snippets = soup.find_all("code")
    for snippet in code_snippets:
        if snippet.text.count("\n") == 0:
            snippet.string = code_token["short"]
        else:
            snippet.string = code_token["long"]

    text_from_html = soup.text

    text_from_html = re.sub(
        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
        url_token,
        text_from_html
    )
    
    text_from_html = re.sub(
        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
        url_token,
        text_from_html
    )
    
    text_from_html = re.sub(
        '\n',
        return_carriage_token,
        text_from_html
    )    
    
    return ' '.join([t for t in text_from_html.split(' ') if t != ''])

# Feature extraction function
def extract_simple_features(data):
    question_ids = []
    answer_ids = []
    what_start = []
    which_start = []
    how_start = []
    why_start = []
    len_question = []
    len_question_body = []
    len_answer = []
    
    nb_strong_tags_question = []
    nb_code_tags_question = []
    nb_href_tags_question = []
    nb_hr_tags_question = []
    nb_blockquote_tags_question = []
    
    nb_strong_tags_answer = []
    nb_code_tags_answer = []
    nb_href_tags_answer = []
    nb_hr_tags_answer = []
    nb_blockquote_tags_answer = []
    
    nb_return_carriage_question = []
    nb_return_carriage_answer = []
    
    answer_score = []
    question_score = []
    question_view = []
    ratio_score1 = []
    ratio_score2 = []
    time_difference = []
    
    has_root_causes = []
    
    for d in data:
        question_ids.append(d['question_id'])
        answer_ids.append(d['answer_id'])
        has_root_cause = None
        if 'has_root_cause' in d:
            has_root_cause = d['has_root_cause']
            if has_root_cause is not None and not np.isnan(has_root_cause):
                has_root_causes.append(int(has_root_cause))
            else:
                has_root_causes.append(has_root_cause)
        else:
            has_root_causes.append(has_root_cause)

        question = d['question_title']
        question_body = d['question_body']
        try:
            answer = d['answer_body']
        except:
            answer = ''
        
        what_start.append(question.lower().startswith('what'))
        which_start.append(question.lower().startswith('which'))
        how_start.append(question.lower().startswith('how'))
        why_start.append(question.lower().startswith('why'))
        len_question.append(len(question))
        len_question_body.append(len(question_body))
        len_answer.append(len(answer))

        nb_strong_tags_question.append(question_body.count('<strong>'))
        nb_code_tags_question.append(question_body.count('<code>'))
        nb_href_tags_question.append(question_body.count('href='))
        nb_hr_tags_question.append(question_body.count('<hr/>'))
        nb_blockquote_tags_question.append(question_body.count('<blockquote>'))
        
        nb_strong_tags_answer.append(answer.count('<strong>'))
        nb_code_tags_answer.append(answer.count('<code>'))
        nb_href_tags_answer.append(answer.count('href='))
        nb_hr_tags_answer.append(answer.count('<hr/>'))
        nb_blockquote_tags_answer.append(answer.count('<blockquote>'))
        
        nb_return_carriage_question.append(question_body.count('\n'))
        nb_return_carriage_answer.append(answer.count('\n'))
        
        answer_score.append(d['answer_score'])
        question_score.append(d['question_score'])
        question_view.append(d['question_view_count'])
        try:
            ratio_score1.append(d['answer_score'] / d['question_score'])
        except:
            ratio_score1.append(0)
        ratio_score2.append(d['answer_score'] / d['question_view_count'])
        time_difference.append(d['answer_creation_date'] - d['question_creation_date'])
        
        
    return pd.DataFrame({
                          'question_id' : question_ids,
                          'answer_id' : answer_ids,
                          'what_start' : np.array(what_start).astype(int), 
                          'which_start' : np.array(which_start).astype(int), 
                          'how_start' : np.array(how_start).astype(int), 
                          'why_start' : np.array(why_start).astype(int),
                          'len_question' : len_question,
                          'len_question_body' : len_question_body,
                          'len_answer' : len_answer,
                          'nb_strong_tags_question' : nb_strong_tags_question,
                          'nb_code_tags_question' : nb_code_tags_question,
                          'nb_href_tags_question' : nb_href_tags_question,
                          'nb_hr_tags_question' : nb_hr_tags_question,
                          'nb_blockquote_tags_question' : nb_blockquote_tags_question,
                          'nb_strong_tags_answer' : nb_strong_tags_answer,
                          'nb_code_tags_answer' : nb_code_tags_answer,
                          'nb_href_tags_answer' : nb_href_tags_answer,
                          'nb_hr_tags_answer' : nb_hr_tags_answer,
                          'nb_blockquote_tags_answer' : nb_blockquote_tags_answer,
                          'nb_return_carriage_question' : nb_return_carriage_question,
                          'nb_return_carriage_answer' : nb_return_carriage_answer,
                          'answer_score' : answer_score,
                          'question_score' : question_score,
                          'question_view' : question_view,
                          'ratio_score1' : ratio_score1,
                          'ratio_score2' : ratio_score2,
                          'time_difference' : time_difference,
                          'has_root_cause' : has_root_causes
                        })