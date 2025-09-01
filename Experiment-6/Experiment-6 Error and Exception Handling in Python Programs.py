import re
from collections import Counter  # Add for character frequencies
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class InvalidInputDataError(Exception):
    pass

pattern = r'^[a-zA-Z \n]+$'

def process_file(filename):
    try:
        with open(filename, "r") as f:
            data = f.read()
            word_count = data.split()
            print(data)
            
            # Calculate character frequencies (excluding spaces)
            char_freq = {}
            for c in data:
                if c in char_freq:
                    char_freq[c] += 1
                else:
                    char_freq[c] = 1
            print("Character frequencies :")
            for char, freq in char_freq.items():
                print(f"'{char}': {freq}")
            
            print(f"Number of words in the file are {len(word_count)}")

            word_cloud = WordCloud(width=1600, height=1200, background_color='white').generate(data)
            plt.imshow(word_cloud, interpolation='bilinear')
            plt.axis("off")
            plt.show()
            if not re.search(pattern, data):
                raise InvalidInputDataError(f"Error: Data does not match the required pattern: {data}")
            return data
    except FileNotFoundError:
        print("File not found.")
    except InvalidInputDataError as e:
        print(f"InvalidInputDataError: {e}")

if __name__ == "__main__":
    filename = "file.txt" 
    process_file(filename)
