# WordPass -- Vocabulary Flashcards

WordPass is a powerful tool designed for those struggling with the massive amount of words. If you are preparing for language tests, such as GRE and GMAT, WordPass can help you memorize words and greatly improve learning efficiency.

WordPass uses Python 3.6.

### New Features

  - Containing Learning Mode and Quiz Mode
  - Users can select the number of words to learn/be quizzed on.
  - Users can choose whatever vocabulary they want to learn.

### Main Sections

WordPass contains the following sections:

* “Flashcard” Function -- Users can toggle between word and definition upon mouse click.
* Memorization/Learning mode -- By selecting between “I know this”, “Familiar”, and “I don’t know”, words will be sorted into corresponding datasets and retrieved repeatedly until user “knows” all words.
* Quiz mode -- Users will be quizzed on words they have learnt through multiple choice, fill in the blank and true/false questions.


### Prerequisites

First, make sure python is updated to python3.

```sh
$ python --version
$ conda update python
$ conda install python=3.6
$ python3 --version
```


### Run Instructions

Users can choose any word list they want to learn by saving the word list file as "vocabulary.csv". After openning the interface, you can choose learning mode (Memorization Mode/Quiz Mode) and how many words are you going to learn. 

By clicking the "Memorization" button, words along with their definitions will show up. You need to choose to what extend you know the given word and "WordPass" will save the infomation to memory for future learning.

By clicking the "Quiz" button, you will be given a quiz with multiple choices to check whether you have mastered those learned words in Memorization Mode. You can see your score after the quiz and the correct answer of your mistake will also be shown. The quiz record will be saved to memory too. 

All the learning records will be updated after each Memorization or Quiz so you can start from current level next time. Therefore, "WordPass" is quite a useful tool to learn words.


### Contribute

Contributions are welcome! Just open a pull request and we will attend to it as soon as possible.

