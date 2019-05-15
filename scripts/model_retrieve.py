import re
import pickle
import numpy as np
import tensorflow as tf
from tensorflow import keras

# retrieving dictionary
pickle_in = open("files/dict.pickle","rb")
dictionary = pickle.load(pickle_in)

# retrieving model
model = keras.models.load_model('files/full_model.h5')

# formatting string into data so we can process it throw neural net
def stringOfWordsToTestList(tale):
    
    # splitting string to list of words
    listOfWords = re.findall(r'\w+', tale)
    
    # changing each word to it's number
    listOfNumbers = list(map(lambda y: dictionary.get(y, 0), listOfWords))
    
    # splitting list of numbers to list of lists where each list contains 128 numbers
    listOfListsOfNumbers = [listOfNumbers[x:x+128] for x in range(0, len(listOfNumbers), 128)]
    
    # preprocessing each list
    listOfListsOfNumbers = keras.preprocessing.sequence.pad_sequences(listOfListsOfNumbers,
                                                                      value=0,
                                                                      padding='post',
                                                                      maxlen=128)
    return listOfListsOfNumbers

# make prediction
def predict(stringOfWords):
    results = model.predict(stringOfWordsToTestList(stringOfWords))
    return results

# returning result
def returnAverageResult(stringOfWords):
    results = predict(stringOfWords)
    avg = np.average(results)

    output = "Average result of given text is " + str(round(avg, 2)) + "\n"
    if (avg > 0.5):
        output += "This page is OK to be read by children"
    else:
        output += "This page is not appropriate to be read by children"

    return output

print(returnAverageResult("лол кек"))
