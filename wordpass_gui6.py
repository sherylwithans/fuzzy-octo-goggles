from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys

import pandas as pd
import numpy as np

# to disable chained assignment warnings b/c we overwrite original df
pd.options.mode.chained_assignment = None

def get_df(filename):
    return pd.read_csv(filename)

# read vocabulary.csv as dataframe and add 'proficiency', 'index' columns if necessary
def read_file(filename):
    df = get_df(filename)
    col_name = df.columns.tolist()

    if 'proficiency' not in col_name:
        df['proficiency'] = None
    if 'index' not in col_name:
        df.to_csv(filename, index_label = 'index')
    else:
        df.to_csv(filename, index=False)

# write results from sub df to original file (update proficiency)
def write_file(filename,df_sub):
    df_new = get_df(filename)
    for t in zip(df_sub['index'],df_sub['proficiency']):
        i = t[0]
        v = t[1]
        df_new['proficiency'].iloc[i] = v
    df_new.to_csv(filename, index=False)


# returns a dataframe of random quiz words,definitions and randomized choices list with correct answer index
def quiz(number,df):
    import random
    result = {}
    
    # Quiz the words whose proficiency is not 1
    unknown_df = df[(df['proficiency'].notnull()) & (df['proficiency'] != 1)]
    length = len(unknown_df)

    #Quiz words whose proficiency is not 1 first
    if length >= number:
        quiz_df = unknown_df[: number]
    elif length >= 1:
        quiz_df = pd.concat([unknown_df, df[df['proficiency'].isnull()].sample(n=number-length)])[: number]
    # if no words have proficiency marked, quiz from entire df
    else:
        quiz_df = df.sample(n=number)
        
    quiz_df['choices'] = None
    quiz_df['correct_index'] = None

    for i in range(number):
        #choose 3 definition  randomly from the whole word list.
        choices = list(df.sample(n=3, replace = True)['definitions'])  
        solution = quiz_df['definitions'].iloc[i]
        # Produce choices in a random order.
        flag = random.randint(0,3)
        choices.insert(flag, solution)

        quiz_df['choices'].iloc[i]=choices
        quiz_df['correct_index'].iloc[i]=flag

    return quiz_df

class Communicate(QObject):
    # this class creates a custom signal object to send signals to main window
    myGUI_signal = pyqtSignal(str)

class CustomDialog(QInputDialog):
    # this class creates a pop up dialog for users to select number of words to memorize/quiz
    def __init__(self, text, *args, **kwargs):
        super(CustomDialog, self).__init__(*args, **kwargs)

        self.setComboBoxItems([str(i) for i in range(10,60,10)])
        self.setLabelText(text)

class InitialWidget(QWidget):
    # this class creates the home page widget for users to choose between memorize and quiz functions
    def __init__(self, callbackFunc, *args, **kwargs):
        super(QWidget, self).__init__(*args, **kwargs)

        self.mySrc = Communicate()
        self.mySrc.myGUI_signal.connect(callbackFunc) 

        #button layout
        memorize_btn = QPushButton('Memorize')
        memorize_btn.clicked.connect(lambda x: self.btn_clicked('memorize'))
        quiz_btn = QPushButton('Quiz')
        quiz_btn.clicked.connect(lambda x: self.btn_clicked('quiz'))
        button_layout = QHBoxLayout()
        button_layout.addWidget(memorize_btn)
        button_layout.addWidget(quiz_btn)

        #full layout
        initial_layout = QVBoxLayout()
        initial_layout.setSpacing(100)
        initial_layout.setContentsMargins(150,150,150,150)
        welcome = QLabel("Welcome to WordPass, your awesome vocabulary builder")
        welcome.setAlignment(Qt.AlignCenter)
        font = QFont("Times", 15)
        welcome.setFont(font)
        description = QLabel(" Please select your goal today.")
        description.setAlignment(Qt.AlignCenter)
        initial_layout.addWidget(welcome)
        initial_layout.addWidget(description)
        initial_layout.addLayout(button_layout)

        self.setLayout(initial_layout)

    # sent a signal to report which button is clicked and number of words selected
    def btn_clicked(self,s):
        dlg = CustomDialog('What would you like to ' + s + ' today?')
        if dlg.exec_():
            i = int(dlg.textValue())
            if s=='memorize':
                self.mySrc.myGUI_signal.emit('0'+str(i))
            elif s=='quiz':
                self.mySrc.myGUI_signal.emit('1'+str(i))


