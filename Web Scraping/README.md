# News Generation

## Introduction

This project is a part of the Teknofest 2024 Türkçe Doğal Dil İşleme competition. The aim of the project is to
generate news title and content from a given image.

## Dataset

The dataset is collected from the ![Sabah](https://www.sabah.com.tr/timeline/) news website.
The dataset consist of news titles, news content and images. The dataset is in Turkish Language.

## Data-Preprocessing

- Sample Data:
  ![image](https://isbh.tmgrup.com.tr/sbh/2022/03/31/balikesirde-tarihi-binada-baslayan-ve-restorana-sicrayan-yangin-sonduruldu-1648686422986.jpeg)

  ***

  ```python
    title = "Balıkesir’de tarihi bina yangında küle döndü"
    word_index = {'Balıkesir’de': 9, 'tarihi': 5, 'bina': 3, 'yangında': 7, 'küle': 5, 'döndü': 6 }
    tokens: [start_token, 9, 5, 3, 7, 5, 6, end_token]
  ```

  | Input                                       | Output    |
  | ------------------------------------------- | --------- |
  | Image + start_token                         | 9         |
  | Image + start_token + 9                     | 5         |
  | Image + start_token + 9 + 5                 | 3         |
  | Image + start_token + 9 + 5 + 3             | 7         |
  | Image + start_token + 9 + 5 + 3 + 7         | 5         |
  | Image + start_token + 9 + 5 + 3 + 7 + 5     | 6         |
  | Image + start_token + 9 + 5 + 3 + 7 + 5 + 6 | end_token |

## Model

The model is a combination of CNN and LSTM, where the image is fed to the Encoder(CNN) and the output of the CNN is
fed to the Decoder(LSTM) along with the input text.
