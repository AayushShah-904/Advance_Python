

class InvalidInputDataError(Exception):
    pass

pattern = r'^[a-zA-Z]+$'  
def process_file(filename):
    try:
        with open(filename, "r") as f:
            data = f.read().strip()
            print(data) 
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
