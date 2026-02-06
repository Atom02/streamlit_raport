from data_processor import parse_data, save_to_db, init_db, DB_PATH
import pandas as pd
from sqlalchemy import create_engine, text

# Mock parse_data to use local file
# We will just run the logic of parse_data and save_to_db here to debug

try:
    with open('excel_input.xlsx', 'rb') as f:
        # We need to pass a file-like object with a name attribute for my parse_data function
        class FileMock:
            def __init__(self, f, name):
                self.f = f
                self.name = name
            def read(self, *args):
                return self.f.read(*args)
            def seek(self, *args):
                return self.f.seek(*args)
            def __iter__(self):
                return self.f.__iter__()
        
        file_mock = FileMock(f, 'excel_input.xlsx')
        df = parse_data(file_mock)
        print("Parsed Columns:", df.columns.tolist())
        
        # Override DB_PATH to a test db
        import data_processor
        data_processor.DB_PATH = 'debug_test.db'
        
        # Init and Save
        init_db()
        save_to_db(df)
        
        # Verify
        engine = create_engine('sqlite:///debug_test.db')
        with engine.connect() as conn:
            subjects = conn.execute(text("SELECT DISTINCT subject FROM scores")).fetchall()
            print("\nSubjects in DB:")
            for s in subjects:
                print(s[0])
                
            count = conn.execute(text("SELECT count(*) FROM scores")).fetchone()[0]
            print(f"\nTotal score entries: {count}")
            
except Exception as e:
    print(e)
