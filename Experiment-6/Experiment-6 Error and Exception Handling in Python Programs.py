import re
from collections import Counter  # This will be used now
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import sys  # Used for exiting on critical errors

# --- Custom Exceptions ---
class InvalidInputDataError(Exception):
    pass

class DiskSpaceFullError(Exception):
    pass

# --- Main Functions ---

def process_file(filename):
    """
    Reads a file, validates its content, and generates a WordCloud object.
    """
    try:
        with open(filename, "r") as f:
            data = f.read()

        # 1. Validate data FIRST
        if not data.strip():
            print(f"Error: File '{filename}' is empty.")
            return None  # Return None to signal failure

        # 2. Perform regex check (Note: this pattern is very strict)
        # It will fail if *any* punctuation (like '.' or ',') is present.
        pattern = r'^[a-zA-Z \n]+$'
        if not re.search(pattern, data):
            raise InvalidInputDataError(f"Error: Data does not match the required pattern (letters, spaces, newlines only).")

        print("--- File Content ---")
        print(data)
        print("--------------------")

        # 3. Calculate character frequencies using Counter
        #    This now respects the "excluding spaces" comment
        filtered_chars = data.replace(" ", "").replace("\n", "")
        char_freq = Counter(filtered_chars)
        
        print("Character frequencies (excluding spaces/newlines):")
        for char, freq in char_freq.items():
            print(f"'{char}': {freq}")
        
        # 4. Calculate word count
        word_count = data.split()
        print(f"\nNumber of words in the file are {len(word_count)}")

        # 5. Generate and return the WordCloud object
        print("Generating word cloud...")
        word_cloud = WordCloud(width=1600, height=1200, background_color='white').generate(data)
        
        # Show the plot
        plt.imshow(word_cloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()

        return word_cloud

    except FileNotFoundError:
        print(f"Error: File not found at '{filename}'")
    except InvalidInputDataError as e:
        print(f"InvalidInputDataError: {e}")
    
    return None  # Return None on any handled error

def save_wordcloud_image(word_cloud, output_file):
    """
    Saves the generated WordCloud object to a file.
    Handles potential disk space errors.
    """
    # This function was well-written, but needs to handle a None input
    if word_cloud is None:
        print("Error: Cannot save word cloud, processing failed.")
        return

    try:
        word_cloud.to_file(output_file)
        print(f"\nSuccessfully saved word cloud to {output_file}")
    except OSError as e:
        # errno 28 corresponds to "No space left on device"
        if e.errno == 28:
            raise DiskSpaceFullError(f"Disk space is full. Cannot write to '{output_file}'.") from e
        else:
            # Re-raise other/unexpected OS errors
            raise

# --- Main execution block ---

if __name__ == "__main__":
    filename = "file.txt" 
    output_file = "wordcloud.png"  # Use a proper image extension
    
    try:
        # 1. Process the file
        wc_object = process_file(filename)
        
        # 2. Save the result (only if processing was successful)
        save_wordcloud_image(wc_object, output_file)
            
    except DiskSpaceFullError as e:
        # This is the correct place to catch this error
        print(f"Critical Error: {e}")
        sys.exit(1)  # Exit with a non-zero status
    except Exception as e:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred: {e}")