class MemorizeWidget(QWidget):
    # this class creates a widget layout for users to memorize/learn words
    def __init__(self, quiz_num, filename, *args, **kwargs):
        super(QWidget, self).__init__(*args, **kwargs)
        
        self.filename = filename

        #layout for memorizing mode
        buttonlayout = QHBoxLayout()
        button_namelist = ["I don't know","Looks familiar","I know this"]
        self.button_list = []
        buttonlayout.setContentsMargins(25,25,25,25) 
        i = -1
        for b in button_namelist:
            button = QPushButton(b)
            self.button_list.append(button)
            button.pressed.connect(lambda i = i: self.btn_pushed(i))
            buttonlayout.addWidget(button)
            i += 1
        
        self.quiz_num = quiz_num
        self.df = get_df(self.filename).sample(n=self.quiz_num)

        #layout for display screen (flashcard)
        self.displaylayout = QVBoxLayout()
        self.displaylayout.setContentsMargins(50,50,75,50)
        self.selected_index = 0
        self.card = QPushButton(self.df['words'].iloc[self.selected_index])
        self.card.setMinimumWidth(800)
        self.card.setMinimumHeight(300)
        self.card.clicked.connect(lambda x: self.card_clicked(self.card))
        self.displaylayout.addWidget(self.card)
        self.displaylayout.addLayout(buttonlayout)
        
        self.setLayout(self.displaylayout)
            
    # records user proficiency and calls next card click, or writes results to file
    def btn_pushed(self,i):
        p = self.df['proficiency'].iloc[self.selected_index]
        if np.isnan(p):
            self.df['proficiency'].iloc[self.selected_index] = i
        else:
            self.df['proficiency'].iloc[self.selected_index] += i

        self.selected_index += 1

        if self.selected_index==self.quiz_num:
            write_file(self.filename,self.df)

        self.card_clicked(self.card)
        
    # card flips between word and definition or displays "finish"
    def card_clicked(self,c):
        if self.selected_index >= self.quiz_num:
            c.setText('You have finished all the words for this session!\n\nPlease click the home button on the menubar\nto go back to homepage.')
            for i in self.button_list:
                i.hide()

        elif c.text() == self.df['words'].iloc[self.selected_index]:
            c.setText('Definition:\n'+self.df['definitions'].iloc[self.selected_index])
        else:
            c.setText(self.df['words'].iloc[self.selected_index])


class QuizWidget(QWidget):
    #this class creates a quiz widget from a given quiz dataframe and exports results to file
    #constructor
    def __init__(self, quiz_df, filename, *args, **kwargs):
        super(QWidget, self).__init__(*args, **kwargs)

        self.filename = filename
        self.correct_num, self.incorrect_num = 0,0
        self.result_list=[]
        self.df = quiz_df
        self.index = 0

        self.instruction = QLabel('Please select the correct definition for: ' + self.df['words'].iloc[self.index])

        #create radio buttons
        self.button_list=[]
        a = ['A. ','B. ','C. ','D. ']
        for i in range(4):
            self.button_list.append(QPushButton(str(i)))
        self.set_choice_btn(self.df['choices'].iloc[self.index])

        #create layout for radio buttons and add them
        self.button_layout = QVBoxLayout()

        #add buttons to the layout
        counter = 0
        for each in self.button_list:
            self.button_layout.addWidget(each)
            each.pressed.connect(lambda counter = counter: self.button_clicked(counter))
            counter += 1

        self.mainlayout = QVBoxLayout()
        self.mainlayout.addWidget(self.instruction)
        self.mainlayout.addLayout(self.button_layout)
        self.mainlayout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.mainlayout)

    # set text for choices buttons
    def set_choice_btn(self,choices):
        a = ['A. ','B. ','C. ','D. ']
        for i in range(4):
            self.button_list[i].setText(a[i]+choices[i])

    # get choice values for current self.index
    def get_values(self, i):
        word = self.df['words'].iloc[self.index]
        choices = self.df['choices'].iloc[self.index]
        correct_index = self.df['correct_index'].iloc[self.index]
        correct_ans = self.df['definitions'].iloc[self.index]
        user_ans = self.df['choices'].iloc[self.index][i]
        return word, choices, correct_index, correct_ans, user_ans

    # record correct answer and update self.df proficiency value on each button click
    def button_clicked(self,s):
        word, choices, correct_index, correct_ans, user_ans = self.get_values(s)
        if s == correct_index:
            self.result_list.append((word,correct_ans,'Correct'))
            self.correct_num+=1
            f = 1
        else:
            self.result_list.append((word,correct_ans,user_ans))
            self.incorrect_num+=1
            f = -1
            
        # add to proficiency value if not None, else set to value
        p = self.df['proficiency'].iloc[self.index]
        if not np.isnan(p):
            self.df['proficiency'].iloc[self.index] += f
        else:
            self.df['proficiency'].iloc[self.index] = f  

        self.index+=1
        self.next_quiz()

    # go to next word
    def next_quiz(self):
        if self.index <= len(self.df)-1:
            word, choices, correct_index, correct_ans, user_ans = self.get_values(1)
            self.set_choice_btn(choices)
            self.instruction.setText('Please select the correct definition for: ' + word)
        else:
            for i in range(4):
                self.button_list[i].hide()

            accuracy = 100*self.correct_num/(self.incorrect_num+self.correct_num)
            if accuracy >= 80:
                evaluation = 'Excellent!'
            elif accuracy >= 60:
                evaluation = 'Great!'
            else:
                evaluation = 'Keep fighting!'
            self.instruction.setText('Great work! Here are your results:\nScore: '\
                                    +'%1.2f%%'%accuracy\
                                    +f' ({self.correct_num}/{self.incorrect_num+self.correct_num})'\
                                    +'\n'\
                                    +evaluation)
            self.mainlayout.addWidget(ResultWidget(self.result_list))
            write_file(self.filename,self.df)


