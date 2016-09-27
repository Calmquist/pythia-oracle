#!/usr/bin/env python
#-*- coding: utf-8 -*-
##---------------------------------------------------------------------------------------------------
#  General logic
#
##---------------------------------------------------------------------------------------------------

import imports
from imports import *
import config

import logicscen
from logicscen import *

from kivy.uix.spinner import SpinnerOption

#---------------------------------------------------------------------------------------------------
# Basic
#---------------------------------------------------------------------------------------------------

class ClickLabel(Button, Label):
    pass

# is this even used anywhere anymore?
class InputLabel(TextInput, Label):
    pass

def resetCenterDisplay(self, textArray=config.textArray, textStatusArray=config.textStatusArray):

    for i in range(len(textArray)):
        makeItemLabels(self, textArray[i], textStatusArray[i])

    switchModes(self)

def updateCenterDisplay(self, text, status='result'):

    makeItemLabels(self, text, status)
    addToCenterDisplay(self, text, status)

def switchModes(self):

    self.centerDisplayGrid.clear_widgets()
    fictionStatusList = ["plain", "italic", "bold", "bold_italic", "color1", "color2"]

    edit_mode = config.general['edit_behavior']

    if edit_mode == "read":
        # this mode is for reading the entire log, mechanics and all

        self.centerDisplayGrid.cols = 1

        for index in range(len(config.textArray)):
            status = config.textStatusArray[index]
            if status != "ephemeral":
                self.centerDisplayGrid.add_widget(config.textLabelArray[index])

    elif edit_mode == "play":
        # this mode is used if you're prone to forgetting to change format type but don't wish to edit text; probably going to deprecate this now that switching modes is faster

        self.centerDisplayGrid.cols = 2

        for index in range(len(config.textArray)):
            status = config.textStatusArray[index]
            if status != "ephemeral":
                self.centerDisplayGrid.add_widget(config.textLabelArray[index])
                self.centerDisplayGrid.add_widget(config.textStatusLabelArray[index])

    elif edit_mode == "fiction":
        # fiction mode for reading just text; don't show mechanics or formats tags

        self.centerDisplayGrid.cols = 1

        for index in range(len(config.textArray)):
            status = config.textStatusArray[index]
            if status in fictionStatusList:
                self.centerDisplayGrid.add_widget(config.textLabelArray[index])

    elif edit_mode == "fic-edit":
        # editing mode for just text, no mechanics or formats tags

        self.centerDisplayGrid.cols = 1

        for index in range(len(config.textArray)):
            status = config.textStatusArray[index]
            if status in fictionStatusList:
                self.centerDisplayGrid.add_widget(config.textFieldLabelArray[index])

    else:
        # full editing mode, text, mechanics, formats
        self.centerDisplayGrid.cols = 2

        for index in range(len(config.textArray)):
            status = config.textStatusArray[index]
            if status != "ephemeral":
                self.centerDisplayGrid.add_widget(config.textFieldLabelArray[index])
                self.centerDisplayGrid.add_widget(config.textStatusLabelArray[index])

    jumpToIndex(self, -1)

def addToCenterDisplay(self, text, status):

    edit_mode = config.general['edit_behavior']
    fictionStatusList = ["plain", "italic", "bold", "bold_italic", "color1", "color2"]

    if edit_mode == "read":
        # this mode is for reading the entire log, mechanics and all
        if status != "ephemeral":
            self.centerDisplayGrid.add_widget(config.textLabelArray[-1])

    elif edit_mode == "play":
        # this mode is used if you're prone to forgetting to change format type but don't wish to edit text
        if status != "ephemeral":
            self.centerDisplayGrid.add_widget(config.textLabelArray[-1])
            self.centerDisplayGrid.add_widget(config.textStatusLabelArray[-1])

    elif edit_mode == "fiction":
        # fiction mode for reading just text; don't show mechanics or formats tags
        if status in fictionStatusList:
            self.centerDisplayGrid.add_widget(config.textLabelArray[-1])

    elif edit_mode == "fic-edit":
        # editing mode for just text, no mechanics or formats tags
        if status in fictionStatusList:
            self.centerDisplayGrid.add_widget(config.textFieldLabelArray[-1])

    else:
        # full editing mode, text, mechanics, formats
        if status != "ephemeral":
            self.centerDisplayGrid.add_widget(config.textFieldLabelArray[-1])
            self.centerDisplayGrid.add_widget(config.textStatusLabelArray[-1])

    jumpToIndex(self, -1)

def makeItemLabels(self, text, status='result'):

    if len(text) <= 0:
        return

    edit_mode = config.general['edit_behavior']

    if text[:1] == "\n":
        text = text[1:]

    config.textArray.append(text)
    config.textStatusArray.append(status)

    base_text = text
    text = parseText(text, status)

    label = ClickLabel(text=text, size_hint_y=None, font_size=config.maintextfont, font_name='Fantasque-Sans', background_normal='', background_down='', background_color=(0,0,0,0), background_color_down=accent2)
    label.text_size = (self.centerDisplayGrid.width, None)
    label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
    label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
    label.bind(on_release=storeBookmarkLabel)
    label.bind(on_ref_press=refPress)
    label.foreground_color=(1,1,1,1)
    label.markup = True
    label.self = self
    label.index = len(config.textArray)-1
    #label.index = config.textArray.index(base_text)
    config.textLabelArray.append(label)

    label = ClickLabel(text=status, size_hint=(None, .15), height=12, font_size=config.basefont60, font_name='Fantasque-Sans')
    label.background_normal=''
    label.background_color=accent1
    label.background_down=''
    label.background_color_down=accent2
    label.bind(on_press=cycleText)
    config.textStatusLabelArray.append(label)
    label.index = len(config.textArray)-1

    # this is a much cleaner solution instead of cycling, but takes an unacceptably long time
    #formatList = ['query', 'result', 'oracle', 'aside', 'mechanic1', 'mechanic2', "plain", "italic", "bold", "bold_italic", "color1", "color2"]

    #spinner = Spinner(
        # default value shown
    #    text=status,
        # available values
    #    values=formatList,
    #    background_normal='',
    #    background_color=accent1,
    #    background_down='',
    #    background_color_down=accent2,
    #    font_size=config.basefont60,
    #    size_hint=(.15, None),
    #    )
    #spinner.bind(text=reformatText)
    #config.textStatusLabelArray.append(spinner)

    label = TextInput(text="", size_hint_y=None, font_size=config.maintextfont)
    label.bind(focus=focusChangeText)
    label.background_color=neutral
    label.foreground_color=(1,1,1,1)
    #label.index = config.textArray.index(base_text)
    label.index = len(config.textArray)-1
    label.text = base_text
    config.textFieldLabelArray.append(label)

