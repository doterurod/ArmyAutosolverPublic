import requests
import base64
import json
import urllib.parse
cookie = '''вставьте вместо этого текст ваши куки файлы'''
def ParseBetween(string,fr,to):
    start = string.find(fr)+len(fr)
    end = string.find(to,start)
    return string[start:end]
def Solve(Link,cookies):
    headers = {'cookie':cookies,'referer':Link,'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    r = requests.get(Link,headers=headers)
    questionaryId = ParseBetween(r.text,"questionaryId:",",")#регулярки? не не слышал
    object_id = ParseBetween(r.text,"objectId: ",',')
    is_last_question = False
    while not is_last_question:
        r = requests.post('https://online.patriotsport.moscow/pl/teach/questionary-public/testing?id='+questionaryId,headers = headers,data=f'questionaryId={questionaryId}')#получаем вопросы и ответы
        if 'Ваш результат'in r.text or "Ваша оценка" in r.text:
            return #ес уже решали то пропускаем эти тесты
        json_data = r.json()['data']

        is_last_question = json_data['isLastQuestion']
        answers = json.loads(base64.b64decode(json_data['resultHash']))

        try:
            right_answer =next(item for item in answers['question']['variants'] if item["is_right"] == 1)
        except:
            right_answer =answers['question']['variants'][0]#у них в нескольких вопросах нет ни одного правильного ответа. Кто тот сайт писал?

        r=requests.post('https://online.patriotsport.moscow/pl/teach/questionary-public/do-question-answer',headers=headers,data=f"questionId={json_data['question_id']}&answerValue={urllib.parse.quote(right_answer['value'].encode('utf-8'))}&objectId={object_id}")
        print(f"Вопрос:{answers['question']['title']} Ответ:{right_answer}")
links = ['https://online.patriotsport.moscow/pl/teach/control/lesson/view?id=194854525&editMode=0','https://online.patriotsport.moscow/pl/teach/control/lesson/view?id=195162710&editMode=0','https://online.patriotsport.moscow/pl/teach/control/lesson/view?id=195163858&editMode=0','https://online.patriotsport.moscow/pl/teach/control/lesson/view?id=195304784&editMode=0','https://online.patriotsport.moscow/pl/teach/control/lesson/view?id=195378428&editMode=0','https://online.patriotsport.moscow/pl/teach/control/lesson/view?id=195379409&editMode=0','https://online.patriotsport.moscow/pl/teach/control/lesson/view?id=195379761&editMode=0','https://online.patriotsport.moscow/pl/teach/control/lesson/view?id=195380095&editMode=0']
for link in links:
    Solve(link,cookie)
    print(f"Прорешал по ссылке {link}")