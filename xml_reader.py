import json

from bs4 import BeautifulSoup

def getElseConditional(i):
    conditional = ""
    while bs_data.find_all()[i].next != 'if':
        if bs_data.find_all()[i].next == 'elif':
            conditional += "not " + bs_data.find_all()[i+1].text + " and "
        i -= 1
    conditional += "not " + bs_data.find_all()[i+1].text
    return conditional

def getIfCodeBlock(i):
    codeBlock = []
    if len(bs_data.find_all()) >= i + 2:
        while bs_data.find_all()[i+2].name != 'directive':
            codeBlock.append(bs_data.find_all()[i].text)
            i += 1
    return codeBlock

def findConditionals():
    global bs_data, allConditionalsDic
    for i in range(0, len(bs_data.find_all())):

        if(bs_data.find_all()[i].name == 'directive' and
               (bs_data.find_all()[i].next == 'if' or
                bs_data.find_all()[i].next == 'ifdef' or
                bs_data.find_all()[i].next == 'ifndef' or
                bs_data.find_all()[i].next == 'elif')):
            
            conditional = bs_data.find_all()[i+1].text
            codeBlock = getIfCodeBlock(i)
            if allConditionalsDic.get(conditional) is not None:
                allConditionalsDic[conditional].append(codeBlock) 
            else:
                allConditionalsDic[conditional] = codeBlock 
        
        elif bs_data.find_all()[i].name == 'directive' and bs_data.find_all()[i].next == 'else':
            conditional = getElseConditional(i)
            codeBlock = getIfCodeBlock(i)
            if allConditionalsDic.get(conditional) is not None:
                allConditionalsDic[conditional].append(codeBlock) 
            else:
                allConditionalsDic[conditional] = codeBlock 



def main():
    global allDirectivesArray, bs_data, c_file_name
    with open('tests/'+c_file_name, 'r') as f:
        data = f.read() 
    bs_data = BeautifulSoup(data, 'xml') 
    directives = [
        'include',
        'define',
        'if',
        'elif',
        'else',
        'endif',
        'error',
        'ifdef',
        'ifndef',
        'line',
        'pragma',
        'undef',
        'warning',
    ]
    allDirectivesArray = []
    for data in bs_data.find_all():
        if data.name == 'directive':
            allDirectivesArray.append(data)
    findConditionals()
    json_name = 'conditionals_' + c_file_name[:-6] + '.json'
    with open(json_name, 'w', newline='') as json_file:
        json.dump(allConditionalsDic, json_file)


allDirectivesArray = []
allConditionalsDic = {}
bs_data = None
directiveIndex = None
c_file_name = 'test3.c.xml'
main()