def parseText(text, status):

    #mechanicStatusList = ["oracle", "result", "aside", "query", "mechanic1", "mechanic2"]
    #fictionStatusList = ["plain", "italic", "bold", "bold_italic", "color1", "color2"]

    if status in config.formats:
        blockformat = config.formats[status]
        print(status, blockformat)
        if blockformat == "color1":
            text = "[color=" + str(config.formats['highlight_color']) + "]" + text + "[/color]"
        elif blockformat == "color2":
            text = "[color=" + str(config.formats['alternate_color']) + "]" + text + "[/color]"
        elif blockformat == "color3":
            text = "[i][color=" + str(config.formats['transitory_color']) + "]" + text + "[/color][/i]"
        else:
            if blockformat == "bold":
                text = "[b]" + text + "[/b]"
            elif blockformat == "italic":
                text = "[i]" + text + "[/i]"
            elif blockformat == "bold_italic":
                text = "[b][i]" + text + "[/i][/b]"

    return text

# used by the spinner option; not used now
def reformatText(spinner, status):

    config.textStatusArray[config.textStatusLabelArray.index(spinner)] = status
    text = config.textArray[config.textStatusLabelArray.index(spinner)]
    text = parseText(text, status)
    config.textLabelArray[index].text = text

    return True

def cycleText(label, *args):

    status = label.text

    # mechanics tags
    formatList = ["ephemeral", "result", "query", "oracle", "aside", "mechanic1", "mechanic2", "plain", "italic", "bold", "bold_italic", "color1", "color2"]

    if formatList.index(status) == len(formatList)-1:
        status = formatList[0]
    else:
        status = formatList[formatList.index(status)+1]

    config.textStatusArray[config.textStatusLabelArray.index(label)] = status
    label.text = status

    text = config.textArray[config.textStatusLabelArray.index(label)]
    text = parseText(text, status)

    config.textLabelArray[config.textStatusLabelArray.index(label)].text = text

    return True

def updateThreadDisplay(self, text, status):

    config.threadArray.append(text)
    config.threadStatusArray.append(status)

    label = TextInput(text=text, size_hint_y=None, size_hint_x=.90, multiline=False, height=config.baseheight, font_size=config.basefont90, font_name='Fantasque-Sans', background_color=(0,0,0,0), foreground_color=styles.textcolor)
    label.bind(focus=focusChangeThread)
    config.threadLabelArray.append(label)

    label = ClickLabel(text=status, size_hint_y=None, size_hint_x=.10, height=config.baseheight, font_size=config.basefont75, font_name='Fantasque-Sans')
    label.background_normal=''
    label.background_color=accent1
    label.background_down=''
    label.background_color_down=accent2
    label.bind(on_press=cycleThread)
    label.markup = True
    config.threadStatusLabelArray.append(label)

    if status == "Resolved":
        self.threadDisplayGrid.add_widget(config.threadStatusLabelArray[-1])
        self.threadDisplayGrid.add_widget(config.threadLabelArray[-1])
    else:
        self.threadDisplayGrid.add_widget(config.threadLabelArray[-1], len(self.threadDisplayGrid.children))
        self.threadDisplayGrid.add_widget(config.threadStatusLabelArray[-1], len(self.threadDisplayGrid.children))

def cycleThread(self, *args):
    # current -> major -> minor -> past -> resolved -> abandoned -> removed -> current
    if self.text == "Current":
        self.text = "Major"
        config.threadStatusArray[config.threadStatusLabelArray.index(self)] = "Major"
    elif self.text == "Major":
        self.text = "Minor"
        config.threadStatusArray[config.threadStatusLabelArray.index(self)] = "Minor"
    elif self.text == "Minor":
        self.text = "Past"
        config.threadStatusArray[config.threadStatusLabelArray.index(self)] = "Past"
    elif self.text == "Past":
        self.text = "Resolved"
        config.threadStatusArray[config.threadStatusLabelArray.index(self)] = "Resolved"
    elif self.text == "Resolved":
        self.text = "Abandoned"
        config.threadStatusArray[config.threadStatusLabelArray.index(self)] = "Abandoned"
    elif self.text == "Abandoned":
        self.text = "Don't Show"
        config.threadStatusArray[config.threadStatusLabelArray.index(self)] = "Don't Show"
    elif self.text == "Don't Show":
        self.text = "Current"
        config.threadStatusArray[config.threadStatusLabelArray.index(self)] = "Current"
    else:
        self.text = "Current"
        config.threadStatusArray[config.threadStatusLabelArray.index(self)] = "Current"

    return True

# this is called only on a save
def clearThread(self, *args):

    for i in range(len(config.threadStatusArray)):
        if config.threadStatusArray[i] == "Don't Show":
            self.threadDisplayGrid.remove_widget(config.threadLabelArray[i])
            self.threadDisplayGrid.remove_widget(config.threadStatusLabelArray[i])
        if config.threadStatusArray[i] == "Resolved":
            self.threadDisplayGrid.remove_widget(config.threadLabelArray[i])
            self.threadDisplayGrid.remove_widget(config.threadStatusLabelArray[i])
            self.threadDisplayGrid.add_widget(config.threadStatusLabelArray[i])
            self.threadDisplayGrid.add_widget(config.threadLabelArray[i])

