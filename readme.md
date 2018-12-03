# WordPass -- Vocabulary Flashcards

- Group Name: WordPass, Section 2
- Team Members: Jing Chen, Beichen Liu, Jingyi Wu, Shengsheng Zhou

WordPass is a powerful tool designed for those struggling with the massive amount of words. If you are preparing for language tests, such as GRE and GMAT, WordPass can help you memorize words and greatly improve learning efficiency.

WordPass uses Python 3.6

### New Features

  - Containing Learning Mode and Quiz Mode
  - Users can select the number of words to learn/be quizzed on.
  - Users can view quiz results after each quiz session。

### Main Sections

WordPass contains the following sections:

* “Flashcard” Function -- Users can toggle between word and definition upon mouse click. Users move onto the next word by selecting between "I know this", "Familiar", and "I don't know".
* Memorization/Learning mode -- By selecting between “I know this”, “Familiar”, and “I don’t know”, words will be categorized into corresponding datasets for the user to be tested on when selecting Quiz mode.
* Quiz mode -- Users will be quizzed on words they have learnt through multiple choice questions, with priority given to words marked as "I don't know".


### Prerequisites

First, make sure python is updated to python3. If Anaconda is installed, please update and run the program through Anaconda.

```sh
$ python --version
$ conda update python
$ conda install python=3.6
$ python3 --version
```
If Anaconda is not installed, please ensure PyQt5 is installed in the system.

```sh
$ sudo apt-get install -y python3-pip
$ pip3 install pyqt5
```
Please look at requirements.txt for more detailed information.

### Run Instructions

Please ensure the file "vocabulary.csv" exists within the same directory as the program.

After opening the interface, you can choose learning mode (Memorization Mode/Quiz Mode) and how many words you are going to learn from the drop down list. 

By clicking the "Memorization" button, words along with their definitions will show up. You need to choose to what extent you know the given word and "WordPass" will save the infomation to memory for future learning. The flashcard will toggle between the word and its definition when clicked. The next word will be shown only after one of the buttons "I know this", "Familiar", "I don't know" is clicked.

By clicking the "Quiz" button, you will be given a quiz with multiple choices to check whether you have mastered those learned words in Memorization Mode. You can see your score after the quiz and the correct answer of your mistakes will be shown. The quiz results will also contribute to the calculation of the user's proficiency of a given word.

All the learning records will be updated after each Memorization or Quiz so you can start from current level next time. Therefore, "WordPass" is quite a useful tool to learn words.


### Contribute

Contributions are welcome! Just open a pull request and we will attend to it as soon as possible.

