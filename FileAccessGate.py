import os
from Database import Database
import csv
import shutil
import time


class FileAccessGate():

    def __init__(self, entries = 'TEMA_PY/entries', backup_entries = 'TEMA_PY/backup_entries'):
        self.entries = os.path.abspath (entries)
        self.backup_entries = os.path.abspath (backup_entries)
        os.makedirs(self.entries, exist_ok=True)
        os.makedirs(self.backup_entries, exist_ok=True)
        self.db = Database()


    # Method to process new files
    def process_new_files(self):
        while True:
            files = os.listdir(self.entries)
            for file_name in files:
                if file_name.startswith("gate") and file_name.endswith(".csv"):
                    gate_id = self.extract_gate_number(file_name)
                    self.process_file(file_name, gate_id)
                    self.move_to_backup(file_name)
                if file_name.startswith("gate") and file_name.endswith(".txt"):
                    gate_id = self.extract_gate_number(file_name)
                    self.process_file(file_name, gate_id)
                    self.move_to_backup(file_name)
            time.sleep(10)  # Check every 10 seconds for new files
           

    # Method to process individual file
    def process_file(self, file_name, gate_id):
        file_path = os.path.join(self.entries, file_name)
        print(f"Processing file: {file_path}")
        if file_name.endswith(".csv"):
            with open(file_path, 'r') as file:
                csv_reader = csv.reader(file)
                header = next(csv_reader, None)
                # print(f"CSV Header: {header}")
                for row in csv_reader:
                    try:
                        user_id = int(row[0])
                        date = row[1] #'%Y-%m-%dT%H:%M:%S'
                        direction = row[2]
                        # Insert into MySQL database
                        self.db.insert_access_record(user_id, date, gate_id, direction)
                        print(f"Processed entry for User ID {user_id} at gate {gate_id}")
                    except ValueError as e:
                        print(f"Error processing row: {row}. Error: {e}")
                    except Exception as e:
                        print(f"Unexpected error: {e}")
        elif file_name.endswith(".txt"):
            with open(file_path, 'r') as file:
                for line in file:
                    try:
                        # Assuming the TXT format is comma-separated like CSV
                        row = line.strip().split(',')
                        user_id = int(row[0])
                        date = row[1] 
                        direction = row[2]
                        # Insert into MySQL database
                        self.db.insert_access_record(user_id, date, gate_id, direction)
                        print(f"Processed entry for User ID {user_id} at gate {gate_id}")
                    except ValueError as e:
                        print(f"Error processing line: {line}. Error: {e}")
                    except Exception as e:
                        print(f"Unexpected error: {e}")
    # Method to extract gate number from the file name
    def extract_gate_number(self, file_name):
        return int(file_name.split('gate')[1].split('.')[0])


    # Method to move processed files to backup
    def move_to_backup(self, file_name):
        try:
            entries = os.path.join(self.entries, file_name)
            backup = os.path.join(self.backup_entries, file_name)
            # print(f"Moving {entries} to {backup}...")
            shutil.move(entries,backup)
            # print(f"Moved {file_name} to backup directory.")
        except Exception as e:
            print(f"Error moving file {file_name}: {e}")

# if __name__ == "__main__":
    
#     # Instantiate the file processor with the database connection
#     file_processor = FileAccessGate()
    
#     try:
#         # Continuously process new files
#         file_processor.process_new_files()
#     except KeyboardInterrupt:
#         # Safely close the database connection when interrupted
#         file_processor.db.close()
#         print("Processing stopped. Database connection closed.")