def updateActorDisplay(self, text, status):

    config.actorArray.append(text)
    config.actorStatusArray.append(status)

    tag, text, sep = getActorTag(text)

    label = TextInput(text=tag, size_hint_y=None, size_hint_x=1, height=config.baseheight, font_size=config.basefont90, font_name='Fantasque-Sans', background_color=(0,0,0,0), foreground_color=styles.textcolor)
    label.bind(focus=focusChangeActorTitle)
    label.self = self
    self.actorDisplayGrid.add_widget(label)
    label.index = len(config.actorLabelArray)

    label = TextInput(text=text, size_hint_y=None, size_hint_x=1, height=config.quintupleheight, font_size=config.basefont90, font_name='Fantasque-Sans', background_color=(0,0,0,0), foreground_color=styles.textcolor)
    label.bind(focus=focusChangeActor)
    label.tag = tag
    label.sep = sep
    label.index = len(config.actorLabelArray)
    config.actorLabelArray.append(label)

    self.actorDisplayGrid.add_widget(config.actorLabelArray[-1])

    label = ClickLabel(text=status, size_hint_y=None, size_hint_x=1, font_size=config.basefont80, height=config.basefont80, font_name='Fantasque-Sans',)
    label.bind(on_press=cycleActor)
    label.background_normal=''
    label.background_color=accent1
    label.background_down=''
    label.background_color_down=accent2
    label.markup = True
    config.actorStatusLabelArray.append(label)

    self.actorDisplayGrid.add_widget(config.actorStatusLabelArray[-1])

def cycleActor(self, *args):
    if self.text == "Current":
        self.text = "Past"
        config.actorStatusArray[config.actorStatusLabelArray.index(self)] = "Past"
    elif self.text == "Past":
        self.text = "In Party"
        config.actorStatusArray[config.actorStatusLabelArray.index(self)] = "In Party"
    elif self.text == "In Party":
        self.text = "Retired"
        config.actorStatusArray[config.actorStatusLabelArray.index(self)] = "Retired"
    elif self.text == "Retired":
        self.text = "Deceased"
        config.actorStatusArray[config.actorStatusLabelArray.index(self)] = "Deceased"
    elif self.text == "Deceased":
        self.text = "Remote"
        config.actorStatusArray[config.actorStatusLabelArray.index(self)] = "Remote"
    elif self.text == "Remote":
        self.text = "Unknown"
        config.actorStatusArray[config.actorStatusLabelArray.index(self)] = "Unknown"
    elif self.text == "Unknown":
        self.text = "Don't Show"
        config.actorStatusArray[config.actorStatusLabelArray.index(self)] = "Don't Show"
    else:
        self.text = "Current"
        config.actorStatusArray[config.actorStatusLabelArray.index(self)] = "Current"
    return True

def showActor(self, *args):
    for i in range(len(config.actorStatusArray)):
        if config.actorStatusArray[i] == "Hide":
            self.actorDisplayGrid.add_widget(config.actorLabelArray[i])
            self.actorDisplayGrid.add_widget(config.actorStatusLabelArray[i])

# this is called only on a save
def clearActor(self, *args):
    for i in range(len(config.actorStatusArray)):
        if config.actorStatusArray[i] == "Don't Show":
            self.actorDisplayGrid.remove_widget(config.actorLabelArray[i])
            self.actorDisplayGrid.remove_widget(config.actorStatusLabelArray[i])

def focusChangeActor(field, value):
    if value:
        pass
    else:
        text = field.tag + field.sep + " " + field.text[0].lower() + field.text[1:]
        config.actorArray[field.index] = text

def focusChangeActorTitle(field, value):
    if value:
        pass
    else:
        label = config.actorLabelArray[field.index]
        text = field.text + label.sep + " " + label.text[0].lower() + label.text[1:]
        config.actorArray[field.index] = text
        updateActorIndex(field.self)

def focusChangeThread(label, value):
    if value:
        pass
    else:
        config.threadArray[config.threadLabelArray.index(label)] = label.text

def focusChangeText(label, value):
    if value:
        pass
    else:
        config.textArray[label.index] = label.text
        status = config.textStatusArray[label.index]
        index = label.index
        formatted_text = parseText(label.text, status)

        config.textLabelArray[index].text = formatted_text
        config.textFieldLabelArray[index].text = label.text

        field = config.textFieldLabelArray[index]
        field.height = max( (len(field._lines) + 1) * field.line_height, config.formats['basefontsize']*2 )

def getActorTag(text):

    tag = " "
    remainder = text

    sepList = [',', ':', '  ', '\n', '.']

    for sep in sepList:
        if sep in text:
            tag, remainder = text.split(sep, 1)
            if len(remainder) > 0:
                break

    tag = tag[:25]
    remainder = remainder.strip()
    if len(remainder) > 0:
        remainder =  remainder[0].upper() + remainder[1:]
    else:
        remainder = text

    #print(tag, remainder)

    return tag, remainder, sep

def updateActorIndex(self):

    self.actorIndexDisplayGrid.clear_widgets()

    tagArray = []
    tagDict = {}

    for item in config.actorArray:
        tag, remainder, sep = getActorTag(item)
        tagArray.append(tag)
        tagDict[tag] = item

    tagArray.sort()

    for tag in tagArray:

        item = tagDict[tag]

        button = Button(text=tag, size_hint=(1,None), halign='center', background_normal='', background_color=neutral, background_down='', background_color_down=accent2, font_name='Fantasque-Sans', font_size=config.basefont80, height=config.basefont90)
        button.value = config.actorArray.index(item)
        button.bind(on_press=self.pressGenericButton)
        button.bind(on_release=self.jumpToActor)
        self.actorIndexDisplayGrid.add_widget(button)

#---------------------------------------------------------------------------------------------
# save/load functions
#---------------------------------------------------------------------------------------------

