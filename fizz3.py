# Interactive python client for fizzbot

import json
import urllib.request
import urllib.error

domain = 'https://api.noopschallenge.com'

def print_sep(): print('----------------------------------------------------------------------')

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

# try an answer and see what fizzbot thinks of it
def try_answer(question_url, answer):
    print_sep()
    body = json.dumps({ 'answer': answer })
    print('*** POST %s %s' % (question_url, body))
    try:
        req = urllib.request.Request(domain + question_url, data=body.encode('utf8'), headers={'Content-Type': 'application/json'})
        res = urllib.request.urlopen(req)
        response = json.load(res)
        print_response(response)
        print_sep()
        return response

    except urllib.error.HTTPError as e:
        response = json.load(e)
        print_response(response)
        return response

# keep trying answers until a correct one is given
def get_correct_answer(question_url):
    while True:
        answer = input('Enter your answer:\n')

        response = try_answer(question_url, answer)

        if (response.get('result') == 'interview complete'):
            print('congratulations!')
            exit()

        if (response.get('result') == 'correct'):
            input('press enter to continue')
            return response.get('nextQuestion')

# do the next question
def do_question(domain, question_url):

    request = urllib.request.urlopen( ('%s%s' % (domain, question_url)) )
    question_data = json.load(request)
    numbers = question_data.get('numbers')

    if (numbers) :
        string = ''
        it = iter(numbers)
        try :
            currentNumber = next(it)
            boolean = False
            if (currentNumber % 3 == 0):
                string += 'Fizz'
                boolean = True
            if (currentNumber % 5 == 0):
                string += 'Buzz'
                boolean = True
            if not boolean:
                string += currentNumber
            string += ' '
        except StopIteration:
            string[0,len(string)-2]
        response = try_answer(question_url, string)

    req = urllib.request.Request(domain + question_url, data=body.encode('utf8'), headers={'Content-Type': 'application/json'})
    res = urllib.request.urlopen(req)
    """
    print_sep()
    print('*** GET %s' % question_url)

    request = urllib.request.urlopen( ('%s%s' % (domain, question_url)) )
    question_data = json.load(request)
    print_response(question_data)
    print_sep()

    next_question = question_data.get('nextQuestion')

    if next_question: return next_question
    return get_correct_answer(question_url)
    """
def do_next_question(domain, question_url):
    request = urllib.request.urlopen( ('%s%s' % (domain, question_url)) )
    question_data = json.load(request)
    print(question_data.get('message'))
    numbers = question_data.get('numbers')
    body = None
    if (numbers) :
        string = ''
        it = iter(numbers)
        try :
            currentNumber = next(it)
            boolean = False
            if (currentNumber % 3 == 0):
                string += 'Fizz'
                boolean = True
            if (currentNumber % 5 == 0):
                string += 'Buzz'
                boolean = True
            if not boolean:
                string += currentNumber
            string += ' '
        except StopIteration:
            string[0,len(string)-2]
        body = json.dumps({'answer': string})
    req = urllib.request.Request(domain + question_url, data=body.encode('utf8'), headers={'Content-Type': 'application/json'})
    res = urllib.request.urlopen(req)
    response = json.load(res)
    nextQuestion = res.get('nextQuestion')
    return do_next_question(domain, nextQuestion)


def first_question(domain, question_url):
    body = json.dumps({'answer':'COBOL'})
    try:
        firstRawResponse = urllib.request.urlopen( ('%s%s' % (domain, question_url)) )
        firstParsedResponse = json.load(firstRawResponse)
        firstQuestionUrl = firstParsedResponse.get('nextQuestion')
        postFirstAnswer = urllib.request.Request(domain + firstQuestionUrl, data=body.encode('utf8'), headers={'Content-Type': 'application/json'})
        firstQuestionResponse = urllib.request.urlopen(postFirstAnswer)
        return json.load(firstQuestionResponse).get('nextQuestion')
    except urllib.error.HTTPError as e:
        response = json.load(e)
        print_response(response)
        exit()
    return

def main():
    question_url = '/fizzbot'
    next_question = first_question(domain, question_url)
    print(next_question)
    do_next_question(domain, next_question)
    return
    while question_url:
        question_url = do_question(domain, question_url)

if __name__ == '__main__': main()
