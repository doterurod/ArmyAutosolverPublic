'''''''''''''''''''''''''''''
COPYRIGHT DOTERUROD & LESTERRRY,

2021
'''''''''''''''''''''''''''''

cookie = "gc_visit_255773=%7B%22id%22%3A2524776305%2C%22sid%22%3A1454671991%7D; gc_visitor_255773=%7B%22id%22%3A1706929101%2C%22sfix%22%3A1%7D; gc_counter_255773=%7B%22id%22%3A1454671991%2C%22partner_code_id%22%3Anull%2C%22ad_offer_id%22%3Anull%2C%22last_activity%22%3A%222021-03-22+21%3A31%3A54%22%2C%22user_id%22%3A156030741%2C%22utm_id%22%3Anull%2C%22fuid%22%3Anull%2C%22fpid%22%3Anull%2C%22city_id%22%3Anull%7D; PHPSESSID5=b4ce07a91b99b58db2ec240cb46a5d64; __cfduid=d09487b73782c7f7d8f9552e79e769f311616437853"

links = [
"https://online.patriotsport.moscow/pl/teach/control/lesson/view?id=194854525&editMode=0",
"https://online.patriotsport.moscow/pl/teach/control/lesson/view?id=195162710&editMode=0", 
"https://online.patriotsport.moscow/pl/teach/control/lesson/view?id=195163858&editMode=0", 
"https://online.patriotsport.moscow/pl/teach/control/lesson/view?id=195304784&editMode=0", 
"https://online.patriotsport.moscow/pl/teach/control/lesson/view?id=195378428&editMode=0", 
"https://online.patriotsport.moscow/pl/teach/control/lesson/view?id=195379409&editMode=0", 
"https://online.patriotsport.moscow/pl/teach/control/lesson/view?id=195379761&editMode=0", 
"https://online.patriotsport.moscow/pl/teach/control/lesson/view?id=195380095&editMode=0"
]

import requests
import base64
import json
import urllib.parse
import platform

def parse_between(string, fr, to):
    start = string.find(fr) + len(fr)
    end = string.find(to, start)
    return string[start:end]

def solve(link, cookies):
    headers = {'cookie': cookies, 'referer': link,'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    r = requests.get(link, headers=headers)
    questionaryId = parse_between(r.text, "questionaryId:", ",") #регулярки? не не слышал
    object_id = parse_between(r.text, "objectId: ", ",")
    is_last_question = False

    while not is_last_question:
        r = requests.post("https://online.patriotsport.moscow/pl/teach/questionary-public/testing?id=" + questionaryId, headers=headers, data=f"questionaryId={questionaryId}") #получаем вопросы и ответы
        if "Ваш результат" in r.text or "Ваша оценка" in r.text:
            print("Тест уже решен")
            return #ес уже решали то пропускаем эти тесты
        json_data = r.json()['data']
        is_last_question = json_data['isLastQuestion']
        answers = json.loads(base64.b64decode(json_data['resultHash']))
        try:
            right_answer = next(item for item in answers['question']['variants'] if item['is_right'] == 1)
        except:
            right_answer = answers['question']['variants'][0] #у них в нескольких вопросах нет ни одного правильного ответа. Кто тот сайт писал?
        r = requests.post('https://online.patriotsport.moscow/pl/teach/questionary-public/do-question-answer', headers=headers, data=f"questionId={json_data['question_id']}&answerValue={urllib.parse.quote(right_answer['value'].encode('utf-8'))}&objectId={object_id}")
        print(f"Q: {answers['question']['title']}\nA: {right_answer['value']}")

n = 0
for link in links:
    n += 1
    print(f"Решаем #{n}")
    solve(link, cookie)