def saveconfig(self, gamedir):
    try:
        tempDict = {}
        tempDict['general'] = config.general
        tempDict['user'] = config.user
        tempDict['scenario'] = config.scenario
        tempDict['formats'] = config.formats

        f = open(gamedir + 'config.txt', 'w')
        json.dump(tempDict, f)
        f.close()
    except:
        if debug == True:
            print("[saveconfig] Unexpected error:", sys.exc_info())

def loadconfig(self, gamedir):

    with open(gamedir + 'config.txt', 'r') as config_file:
        tempDict = json.load(config_file)
        config.general = tempDict['general']
        config.formats = tempDict['formats']
        config.user = tempDict['user']
        config.scenario = tempDict['scenario']
    #try:
    #    f = open(gamedir + 'config.txt', 'r')
    #    tempDict = json.load(f)
    #    for i in tempDict['general']:
    #        config.general[i] = tempDict['general'][i]
    #    for i in tempDict['user']:
    #        config.user[i] = tempDict['user'][i]
    #    for i in tempDict['scenario']:
    #        config.scenario[i] = tempDict['scenario'][i]
    #    for i in tempDict['formats']:
    #        config.formats[i] = tempDict['formats'][i]
    #    f.close()
    #except:
    #    saveconfig(self, gamedir)

def quicksave(self, gamedir):

    f = open(gamedir + 'main.txt', 'w')
    json.dump(config.textArray, f)
    f.close()

    f = open(gamedir + 'main_status.txt', 'w')
    json.dump(config.textStatusArray, f)
    f.close()

    f = open(gamedir + 'threads.txt', 'w')
    json.dump(config.threadArray, f)
    f.close()

    f = open(gamedir + 'threads_status.txt', 'w')
    json.dump(config.threadStatusArray, f)
    f.close()

    f = open(gamedir + 'actors.txt', 'w')
    json.dump(config.actorArray, f)
    f.close()

    f = open(gamedir + 'actors_status.txt', 'w')
    json.dump(config.actorStatusArray, f)
    f.close()

    f = open(gamedir + 'tracks.txt', 'w')
    tempArray = []
    for i in range(len(config.trackLabelArray)):
        tempArray.append([config.trackLabelArray[i].text, config.trackStatusLabelArray[i].active])
    json.dump(tempArray, f)
    f.close

    f = open(gamedir + 'pcs.txt', 'w')
    tempArray = []
    for pc in range(len(config.pcKeyLabelArray)):
        tempArray.append([])
        for i in range(len(config.pcKeyLabelArray[pc])):
            key = config.pcKeyLabelArray[pc][i].text
            val = config.pcValueLabelArray[pc][i].text
            tempArray[pc].append([key,val])

    json.dump(tempArray, f)
    f.close

    f = open(gamedir + 'maps.txt', 'w')
    json.dump(config.mapArray, f)
    f.close()

    updateRawHTML()
    updateRawMarkdown()
    updateCollapseHTML()
    updateFictionMarkdown()
    updateFictionHTML()

    saveconfig(self, gamedir)

def quickload(self, gamedir):

    try:
        with open(gamedir + 'main.txt', 'r') as mainfile, open(gamedir + 'main_status.txt', 'r') as statusfile:
            text = json.load(mainfile)
            status = json.load(statusfile)

        resetCenterDisplay(self, text, status)

    except:
        if config.debug == True:
            print("[quickload Main] Unexpected error:", sys.exc_info())
        updateCenterDisplay(self, "The adventure begins...", 'italic')

    try:
        with open(gamedir + 'threads.txt', 'r') as mainfile, open(gamedir + 'threads_status.txt', 'r') as statusfile:
            text = json.load(mainfile)
            status = json.load(statusfile)

        for i in range(len(text)):
            updateThreadDisplay(self, text[i], status[i])
    except:
        if config.debug == True:
            print("[quickload Threads] Unexpected error:", sys.exc_info())

    try:
        with open(gamedir + 'actors.txt', 'r') as mainfile, open(gamedir + 'actors_status.txt', 'r') as statusfile:
            text = json.load(mainfile)
            status = json.load(statusfile)

        for i in range(len(text)):
            updateActorDisplay(self, text[i], status[i])
    except:
        if config.debug == True:
            print("[quickload actors_status] Unexpected error:", sys.exc_info())

    try:
        with open(gamedir + 'tracks.txt', 'r') as filename:
            tempTable= json.load(filename)

        for x in range(len(tempTable)):
            config.trackLabelArray[x].text = tempTable[x][0]
            config.trackStatusLabelArray[x].active = tempTable[x][1]
    except:
        if config.debug == True:
            print("[quickload Tracks] Unexpected error:", sys.exc_info())

    try:
        with open(gamedir + 'pcs.txt', 'r') as f:
            tempArray = json.load(f)

        for pc in range(len(tempArray)):
            for x in range(len(config.pcKeyLabelArray[pc])):
                config.pcKeyLabelArray[pc][x].text = tempArray[pc][x][0]
                config.pcValueLabelArray[pc][x].text = tempArray[pc][x][1]
    except:
        if config.debug == True:
            print("[quickload PCs] Unexpected error:", sys.exc_info())

    try:
        with open(gamedir + 'maps.txt', 'r') as filename:
            config.mapArray = json.load(filename)

        tempVals = []
        for i in config.mapArray:
            tempVals.append(i)
        self.mapSpinner.values = tempVals
    except:
        if config.debug == True:
            print("[quickload Maps] Unexpected error:", sys.exc_info())

def makeBackup():
    saveFiles = '.' + os.sep + 'saves' + os.sep
    timestamp =  'save_{:%Y-%m-%d-%H-%M-%S}'.format(datetime.datetime.now())
    backupZip = zipfile.ZipFile('.' + os.sep + 'backups' + os.sep + timestamp + '.zip', 'w')
    for dirname, subdirs, files in os.walk(saveFiles):
        backupZip.write(dirname)
        for filename in files:
            backupZip.write(os.path.join(dirname, filename))
    backupZip.close()

