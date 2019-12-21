from bs4 import BeautifulSoup
import requests
import json

def get_questions_ids_by_tag(tag, pagenumber):

    url = 'https://stackoverflow.com/questions/tagged/{}?tab=votes&page={}&pagesize=50'.format(tag, pagenumber)
    resonse = requests.get(url)
    html_doc = resonse.text
    soup = BeautifulSoup(html_doc, 'lxml')
    links = []

    for link in soup.find_all('div'):
        try:
            id_element = link.get('id')
            if id_element.startswith('question-summary-'):
                links.append(int(id_element.split('-')[-1]))
        except:
            pass

    print(links)
    print(len(links))

class SofScrapper:
    def __init__(self,
                 api_key='sBV84q*C4QiG5o8C9Od3uw((',
                 verbose_quota=True):
        self.api_key = api_key
        self.verbose_quota = verbose_quota

    def _process_url(self, url):
        if self.api_key is not None:
            url += '&key=' + self.api_key
        return url
    
    def _verbose_quota(self, data_json):
        print(str(data_json["quota_remaining"]) + ' / ' + str(data_json["quota_max"]))

    def get_question_data_from_id(self, question_id):
        url = 'https://api.stackexchange.com/2.2/questions/{}?order=desc&sort=activity&site=stackoverflow&filter=withbody'\
              .format(str(question_id))
        url = self._process_url(url)
        req = requests.get(url)
        data_json = req.json()
        if self.verbose_quota:
            self._verbose_quota(data_json)
        return data_json['items']

    def get_answer_data_from_id(self, answer_id):
        url = 'https://api.stackexchange.com/2.2/answers/{}/?order=desc&sort=activity&site=stackoverflow&filter=withbody'\
              .format(str(answer_id))
        url = self._process_url(url)
        req = requests.get(url)
        data_json = req.json()
        if self.verbose_quota:
            self._verbose_quota(data_json)
        return data_json['items']
        
    def get_answer_data_from_question_id(self, question_id):
        url = 'https://api.stackexchange.com/2.2/questions/{}/answers?order=desc&sort=activity&site=stackoverflow&filter=withbody'\
              .format(str(question_id))
        url = self._process_url(url)
        req = requests.get(url)
        data_json = req.json()
        if self.verbose_quota:
            self._verbose_quota(data_json)
        return data_json['items']

    def get_questions_ids_from_tag(self, tag, sort_by='votes'):
        url = 'https://api.stackexchange.com/2.2/search?order=desc&sort={}&site=stackoverflow&filter=withbody&tagged={}'\
              .format(sort_by, tag)
        url = self._process_url(url)
        req = requests.get(url)
        data_json = req.json()
        if self.verbose_quota:
            self._verbose_quota(data_json)
        return data_json['items']
    
if __name__ == '__main__':
    tags = ['python', 'java', 'scikit-learn', 'tensorflow', 'docker', 'jupyter', 'sql', 'django', 'beautifulsoup']

    for tag in tags:
        print('TAG : ' + tag.upper())
        # scrapper = SofScrapper(api_key=None)
        scrapper = SofScrapper(api_key='sBV84q*C4QiG5o8C9Od3uw((')
        questions_json_votes = scrapper.get_questions_ids_from_tag(tag, sort_by='votes')
        questions_json_activity = scrapper.get_questions_ids_from_tag(tag, sort_by='activity')

        with open('../data/{}_questions_votes.json'.format(tag), 'w') as f:
            json.dump(questions_json_votes, f)

        with open('../data/{}_questions_activity.json'.format(tag), 'w') as f:
            json.dump(questions_json_activity, f)

        answers_json_votes = []
        answers_json_activity = []
        for q in questions_json_votes:
            answers_json_votes.append(scrapper.get_answer_data_from_question_id(q['question_id']))
        for q in questions_json_activity:
            answers_json_activity.append(scrapper.get_answer_data_from_question_id(q['question_id']))

        with open('../data/{}_answer_votes.json'.format(tag), 'w') as f:
            json.dump(answers_json_votes, f)
        with open('../data/{}_answer_activity.json'.format(tag), 'w') as f:
            json.dump(answers_json_activity, f)

        print('')