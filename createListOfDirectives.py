import json
import re
from bs4 import BeautifulSoup

def getAllDirectivesFromData():
    global allDirectivesArray, bs_data
    for i in range(0, len(bs_data.find_all())):
        element = bs_data.find_all()[i]
        if element.name == 'directive' and (
            element.next in ['if', 'ifdef', 'ifndef', 'elif', 'else', 'endif']
        ):
            allDirectivesArray.append(i)

def getThisConditionalName(i):
    global allDirectivesArray
    index = allDirectivesArray[i]
    next = bs_data.find_all()[index].next
    if bs_data.find_all()[index + 1].name == 'name':
        name = ''
        j = index
        while bs_data.find_all()[j + 1].name == 'name':
            name += bs_data.find_all()[1 + j].text + ' '
            j += 1
        name = name[:-1]
    else:
        name = bs_data.find_all()[index + 1].text
    conditional = ''
    if next == 'ifndef':
            conditional = "! " + name
    else:
        conditional = name
    return conditional

def getThisCodeBlock(i):
    global conditionalDirectives, allDirectivesArray
    index = allDirectivesArray[i]
    codeBlock = []
    if len(bs_data.find_all()) > index:
        while ((bs_data.find_all()[index].name == 'directive' and
                i not in allDirectivesArray) or
                (bs_data.find_all()[index].name != 'directive' and
                bs_data.find_all()[index].name not in directives)):
            element = bs_data.find_all()[index]
            if (element.name in ['decl_stmt', 'expr_stmt', 'macro'] or
                element.name in directives):
                if element.name not in directives:
                        codeBlock.append(element.text)
                elif element.name in directives and element.text != ('#' + element.name):
                    codeBlock.append(element.text)
            index += 1
            if index + 1 >= len(bs_data.find_all()):
                break
    return codeBlock

def updateAllConditionalsDic(conditional, codeBlock):
    global allConditionalsDic
    if conditional not in allConditionalsDic:
        allConditionalsDic[conditional] = []
    for element in codeBlock:
        allConditionalsDic[conditional].append(element)


def getNestedConditionals(i, currentConditional):
    global allConditionalsDic
    i += 1
    nextElement = bs_data.find_all()[allDirectivesArray[i]]
    conditional = getThisConditionalName(i)
    conditional = "(" + currentConditional + ") and (" + conditional + ")"
    codeBlock = getThisCodeBlock(i)
    updateAllConditionalsDic(conditional, codeBlock)
    nextElement = bs_data.find_all()[allDirectivesArray[i + 1]]
    if nextElement.next in ['if', 'ifdef', 'ifndef']:
        i = getNestedConditionals(i, conditional)
    nextElement = bs_data.find_all()[allDirectivesArray[i + 1]]
    while nextElement.next != 'endif':
        i = getNestedConditionals(i, currentConditional)
        nextElement = bs_data.find_all()[allDirectivesArray[i + 1]]
    return i + 1


def getConditionalsNamesAndCodeBlocks():
    global allConditionalsDic, allDirectivesArray, bs_data
    currentConditional = ''
    i = 0
    while i < len(allDirectivesArray):
        element = bs_data.find_all()[allDirectivesArray[i]]
        if element.next in ['if', 'ifdef', 'ifndef']:
            # get conditional name:
            conditional = getThisConditionalName(i)
            currentConditional = conditional
            codeBlock = getThisCodeBlock(i)
            updateAllConditionalsDic(conditional, codeBlock)
            nextElement = bs_data.find_all()[allDirectivesArray[i + 1]]
            if nextElement.next in ['if', 'ifdef', 'ifndef']:
                i = getNestedConditionals(i, conditional)
                i -= 1
            i += 1
        elif element.next == 'elif':
            conditional = '!(' + currentConditional + ')'
            thisConditional = getThisConditionalName(i)
            conditional += ' and (' + thisConditional + ')'
            currentConditional = conditional
            codeBlock = getThisCodeBlock(i)
            updateAllConditionalsDic(conditional, codeBlock)
            nextElement = bs_data.find_all()[allDirectivesArray[i + 1]]
            if nextElement.next in ['if', 'ifdef', 'ifndef']:
                i = getNestedConditionals(i, conditional)
                i -= 1
            i += 1
        elif element.next == 'else':
            conditional = '!(' + currentConditional + ')'
            codeBlock = getThisCodeBlock(i)
            updateAllConditionalsDic(conditional, codeBlock)
            nextElement = bs_data.find_all()[allDirectivesArray[i + 1]]
            if nextElement.next in ['if', 'ifdef', 'ifndef']:
                i = getNestedConditionals(i, conditional)
                i -= 1
            i += 1
        elif element.next == 'endif':
            conditional = ''
            i += 1


def removeEmptyValuesFromDict():
    global allConditionalsDic
    copy = allConditionalsDic.copy()
    for key in copy:
        if copy[key] == []:
            del allConditionalsDic[key]


def createListOfDirectives():
    global allDirectivesArray, listDict
    listDict["List of Directives:"] = []
    for key in allConditionalsDic:
        listDict["List of Directives:"].append(key)

def initializeGlobalVariables():
    global allDirectivesArray, bs_data, c_file_name, directives, allConditionalsDic
    allDirectivesArray = []
    allConditionalsDic = {}
    bs_data = None
    directiveIndex = None
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
    conditionalDirectives = [
        'if',
        'elif',
        'else',
        'endif',
        'ifdef',
        'ifndef',
    ]
    c_file_name = ''


# Start the project code
def main(file_name):
    global allDirectivesArray, bs_data, c_file_name, directives, allConditionalsDic, listDict
    initializeGlobalVariables()
    c_file_name = file_name
    with open('uploadedFiles/'+c_file_name, 'r') as f:
        data = f.read() 
    bs_data = BeautifulSoup(data, 'xml') 
    getAllDirectivesFromData() # Will save in allDirectivesArray the indexes of directives
    getConditionalsNamesAndCodeBlocks() # Will save in allConditionalsDic the directives conditionals names and codeBlocks
    removeEmptyValuesFromDict()
    createListOfDirectives()
    folder_path = "listFiles/"
    json_name = c_file_name[:-6] + '_directives_list.json'
    with open(folder_path + json_name, 'w', newline='') as json_file:
        json.dump(listDict, json_file)
    return json_name


# Initialize important variables and call main()
allDirectivesArray = []
allConditionalsDic = {}
listDict = {}
bs_data = None
directiveIndex = None
directives = []
conditionalDirectives = []
c_file_name = ''