def storeBookmarkLabel(label):
    try:
        index = label.index
    except:
        index = -9
    l = ToggleButtonBehavior.get_widgets('bookmarks')
    for button in l:
        if button.state == "down":
            button.index = index
            button.state = 'normal'
            button.text = str(index)
            config.general['bookmarks'][button.value] = index
    del l

def updateRawMarkdown():
    try:
        with open(config.curr_game_dir + "logs" + os.sep + "log_raw.md", "w") as log_file:
            result = "\n"
            for item in config.textArray:
                ti = config.textArray.index(item)
                item = item.strip()
                if config.textStatusArray[ti] != "ephemeral":
                    if config.textStatusArray[ti] == "italic" or config.textStatusArray[ti] == "result" or config.textStatusArray[ti] == "aside":
                        item = item.replace('\n', '*\n*')
                        result = result + "\n*" + item + "*"
                    elif config.textStatusArray[ti] == "bold" or config.textStatusArray[ti] == "query":
                        item = item.replace('\n', '**\n**')
                        result = result + "\n**" + item + "**"
                    elif config.textStatusArray[ti] == "bold_italic" or config.textStatusArray[ti] == "oracle":
                        item = item.replace('\n', '_**\n**_')
                        result = result + "\n**_" + item + "_**"
                    elif config.textStatusArray[ti] == "color1" or config.textStatusArray[ti] == "mechanic1":
                        item = item.replace('\n', '`\n`')
                        result = result + "\n`" + item + "`"
                    elif config.textStatusArray[ti] == "color2" or config.textStatusArray[ti] == "mechanic2":
                        item = item.replace('\n', '`\n`')
                        result = result + "\n`" + item + "`"
                    else:
                        result = result + "\n" + item

            # now any in block tags
            result = result.replace('[i]', '_')
            result = result.replace('[/i]', '_')
            result = result.replace('[b]', '**')
            result = result.replace('[/b]', '**')
            result = result.replace('[u]', '<u>')
            result = result.replace('[/u]', '</u>')
            result = result.replace('[s]', '<s>')
            result = result.replace('[/s]', '</s>')
            result = result.replace('[sub]', '<sub>')
            result = result.replace('[/sub]', '</sub>')
            result = result.replace('[sup]', '<sup>')
            result = result.replace('[/sup]', '</sup>')

            log_file.write(result)
    except:
        pass

def updateRawHTML():
    try:
        with open(config.curr_game_dir + "logs" + os.sep + "log_raw.html", "w") as log_file:
            result = "\n<html>\n<head>\n<title>" + config.curr_title + "</title>\n"
            style = '\n<style type="text/css">'
            style = style + "\n.italic {\nfont-style: italic;\n}"
            style = style + "\n.italicbold {\nfont-style: italic;font-weight: bold;\n}"
            style = style + "\n.bold {\nfont-weight: bold;\n}"
            style = style + "\n.highlightcolor {\ncolor: #" + config.formats['highlight_color'] + ";\n}"
            style = style + "\n.alternatecolor {\ncolor: #" + config.formats['alternate_color'] + ";\n}"
            style = style + "\n</style>\n"
            result = result + style + "</head>\n<body><!-- actual adventure starts here -->"
            # actual adventure content starts here
            for item in config.textArray:
                ti = config.textArray.index(item)
                if config.textStatusArray[ti] != "ephemeral":
                    if config.textStatusArray[ti] == "result":
                        result = result + '\n<div class="mechanic"><div class="italic">' + item + "</div></div>"
                    elif config.textStatusArray[ti] == "query":
                        result = result + '\n<div class="mechanic"><div class="bold">' + item + "</div></div>"
                    elif config.textStatusArray[ti] == "aside":
                        result = result + '\n<div class="mechanic"><div class="italic">' + item + "</div></div>"
                    elif config.textStatusArray[ti] == "oracle":
                        result = result + '\n<div class="mechanic"><div class="italicbold">' + item + "</div></div>"
                    elif config.textStatusArray[ti] == "mechanic1":
                        result = result + '\n<div class="mechanic"><div class="highlightcolor">' + item + "</div></div>"
                    elif config.textStatusArray[ti] == "mechanic2":
                        result = result + '\n<div class="mechanic"><div class="alternatecolor">' + item + "</div></div>"
                    else:
                        if config.textStatusArray[ti] == "italic":
                            result = result + '\n<div class="italic">' + item + "</div></div>"
                        elif config.textStatusArray[ti] == "bold":
                            result = result + '\n<div class="bold">' + item + "</div></div>"
                        elif config.textStatusArray[ti] == "bold_italic":
                            result = result + '\n<div class="bold_italic">' + item + "</div></div>"
                        elif config.textStatusArray[ti] == "color1":
                            result = result + '\n<div class="color1">' + item + "</div></div>"
                        elif config.textStatusArray[ti] == "color2":
                            result = result + '\n<div class="color2">' + item + "</div></div>"
                        else:
                            result = result + '\n<div class="normal">' + item + "</div></div>"

            # now any in block tags
            result = result.replace('[i]', '<i>')
            result = result.replace('[/i]', '</i>')
            result = result.replace('[b]', '<b>')
            result = result.replace('[/b]', '</b>')
            result = result.replace('[u]', '<u>')
            result = result.replace('[/u]', '</u>')
            result = result.replace('[s]', '<s>')
            result = result.replace('[/s]', '</s>')
            result = result.replace('[sub]', '<sub>')
            result = result.replace('[/sub]', '</sub>')
            result = result.replace('[sup]', '<sup>')
            result = result.replace('[/sup]', '</sup>')

            result = result +  "\n</body>\n</html>"
            log_file.write(result)
    except:
        pass