class ResultWidget(QWidget):
    # this class creates a table widget to display quiz results
    def __init__(self, result_list, *args, **kwargs):
        super(QWidget, self).__init__(*args, **kwargs)

        #create table for result view
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Word","Correct Answer","Your Answer"])

        self.table.setRowCount(len(result_list))
        for i in range(len(result_list)):
            for j in range(len(result_list[i])):
                s = QTableWidgetItem(result_list[i][j])
                s.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(i,j,s)

        self.table.resizeColumnsToContents()

        # set result widget layout
        self.layout = QVBoxLayout()
        self.layout.setSpacing(50)
        self.layout.setAlignment(Qt.AlignHCenter)
        self.layout.setContentsMargins(50,50,50,50)
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)


class MainWindow(QMainWindow):
    #this class is the MainWindow class, and will be executed until termination
    def __init__(self, filename, *args, **kwargs):
        #always call the super init function to avoid error
        super(MainWindow, self).__init__(*args,**kwargs)

        #set window title, function of QMainWindow Class
        self.setWindowTitle("WordPass: My Awesome Vocabulary Builder")
        self.setCentralWidget(InitialWidget(callbackFunc=self.my_signal))

        # initialize file
        self.filename = filename
        read_file(self.filename)

        home_btn= QAction( "&Home", self)
        home_btn.setStatusTip("Exit current session and go back to home page.")           
        home_btn.triggered.connect(self.home_clicked)
        # gen_new.setCheckable(True)
        home_btn.setShortcut(QKeySequence("Ctrl+h"))

        #set status bar
        self.setStatusBar(QStatusBar(self))

        #add menu 
        menu = self.menuBar()                               
        menu.addAction(home_btn)  
        menu.setNativeMenuBar(False)

    # this function returns to home page
    def home_clicked(self):
        self.setCentralWidget(InitialWidget(callbackFunc=self.my_signal))

    # this function sets central widget to either memorize or quiz based on custom signal
    def my_signal(self,s):
        f,i = int(s[0]),int(s[1:])
        
        # load file
        df = get_df(self.filename)
        # only quiz/learn words that have not been marked "I know this" (proficiency=1)
        df = df[df['proficiency'] != 1]
        
        if f == 0:
            self.setCentralWidget(MemorizeWidget(quiz_num = int(s[1:]), filename = self.filename))
        elif f == 1:
            x = quiz(i,df=df)
            self.setCentralWidget(QuizWidget(quiz_df = x, filename = self.filename))

#sys.argv allows pass command line arguments to application
app = QApplication.instance()
if app is None:
    app = QApplication(sys.argv)

#create window instance (after create QApplication instantce but before enter event loop)
window = MainWindow(filename = 'vocabulary.csv') 
window.show()

#enter the event loop
app.exec_()