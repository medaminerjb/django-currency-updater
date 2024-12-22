import json
import os  # Import os for file path handling

symbols_file = os.path.join(os.path.dirname(__file__), 'data', 'symbols.json')
print(symbols_file)
def load_symbols():
        """
        Load symbols from the symbols.json file.
        """
        # Assuming symbols.json is located inside a data folder within the app
        symbols_file = os.path.join(os.path.dirname(__file__), 'data', 'symbols.json')
        
        # Check if the symbols.json exists
        if not os.path.exists(symbols_file):
            print("symbols.json file not found!")
            return {}

        # Load the symbols from the file
        with open(symbols_file, 'r') as file:
            symbols_data = json.load(file)

        return symbols_data

load_symbols()