def updateCollapseHTML():

    try:
        fictionStatusList = ["plain", "italic", "bold", "bold_italic", "color1", "color2"]
        tempStatusArray = []
        tempArray = []

        for i in range(len(config.textStatusArray)):
            if config.textStatusArray[i] != "ephemeral":
                if config.textStatusArray[ti] == "result":
                    result = '\n<p class="italic">' + config.textArray[i] + "</p>\n"
                elif config.textStatusArray[ti] == "aside":
                    result = '\n<p class="italic">' + config.textArray[i] + "</p>\n"
                elif config.textStatusArray[ti] == "query":
                    result = '\n<p class="bold">' + config.textArray[i] + "</p>\n"
                elif config.textStatusArray[ti] == "oracle":
                    result = '\n<p class="italicbold">' + config.textArray[i] + "</p>\n"
                elif config.textStatusArray[ti] == "mechanic1":
                    result = '\n<p class="highlightcolor">' + config.textArray[i] + "</p>\n"
                elif config.textStatusArray[ti] == "mechanic2":
                    result = '\n<p class="alternatecolor">' + config.textArray[i] + "</p>\n"
                else:
                    if config.textStatusArray[ti] == "italic":
                        result = '\n<p class="italic">' + config.textArray[i] + "</p>\n"
                    elif config.textStatusArray[ti] == "bold":
                        result = '\n<p class="bold">' + config.textArray[i] + "</p>\n"
                    elif config.textStatusArray[ti] == "bold_italic":
                        result = '\n<p class="italicbold">' + config.textArray[i] + "</p>\n"
                    elif config.textStatusArray[ti] == "color1":
                        result = '\n<p class="highlightcolor">' + config.textArray[i] + "</p>\n"
                    elif config.textStatusArray[ti] == "color2":
                        result = '\n<p class="alternatecolor">' + config.textArray[i] + "</p>\n"
                    else:
                        result = '\n<p class="normal">' + config.textArray[i] + "</p>\n"

                tempArray.append(result)
                tempStatusArray.append(config.textStatusArray[i])

        with open(config.curr_game_dir + "logs" + os.sep + "log_raw_collapsible.html", "w") as log_file:
            count = 0
            bracket = "\n<html>\n<head>\n<title>" + config.curr_title + "</title>\n"
            script = '<script>'
            script = script + '\nfunction toggle2(showHideDiv, switchTextDiv) {'
            script = script + '\n	 var ele = document.getElementById(showHideDiv);'
            script = script + '\n	 var text = document.getElementById(switchTextDiv);'
            script = script + '\n	 if(ele.style.display == "block") {'
            script = script + '\n    		ele.style.display = "none";'
            script = script + '\n		text.innerHTML = "show";'
            script = script + '\n  	}'
            script = script + '\n	 else {'
            script = script + '\n		ele.style.display = "block";'
            script = script + '\n		text.innerHTML = "hide";'
            script = script + '\n	}'
            script = script + '\n}'
            script = script + '\nfunction toggle3(contentDiv, controlDiv) {'
            script = script + '\n        if (contentDiv.constructor == Array) {'
            script = script + '\n                for(i=0; i < contentDiv.length; i++) {'
            script = script + '\n                     toggle2(contentDiv[i], controlDiv[i]);'
            script = script + '\n                }'
            script = script + '\n        }'
            script = script + '\n        else {'
            script = script + '\n               toggle2(contentDiv, controlDiv);'
            script = script + '\n        }'
            script = script + '\n}'
            script = script + '</script>'
            style = '\n<style type="text/css">'
            style = style + "\n.italic {\nfont-style: italic;\n}"
            style = style + "\n.italicbold {\nfont-style: italic;font-weight: bold;\n}"
            style = style + "\n.bold {\nfont-weight: bold;\n}"
            style = style + "\n.highlightcolor {\ncolor: #" + config.formats['highlight_color'] + ";\n}"
            style = style + "\n.alternatecolor {\ncolor: #" + config.formats['alternate_color'] + ";\n}"
            style = style + "\n</style>\n"
            bracket = bracket + "</head>\n<body><!-- actual adventure starts here -->"

            content_string = ""
            header_string = ""
            result = ""
            chunk = False
            if tempStatusArray[0] not in fictionStatusList:
                count = count + 1
                result = result + '\n<a id="myHeader' + str(count) + '" href="javascript:toggle2(\'myContent'  + str(count) + '\',\'myHeader' + str(count) + '\');" >hide</a>'
                result = result + "\n<div id='myContent" + str(count) + "'>"
                content_string = content_string + "'myContent" + str(count) + "',"
                header_string = header_string + "'myHeader" + str(count) + "',"
                chunk = True

            for ti in range(len(tempStatusArray)):
                if tempStatusArray[ti] not in fictionStatusList and chunk == False:
                    count = count + 1
                    result = result + '\n<a id="myHeader' + str(count) + '" href="javascript:toggle2(\'myContent'  + str(count) + '\',\'myHeader' + str(count) + '\');" >collapse</a>'
                    result = result + "\n<div id='myContent" + str(count) + "'>"
                    result = result + tempArray[ti]
                    content_string = content_string + "'myContent" + str(count) + "',"
                    header_string = header_string + "'myHeader" + str(count) + "',"
                    chunk = True
                elif tempStatusArray[ti] not in fictionStatusList and chunk == True:
                    result = result + "\n" + tempArray[ti]
                elif tempStatusArray[ti] in fictionStatusList and chunk == True:
                     result = result + "</div>\n" + tempArray[ti]
                     chunk = False
                else:
                    result = result + "\n" + tempArray[ti]
                    chunk = False
                    pass

            # now any in block tags
            result = result.replace('[i]', '<i>')
            result = result.replace('[/i]', '</i>')
            result = result.replace('[b]', '<b>')
            result = result.replace('[/b]', '</b>')
            result = result.replace('[u]', '<u>')
            result = result.replace('[/u]', '</u>')
            result = result.replace('[s]', '<s>')
            result = result.replace('[/s]', '</s>')
            result = result.replace('[sub]', '<sub>')
            result = result.replace('[/sub]', '</sub>')
            result = result.replace('[sup]', '<sup>')
            result = result.replace('[/sup]', '</sup>')

            final = bracket + script + style

            final = final + '<input type="button" value="Toggle All" onClick="toggle3([' + content_string + '], [' + header_string + ']);">'

            final = final + result
            final = final +  "\n</body>\n</html>"
            log_file.write(final)
    except:
        pass

