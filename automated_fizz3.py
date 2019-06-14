# Interactive python client for fizzbot

import json
import urllib.request
import urllib.error

domain = 'https://api.noopschallenge.com'

# print server response
def print_response(dict):
    print('')
    print('message:')
    print(dict.get('message'))
    print('')
    for key in dict:
        if key != 'message':
            print('%s: %s' % (key, json.dumps(dict.get(key))))
    print('')

def apply_rules(number, rules):
    ret = ''
    printNumber = True
    for rule in rules:
        if (number % rule[0] == 0):
            ret += rule[1]
            printNumber = False
    if printNumber:
        ret += str(number)
    return ret

def make_rules(rules):
    arr = []
    for rule in rules:
        arr.append([int(rule.get('number')), rule.get('response')])
    return arr

def do_next_question(domain, question_url):
    request = urllib.request.urlopen( ('%s%s' % (domain, question_url)) )
    question_data = json.load(request)
    rules = make_rules(question_data.get('rules'))
    numbers = question_data.get('numbers')
    body = None
    if (numbers) :
        string = ''
        it = iter(numbers)
        try :
            while True:
                currentNumber = int(next(it))
                string += apply_rules(currentNumber, rules)
                string += ' '
        except StopIteration:
            string = string[0:-1]
        body = json.dumps({ 'answer':string })
    req = urllib.request.Request(domain + question_url, data=body.encode('utf8'), headers={'Content-Type': 'application/json'})
    res = urllib.request.urlopen(req)
    response = json.load(res)
    nextQuestion = response.get('nextQuestion')
    if nextQuestion:
        return do_next_question(domain, nextQuestion)
    print(response.get('message'))


def first_question(domain, question_url):
    body = json.dumps({'answer':'COBOL'})
    try:
        firstRawResponse = urllib.request.urlopen( ('%s%s' % (domain, question_url)) )
        firstParsedResponse = json.load(firstRawResponse)
        firstQuestionUrl = firstParsedResponse.get('nextQuestion')
        firstPostAnswer = urllib.request.Request(domain + firstQuestionUrl, data=body.encode('utf8'), headers={'Content-Type': 'application/json'})
        secondQuestionResponse = urllib.request.urlopen(firstPostAnswer)
        return json.load(secondQuestionResponse).get('nextQuestion')
    except urllib.error.HTTPError as e:
        response = json.load(e)
        print_response(response)
        exit()
    return

def main():
    question_url = '/fizzbot'
    next_question = first_question(domain, question_url)
    #print(next_question)
    do_next_question(domain, next_question)
    return

if __name__ == '__main__': main()
