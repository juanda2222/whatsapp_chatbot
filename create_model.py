
# things we need for NLP
import nltk
nltk.download('punkt')
#from nltk.stem.lancaster import LancasterStemmer
#stemmer = LancasterStemmer()
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer() 

# things we need for Tensorflow
import tensorflow as tf
from keras.layers import Dense
from keras.models import Sequential
from keras.preprocessing import text
from sklearn.utils import shuffle   
from sklearn.preprocessing import MultiLabelBinarizer

# other tools
import itertools
import time
from copy import copy
import pickle
import json
import random
import pickle
from pathlib import Path
import numpy as np
import pandas as pd

# constant paths
INTENTS_PATH = (Path(__file__).parent / "read_messages_function/intents.json").absolute()
TRAINING_DATA_PATH = (Path(__file__).parent / "read_messages_function/training_data.pickle").absolute()


def create_training_data(show_details=False):
        
    with open(INTENTS_PATH) as json_data:
        intents = json.load(json_data)


    ###########################################################################
    ####------ create the list of words (sentences) with synonims -------######
    ###########################################################################

    # for english synonims:
    import nltk
    from nltk.corpus import wordnet
    nltk.download('wordnet') # this is only needed if the package wordnet is not downloaded

    synonyms_tagged_sentences = [] # copy(documents)
    synonyms_words = []
    synonyms_clases = []

    # iterate each sentence
    prhase_no = 0

    # loop through each sentence in our intents patterns
    for intent in intents['intents']:

        synonyms_clases.append(intent['tag'])
        
        # loop through each sentence in the intent:
        for pattern in intent['patterns']:

            # separate the text as a list of words. like: ["this", "is", "a", "sentence"]
            sentence_list = nltk.word_tokenize(pattern)
            sentence_list = [word.lower() for word in sentence_list] # convert to lowercase

            prhase_no += 1
            synonyms_tagged_sentences.append((sentence_list, (intent['tag'],) ))
            synonyms_words.extend(sentence_list)

            # generate the tagged word list:
            tagged_phrase = nltk.pos_tag(sentence_list)

            # iterate each word
            for i, word in enumerate(sentence_list):
                
                # copy the frase to avoid overwriting of the original phrase:
                aux_phrase = copy(sentence_list)

                # get the synonim type (noun, adjective, etc...) of the word
                word_type = tagged_phrase[i][1][0].lower()
                synonym_list = []

                # Generate the synonyms list
                # avoid error with special kind of types such as "possessive wh-pronoun" identified with "w" character
                try:
                    #iterate throug synonyms
                    for syn in wordnet.synsets(word, word_type): # filter by word type j, n, i, c ,r ,v, u, p
                                    
                        # process unique synonyms
                        for synonym in syn.lemmas():

                            #print("Synonyms: ", l.name())
                            synonym_list.append(synonym.name().lower())
                    
                    # remove duplicates!
                    synonym_list = list(set(synonym_list))

                except Exception:
                    if show_details:
                        print("Synonyms not found for that type of word")
                
                # Append the new synonyms for the current word:
                for synonym in synonym_list:

                    aux_phrase[i] = synonym
                    
                    if show_details:
                        print("New phrase: ", aux_phrase, "Tag: ", (intent['tag']) , ", original No.", prhase_no )
                    
                    # add to the sentence list
                    synonyms_tagged_sentences.append( (copy(aux_phrase), (intent['tag'],) ) ) # use copy to avoid duplicates 
                    # add to the word list (for the dictionary)
                    synonyms_words.extend(aux_phrase)
                    
    # lematize and lower each word
    # synonyms_words = [lemmatizer.lemmatize(w.lower()) for w in synonyms_words if w not in ignore_words] # the bag of words keras method aleady filter
    
    # remoove duplicates
    synonyms_words = list(set(synonyms_words))
    synonyms_clases = list(set(synonyms_clases))

    if show_details:
        print(">> ", len(synonyms_tagged_sentences), "Synonyms sencences. List secction: ", synonyms_tagged_sentences[:120])
        print(">> ", len(synonyms_words), "Synonym words. List section: ", synonyms_words[:40])
        print(">> ", len(synonyms_clases), "Synonym clases. List section: ", synonyms_clases)

    """
    # optional add a permutation logic to the synonym generation (not working)

    intent_index = 0
    sentence_no = 2

    for frases in itertools.permutations(
        documents[sentence_no][intent_index],
        len(documents[sentence_no][intent_index])
        ):
        print("Frase: ", frases, "Sentence No. ", sentence_no, "intent index: ", intent_index) # [sentence as list][intent]
    """


    #####################################################################
    ####------ convert the data to numeric and save to file -------######
    #####################################################################

    # use 80% as training dataset
    TRAINING_SIZE = int( len(synonyms_tagged_sentences) * 0.8 )

    # Prepare the data for preprocessing (Create the pandas DataFrame and shuffle)
    pandas_data = pd.DataFrame(synonyms_tagged_sentences, columns = ['Sentenece', 'Tag',])  
    pandas_data = shuffle(pandas_data, random_state=22)
    print(">> data head: ", pandas_data.head())

    # create the output binary data from the dataset
    #-----------------------------------------------
    tag_encoder = MultiLabelBinarizer()
    binarized_y_data = tag_encoder.fit_transform(pandas_data["Tag"].values) # this function filters !”#$%&()*+,-./:;<=>?@[\]^_{|}~\t\n. characters    

    # separate the training y data from the testing one
    y_training_data = binarized_y_data[:TRAINING_SIZE]
    y_testing_data = binarized_y_data[TRAINING_SIZE:]

    # Print for inspection
    if show_details:
        print("Encoder classes: ", tag_encoder.classes_)
        print(len(binarized_y_data), " Binnarized Taggs. Taggs: ", binarized_y_data)
        print(len(binarized_y_data[0]), "Output size. Output example: ", binarized_y_data[0])


    # create the input binary data from the dataset
    #-----------------------------------------------
    word_tokenizer = text.Tokenizer(num_words=200) # num_words is the size of the vocabulary
    word_tokenizer.fit_on_texts(pandas_data["Sentenece"]) # use this to set up the bynary converter for the input

    # about the tokenizer:
    if show_details:
        print("Tokenizer word counts: ", word_tokenizer.word_counts)
        print("Tokenizer word docs: ", word_tokenizer.word_docs)
        print("Tokenizer word indexes: ", word_tokenizer.word_index)
        print("Tokenizer word document count: ", word_tokenizer.document_count)

    # separete the training x data to the testing one and convert it to binary matrix
    binarized_x_data = word_tokenizer.texts_to_matrix(pandas_data["Sentenece"].values)
    x_training_data = binarized_x_data[:TRAINING_SIZE]
    x_testing_data = binarized_x_data[TRAINING_SIZE:]

    # Print for inspection
    print(len(binarized_x_data), " Binnarized sentences. Sentences: ", binarized_x_data)
    print(len(binarized_x_data[0]), "Input size. Input example: ", binarized_x_data[0])


    # save all of our data structures
    with open( TRAINING_DATA_PATH, "wb" ) as pickle_data:
        pickle.dump( {
            'in_binarizer':word_tokenizer, 
            'out_binarizer':tag_encoder, 
            'train_x':x_training_data, 
            'train_y':y_training_data, 
            'test_x':x_testing_data,
            'test_y':y_testing_data,
        },  pickle_data)

    return True