def updateFictionMarkdown():
    try:
        fictionStatusList = ["plain", "italic", "bold", "bold_italic", "color1", "color2"]
        with open(config.curr_game_dir + "logs" + os.sep + "log_fiction.md", "w") as log_file:
            result = "\n"
            for item in config.textArray:
                ti = config.textArray.index(item)
                item = item.rstrip()
                if config.textStatusArray[ti] in fictionStatusList:
                        result = result + "\n" + item

            # now replace any in block tags
            result = result.replace('[i]', '_')
            result = result.replace('[/i]', '_')
            result = result.replace('[b]', '**')
            result = result.replace('[/b]', '**')
            result = result.replace('[u]', '<u>')
            result = result.replace('[/u]', '</u>')
            result = result.replace('[s]', '<s>')
            result = result.replace('[/s]', '</s>')
            result = result.replace('[sub]', '<sub>')
            result = result.replace('[/sub]', '</sub>')
            result = result.replace('[sup]', '<sup>')
            result = result.replace('[/sup]', '</sup>')

            log_file.write(result)
    except:
        pass

def updateFictionHTML():
    try:
        fictionStatusList = ["plain", "italic", "bold", "bold_italic", "color1", "color2"]
        with open(config.curr_game_dir + "logs" + os.sep + "log_fiction.html", "w") as log_file:
            result = "\n<html>\n<head>\n<title>" + config.curr_title + "</title>\n"
            style = '\n<style type="text/css">'
            style = style + "\n</style>\n"
            result = result + style + "</head>\n<body><!-- actual adventure starts here -->"
            # actual adventure content starts here
            for item in config.textArray:
                ti = config.textArray.index(item)
                if config.textStatusArray[ti] in fictionStatusList:
                    status = config.textStatusArray[ti]
                    result = result + '\n<div class="' + status + '">' + item + "</div></div>"

            # now any in block tags
            result = result.replace('[i]', '<i>')
            result = result.replace('[/i]', '</i>')
            result = result.replace('[b]', '<b>')
            result = result.replace('[/b]', '</b>')
            result = result.replace('[u]', '<u>')
            result = result.replace('[/u]', '</u>')
            result = result.replace('[s]', '<s>')
            result = result.replace('[/s]', '</s>')
            result = result.replace('[sub]', '<sub>')
            result = result.replace('[/sub]', '</sub>')
            result = result.replace('[sup]', '<sup>')
            result = result.replace('[/sup]', '</sup>')

            result = result +  "\n</body>\n</html>"
            log_file.write(result)
    except:
        pass

def rollDice(text):

    results = "Please use standard dice notation, ie, 1d10."

    if len(text) > 0:
        try:
            count, sides = text.split("d")
        except:
            count = 1
            sides = 100
        # are we repeating?
        try:
            sides, reps = sides.split("x")
        except:
            reps = 1

        results = "Rolling " + str(count) + "d" + str(sides) + " " + str(reps) + " times."
        for m in range(int(reps)):
            resultArray = []
            result = 0
            resultstring = " "
            if int(count) and int(sides):
                for i in range(int(count)):
                    x = random.randint(1,int(sides))
                    resultArray.append(x)
                    result = result + x
                    resultstring = resultstring + " " + str(x)
            results = results + "\n[" + resultstring + "  ] " + str(result)

    return results


#---------------------------------------------------------------------------------------------------
# --> Random choosers from player defined lists
#---------------------------------------------------------------------------------------------------

def getRandomActor(key="All"):

    textarray = []
    result = "[Random actor, key: " + key + "] " + "No results found."

    for i in range(len(config.actorArray)):
        textarray.append(config.actorArray[i] + " (" + config.actorStatusArray[i]) + ")"

    if key == "All" and len(textarray) > 0:
        result = "[Random actor, key: " + key + "] " + random.choice(textarray)
    else:
        matching = [s for s in textarray if key in s]

        if len(matching) > 0:
            result = "[Random actor, key: " + key + "] " + random.choice(matching)

    return result

def getRandomThread(key="All"):

    textarray = []
    result = "[Random thread, key: " + key  + "] No results found."

    for i in range(len(config.threadLabelArray)):
        textarray.append(config.threadLabelArray[i].text + ", " + config.threadStatusLabelArray[i].text)

    if key == "All" and len(textarray) > 0:
        result = "[Random thread, key: " + key  + "] " + random.choice(textarray)
    else:
        matching = [s for s in textarray if key in s]

        if len(matching) > 0:
            result = "[Random thread, key: " + key  + " ] " + random.choice(matching)

    return result

def getRandomPC(key="Name"):

    textarray = []

    for k in range(len(config.pcKeyLabelArray)):
        for i in range(len(config.pcKeyLabelArray[k])):
            textarray.append(config.pcKeyLabelArray[k][i].text + ": " + config.pcValueLabelArray[k][i].text)

    matching = [s for s in textarray if key in s]

    if len(matching) > 0:
        result = "[Random Major Character, key: " + key  + " ] " + random.choice(matching)
    else:
        result = "[Random Major Character, key: " + key  + " ] "  + "No results found."

    return result

def getRandomTrack(key="Active"):

    textarray = []
    matching = []
    result = "[Random track, key: " + key + " ] " + "No results found."
    for i in range(len(config.trackLabelArray)):
        status = "Inactive"
        if config.trackStatusLabelArray[i].active == True:
            status = "Active"
        textarray.append(config.trackLabelArray[i].text + " (" + status + ")")

    if key == "Active":
        for i in range(len(config.trackLabelArray)):
            if config.trackStatusLabelArray[i].active == True:
                matching.append(config.trackLabelArray[i].text)
    else:
        matching = [s for s in textarray if key in s]

    if len(matching) > 0:
        result = "[Random track, key: " + key  + " ] " + random.choice(matching)

    return result

