import numpy as np
import pandas as pd 
import sys

sys.path.append('../Preprocess-Data/')
from category_reducer import category_reducer

def load_data():
    '''
    # Load the data from the csv file and reduce the number of categories
    '''
    data_path = "../Data/news-data-with-imgs.csv"
    data = pd.read_csv(data_path)
    df = data.copy()

    df = category_reducer(df)
    print(df.info())
    df = df[['Content', 'Title', 'img_path']]
    df = df[:10]
    return df

from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import array_to_img

class PreProcessImg:
    '''
    # Class to preprocess the images and get the size information of the images.
    '''
    def __init__(self, df):
        self.loaded_imgs = []
        self.img_arrays = []
        self.df = df

    def load_img(self, target_size=None):
        for img in self.df['img_path']:
            img = img.replace('\\', '/')
            img = load_img(img, target_size=target_size)
            self.loaded_imgs.append(img)

        return self.loaded_imgs

    def img_to_array(self):
        '''
        # Load the images from the directory

        Returns:
            - loaded_imgs: List of loaded images
        '''
        for img in self.loaded_imgs:
            img = img_to_array(img)
            self.img_arrays.append(img)

        return np.array(self.img_arrays) / 255.0

    def get_size_info(self, loaded_imgs):
        '''
        # Get the size information of the images

        Args:
            - loaded_imgs: list of loaded images

        Returns:
            - weights_mean: Mean of the weights of the images
            - weights_std: Standard deviation of the weights of the images
            - heights_mean: Mean of the heights of the images
            - heights_std: Standard deviation of the heights of the images
        '''
        img_weights = []
        img_heights = []
        for size in loaded_imgs:
            img_weights.append(size.size[0])
            img_heights.append(size.size[1])

        max_weight = max(img_weights)
        min_weight = min(img_weights)
        weights_mean = np.mean(img_weights)
        weights_std = np.std(img_weights)

        max_height = max(img_heights)
        min_heigth = min(img_heights)
        heights_mean = np.mean(img_heights)
        heights_std = np.std(img_heights)

        print("Max width: ", max_weight)
        print("Min width: ", min_weight)
        print("Mean width:", weights_mean)
        print("Standard deviation of widths:", weights_std)
        print("==")
        print('Max height:', max_height)
        print('Min height:', min_heigth)
        print("Mean height:", heights_mean)
        print("Standard deviation of heights:", heights_std)


from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

class PreprocessText(Tokenizer):
    '''
    # Class to tokenize and pad the text data

    Args:
        - data: The text data list or series to be tokenized and padded
    '''
    def __init__(self, data):
        super().__init__(filters='!"#$%&()*+,-./:;=?@[\\]^_`{|}~\t\n')

        self.start_mark = '<start> '
        self.end_mark = ' <end>'

        self.data = data.apply(lambda x: self.start_mark + x + self.end_mark)

        self.fit_on_texts(self.data)
        self.tokens = self.texts_to_sequences(self.data)

        self.vocab_size = len(self.word_index) + 1
        self.numbers_of_words = [len(token) for token in self.tokens]
        self.max_tokens = max(self.numbers_of_words)

        self.padded_tokens = pad_sequences(self.tokens, padding='post', truncating='post')

    # padding the token
    @staticmethod
    def pad_data(text, max_tokens=None):
        '''
        # Pad the tokens to a new maximum length

        Args:
            - text: The tokens to be padded
            - max_tokens: The maximum length of the tokens

        Returns:
            - np.array: The padded tokens
        '''
        padded_tokens = pad_sequences(text, maxlen=max_tokens, padding='post', truncating='post')
        return padded_tokens

    def generate_data(self, image_data):
        '''
        # Generate the data for the model based on the next word prediction.
        # First token is input and the second token is output and so on till the end of the sequence.

        * Example:
            - title = "Sel felaketi sonucu 3 vatandaş kayıp"
            - word_index = {'Sel': 9, 'felaketi': 5, 'sonucu': 3, '3': 7, 'vatandaş': 5, 'kayıp': 6 }
            - tokens: [start_token, 9, 5, 3, 7, 5, 6, end_token]

            | Input                                         |   Output    |
            | --------------------------------------------  | ----------  |
            | Image + start_token                           |     9       |
            | Image + start_token + 9                       |     5       |
            | Image + start_token + 9 + 5                   |     3       |
            | Image + start_token + 9 + 5 + 3               |     7       |
            | Image + start_token + 9 + 5 + 3 + 7           |     5       |
            | Image + start_token + 9 + 5 + 3 + 7 + 5       |     6       |
            | Image + start_token + 9 + 5 + 3 + 7 + 5 + 6   |  end_token  |

        Args:
            - image_data: The image data
            - max_tokens: The maximum length of the tokens

        Returns:
            - np.array: The image and text data
        '''
        X_images_list, X_texts_list, y_texts_list = [], [], []

        for img, seq in zip(image_data, self.padded_tokens):
            for i in range(1, len(seq)):
                in_seq, out_seq = seq[:i], seq[i]
                in_seq = pad_sequences([in_seq], maxlen=self.max_tokens)[0]
                out_seq = to_categorical([out_seq], num_classes=self.vocab_size)[0]
                X_images_list.append(img)
                X_texts_list.append(in_seq)
                y_texts_list.append(out_seq)

        self.X_images = np.array(X_images_list)
        self.X_texts = np.array(X_texts_list)
        self.y_texts = np.array(y_texts_list)

        return self.X_images, self.X_texts, self.y_texts

    def token_to_text(tokens):
        """
        # Convert the tokens to text

        Args:
            - tokens: The tokens to be converted

        Returns:
            - str: The text
        """
        text = ' '.join(tokenizer.index_word[token] for token in tokens)
        return text

    def text_to_token(text):
        """
        # Convert the text to tokens

        Args:
            - text: The text to be converted

        Returns:
            - list: The tokens
        """
        tokens = tokenizer.texts_to_sequences([text])[0]
        return tokens
    def get_info(self):
        '''
        # Get the information about the tokenized and padded data
        '''
        print("Max tokens: ", self.max_tokens)
        print("Min tokens: ", min(self.numbers_of_words))
        print("Mean tokens: ", int(np.mean(self.numbers_of_words)))
        print("Standard deviation of tokens: ", int(np.std(self.numbers_of_words)))
        print("Vocabulary Size: ", len(self.word_index) +1 )
        print('Shape of padded tokens: ', self.padded_tokens.shape)
        print('X_images shape: ', self.X_images.shape)
        print('X_texts shape: ', self.X_texts.shape)
        print('y_texts shape: ', self.y_texts.shape)