def create_model(show_details=False):

    ############################################
    ####------- generate the RNN model ----#####
    ############################################

    # read the training data from the pickle file
    with open(TRAINING_DATA_PATH, "rb") as pickle_training_data:
        training_data = pickle.load(pickle_training_data)

    in_binarizer = training_data['in_binarizer']
    train_x = training_data['train_x']
    train_y = training_data['train_y']
    test_x = training_data['test_x']
    test_y = training_data['test_y']

    if show_details:
        print ("Training data loaded:")
        print ("In binarizer: ", in_binarizer)
        print (len(train_x), "Training x. X example: ", train_x)
        print (len(train_y), "Training y. Y example: ", train_y)
        print (len(test_x), "Testing x. X example: ", test_x)
        print (len(test_y), "Testing y. Y example: ", test_y)


    ############################################
    ####------- generate the RNN model ----#####
    ############################################

    # reset underlying graph data
    tf.compat.v1.reset_default_graph()

    model = Sequential()
    model.add( Dense( 40, input_shape=(len(train_x[0]),), activation="relu", name="Dense_input"))
    model.add( Dense( 15, activation="relu", name="Dense_hidden"))
    model.add( Dense( len(train_y[0]), activation="sigmoid", name="Dense_output" ))

    # set the configuration of the learning process
    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"]) 

    #print the characteristics:
    model.summary()

    # train the model
    # epochs No. of times the algoorithm will go through the entire dataset
    #batch_size is the group used to calculate the 
    model.fit(train_x, train_y, epochs=200, batch_size=20)

    if show_details:

        # test the results
        print("Model testing results:")
        print("test x set:", test_x)
        print("test y set:", test_y)

        loss, acc = model.evaluate(test_x, test_y, batch_size=20)
        print('\nTesting loss: {}, acc: {}\n'.format(loss, acc))


    # save the model to disk
    MODEL_DATA_PATH = (Path("./read_messages_function/") / "keras_model.h5").absolute()
    model.save(MODEL_DATA_PATH)

    print("Model created! saved as: ", MODEL_DATA_PATH)
    return True


if __name__ == "__main__":

    create_training_data(show_details=True)
    create_model(show_details=True)