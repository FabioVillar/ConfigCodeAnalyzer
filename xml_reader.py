import json
import re
from bs4 import BeautifulSoup


# Get the conditional variable of a #else
def getElseConditional(i):
    conditional = ""
    while bs_data.find_all()[i].next != 'if' and bs_data.find_all()[i].next != 'ifndef' and bs_data.find_all()[i].next != 'ifdef':
        if bs_data.find_all()[i].next == 'elif':
            conditional += "! (" + bs_data.find_all()[i+1].text + ") && "
        if bs_data.find_all()[i].next == 'endif':
            j = i - 1
            while bs_data.find_all()[j].next != 'if' and bs_data.find_all()[j].next != 'ifndef' and bs_data.find_all()[j].next != 'ifdef':
                j -= 1
            i = j - 1
            continue
        i -= 1
    conditional += "! " + bs_data.find_all()[i+1].text
    return conditional


# Get the code block after a #if, #ifdef, #ifndef, #elif
def getIfCodeBlock(i):
    global directives
    codeBlock = []
    if len(bs_data.find_all()) > i:
        while ((bs_data.find_all()[i].name != 'directive' and
                bs_data.find_all()[i].name not in directives) or
               (bs_data.find_all()[i].name == 'directive' and
                (bs_data.find_all()[i].text != 'else' and
                 bs_data.find_all()[i].text != 'elif' and 
                 bs_data.find_all()[i].text != 'endif' and 
                 bs_data.find_all()[i].text != 'if' and
                 bs_data.find_all()[i].text != 'ifdef' and
                 bs_data.find_all()[i].text != 'ifndef' and
                 bs_data.find_all()[i].text != 'elif'))):
            if (bs_data.find_all()[i].name == 'decl_stmt' or
                bs_data.find_all()[i].name == 'expr_stmt' or
                bs_data.find_all()[i].name == 'macro' or
                bs_data.find_all()[i].name in directives):
                if bs_data.find_all()[i].name not in directives:
                    codeBlock.append(bs_data.find_all()[i].text)
                elif bs_data.find_all()[i].name in directives and bs_data.find_all()[i].text != ('#' + bs_data.find_all()[i].name):
                    codeBlock.append(bs_data.find_all()[i].text)
            i += 1
            if i + 1 >= len(bs_data.find_all()):
                break
    return codeBlock


# Find the elements of bs_data that are conditionals and saves the code block after it
def getCodeBlocks():
    global bs_data, allConditionalsDic
    # iterates the whole bs_data.find_all()
    for i in range(0, len(bs_data.find_all())):
        # if the position has a directive if, ifdef, ifndef or elif:
        if(bs_data.find_all()[i].name == 'directive' and
               (bs_data.find_all()[i].next == 'if' or
                bs_data.find_all()[i].next == 'ifdef' or
                bs_data.find_all()[i].next == 'ifndef' or
                bs_data.find_all()[i].next == 'elif')):
            # conditional will store the conditional variable value
            next = bs_data.find_all()[i].next
            if bs_data.find_all()[i + 1].name == 'name':
                name = ''
                j = i
                while bs_data.find_all()[j + 1].name == 'name':
                    name += bs_data.find_all()[j + 1].text + ' '
                    j += 1
                name = name[:-1]
            else:
                name = bs_data.find_all()[i+1].text
            if next == 'ifndef':
                conditional = "! " + name
            else:
                conditional = name
            # codeBlock will have the code after the conditional
            codeBlock = getIfCodeBlock(i+1)
            # afterwards, the codeblock will be saved in allConditionalsDic
            if allConditionalsDic.get(conditional) is not None:
                allConditionalsDic[conditional].append(codeBlock) 
            else:
                allConditionalsDic[conditional] = [codeBlock]
        # if it does not, check if it's a else:
        elif bs_data.find_all()[i].name == 'directive' and bs_data.find_all()[i].next == 'else':
            conditional = getElseConditional(i)
            codeBlock = getIfCodeBlock(i+1)
            if allConditionalsDic.get(conditional) is not None:
                allConditionalsDic[conditional].append(codeBlock) 
            else:
                allConditionalsDic[conditional] = [codeBlock]


# Check if a conditional has an OR/|| and see if the code block must be appended to another position
def checkConditionalOR():
    global allConditionalsDic
    andString = "&&"
    orString = "||"
    directivesPresent = []
    copy = allConditionalsDic.copy()
    for key in copy:
        if andString in key:
            continue
        if orString in key:
            directivesPresent = re.findall(r'\([^()]+\)|\b\w+\b', key)
            for directive in directivesPresent:
                if directive in allConditionalsDic:
                    allConditionalsDic[directive] += allConditionalsDic[key]
                else:
                    allConditionalsDic[directive] = allConditionalsDic[key]
            del allConditionalsDic[key]
    return

def checkIfDictHasEmptyValues():
    global allConditionalsDic
    copy = allConditionalsDic.copy()
    for key in copy:
        for i in range(len(copy[key])):
            if copy[key][i] == []:
                allConditionalsDic[key].remove(copy[key][i])


# Start the project code
def main(file_name):
    global allDirectivesArray, bs_data, c_file_name, directives, allConditionalsDic
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
    allDirectivesArray = [] # Will have all directives of the C file
    for data in bs_data.find_all():
        if (data.name == 'directive' and 
            (
                data.next == 'if' or
                data.next == 'ifdef' or
                data.next == 'ifndef' or
                data.next == 'ifdef' or
                data.next == 'ifdef' or
                data.next == 'elif' or
                data.next == 'else' or
                data.next == 'endif')
        ):
            allDirectivesArray.append(data)
    getCodeBlocks() # Will get the code block after a conditional directive
    checkConditionalOR() # Verify OR in the conditionals dictionary
    checkIfDictHasEmptyValues()
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
# main('test3.c.xml')