# find
def findText(self, search_string):
    # list comprehension on config.textArray
    search_terms = [search_string.lower(), search_string.capitalize(), search_string]

    resultList = []

    for term in search_terms:
        resultList = resultList + [s for s in config.textArray if term in s]

    config.general['findList'] = list(set(resultList))
    config.general['findIndex'] = 0

    self.findButton.text = "find: " + str(len(config.general['findList']))

    # get the index of the first element
    element = ""
    if len(config.general['findList']) > 0:
        element = config.general['findList'][0]

    if len(element) > 0:
        index = config.textArray.index(element)
    else:
        return "No results found."

    jumpToIndex(self, index)

def jumpToNext(self):

    if config.general['findIndex'] == len(config.general['findList'])-1:
        config.general['findIndex'] = 0
    else:
        config.general['findIndex'] = config.general['findIndex'] + 1

    element = config.general['findList'][config.general['findIndex']]
    index = config.textArray.index(element)
    jumpToIndex(self, index)

def jumpToIndex(self, index):

    edit_mode = config.general['edit_behavior']
    fieldList = ['edit', 'fic-edit']

    # this could use some catching in case the curent label is not visible for some reason

    if edit_mode in fieldList:
        self.centerDisplay.scroll_to(config.textFieldLabelArray[index])
    else:
        self.centerDisplay.scroll_to(config.textLabelArray[index])

# weighted choosers
def chooseWeighted(value, text, form):
    result_string = ""
    result = "Please enter a comma-separated list in one line that has at least as many options as needed. Excess options will be ignored."
    try:
        if value == 1:
            # 2d4
            index = 2
            chart = {}
            result_string = ""
            result = text.split(", ")
            for i in result:
                chart[index] = i
                index = index + 1
            roll = random.randint(1,4) + random.randint(1,4)
            result = chart[roll]
            for key,value in chart.items():
                result_string = result_string + "[" + str(key) + "] " + value + " "
        elif value == 2:
            # 3d6
            index = 3
            chart = {}
            result_string = ""
            result = text.split(", ")
            for i in result:
                chart[index] = i
                index = index + 1
            roll = random.randint(1,6) + random.randint(1,6) + random.randint(1,6)
            result = chart[roll]
            for key,value in chart.items():
                result_string = result_string + str(key) + ": " + value + " "
        elif value == 3:
            # 3:2:1
            roll = random.randint(1,6)
            chart = text.split(", ")
            result_string = "3: " + chart[0] + " 2: " + chart[1] + " 1: " + chart[2]
            if roll <= 3:
                result = chart[0]
                roll = 3
            elif roll <= 5:
                result = chart[1]
                roll = 2
            elif roll == 6:
                result = chart[2]
                roll = 1
        else:
            for element in text.split(", "):
                result_string = result_string + element + ", "
            result = random.choice(text.split(", "))
            roll = "Choice"

        return str(result_string), str(result), str(form), str(roll)

    except:
        return str(result_string), str(result), str("ephemeral"), str("0")

# here's full 100 item lists; I don't think these are tied in right now
def seed_action():
    chart = ['accelerate', 'accumulate', 'acquire', 'adjust', 'adopt', 'advance', 'align', 'alter', 'anger', 'anticipate', 'assist', 'assume', 'bestow', 'carry', 'change', 'clarify', 'command', 'commit', 'conclude', 'consider', 'construct', 'control', 'convince', 'couple', 'determine', 'discover', 'disregard', 'divert', 'divide', 'draw', 'dream', 'edgy', 'educate', 'emphasize', 'enable', 'enchain', 'encourage', 'endless', 'enjoy', 'enrage', 'enter', 'entrance', 'eviscerate', 'examine', 'exchange', 'execute', 'exhaust', 'experience', 'facilitate', 'fascinate', 'feint', 'guess', 'impassion', 'improvise', 'inflame', 'inflate', 'interest', 'involve', 'justify', 'keep', 'ken', 'locate', 'loosen', 'lose', 'love', 'mend', 'mesmerize', 'motivate', 'murder', 'negotiate', 'nurture', 'obscure', 'overcome', 'penalize', 'quarter', 'question', 'refuse', 'reject', 'renegotiate', 'revenge', 'run', 'share', 'simplify', 'spy', 'squelch', 'stoic', 'strengthen', 'substitute', 'synthesize', 'teach', 'tighten', 'track', 'transition', 'trap', 'triumph', 'tumble', 'unify', 'unveil', 'weaken', 'withdraw']

    return random.choice(chart)

def seed_subject():
    chart = ['addiction', 'air', 'ally', 'armor', 'art', 'beyond', 'blood', 'bravery', 'change', 'class', 'cold', 'common', 'compassion', 'consumption', 'couple', 'cowardice', 'death', 'disaster', 'dispassion', 'displeasure', 'earth', 'earth', 'elements', 'emotions', 'enemy', 'fatigue', 'focus', 'foreign', 'forgiveness', 'freedom', 'friend', 'friendship', 'fury', 'future', 'grief', 'hatred', 'health', 'home', 'honor', 'hope', 'hot', 'ideas', 'illness', 'insanity', 'instinct', 'integrity', 'jewel', 'journey', 'joy', 'key', 'kin', 'location', 'love', 'luxuries', 'master', 'moderation', 'monster', 'moon', 'music', 'near', 'necessities', 'neighbor', 'obsession', 'passion', 'past', 'path', 'physical', 'possessions', 'power', 'priceless', 'quarry', 'quest', 'rain', 'reason', 'regret', 'reserves', 'rubbish', 'sex', 'shine', 'skill', 'sorrow', 'stalemate', 'star', 'status quo', 'stoicism', 'sun', 'survival', 'task', 'tool', 'trap', 'uncontrollable', 'unknowable', 'value', 'vengeance', 'violence', 'water', 'wealth', 'weapons', 'whimsy', 'work']

    return random.choice(chart)
