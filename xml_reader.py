import json
import os

from bs4 import BeautifulSoup

# Get the conditional variable of a #else
def getElseConditional(i):
    conditional = ""
    while bs_data.find_all()[i].next != 'if' and bs_data.find_all()[i].next != 'ifndef' and bs_data.find_all()[i].next != 'ifdef':
        if bs_data.find_all()[i].next == 'elif':
            conditional += "not " + bs_data.find_all()[i+1].text + " and "
        i -= 1
    conditional += "not " + bs_data.find_all()[i+1].text
    return conditional

# Get the code block after a #if, #ifdef, #ifndef, #elif
def getIfCodeBlock(i):
    global directives
    codeBlock = []
    if len(bs_data.find_all()) > i + 1:
        while (bs_data.find_all()[i+1].name != 'directive' or
               (bs_data.find_all()[i+1].name == 'directive' and
                (bs_data.find_all()[i+1].text != 'else' and
                 bs_data.find_all()[i+1].text != 'elif' and 
                 bs_data.find_all()[i+1].text != 'endif'))):
            if (bs_data.find_all()[i+1].name == 'decl_stmt' or
                bs_data.find_all()[i+1].name == 'expr_stmt' or
                bs_data.find_all()[i+1].name in directives):
                if bs_data.find_all()[i+1].name not in directives:
                    codeBlock.append(bs_data.find_all()[i+1].text)
                elif bs_data.find_all()[i+1].name in directives and bs_data.find_all()[i+1].text != ('#' + bs_data.find_all()[i+1].name):
                    codeBlock.append(bs_data.find_all()[i+1].text)
            i += 1
            if i + 1 >= len(bs_data.find_all()):
                break
    return codeBlock

# Find elements of bs_data that are directives and are conditionals
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


# Start the project code
def main(file_name):
    global allDirectivesArray, bs_data, c_file_name, directives
    c_file_name = file_name
    with open('uploadedFiles/'+c_file_name, 'r') as f:
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
    folder_path = "jsonFiles/"
    json_name = c_file_name[:-6] + '.json'
    with open(folder_path + json_name, 'w', newline='') as json_file:
        json.dump(allConditionalsDic, json_file)
    return json_name

# Initialize important variables and call main()
allDirectivesArray = []
allConditionalsDic = {}
bs_data = None
directiveIndex = None
directives = []
c_file_name = ''