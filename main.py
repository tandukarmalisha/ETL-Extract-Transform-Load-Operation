import pandas as pd
import logging
import sys
import os
from logic import format_name, clean_mobile, split_email_data
from database import get_db_engine  # Updated import
from reporting import generate_final_report

# ... (Logging setup stays exactly the same) ...
# Logging Setup

logging.basicConfig(
level=logging.INFO,
format='%(asctime)s - %(levelname)s - %(message)s',
handlers=[
logging.FileHandler("import_log.log"),
logging.StreamHandler(sys.stdout)
]
)
def start_import():
    # 1. Path Handling (Stay the same)
    if len(sys.argv) < 2:
        logging.error("Usage: python3 etl.py <filename.xlsx>")
        return

    file_name = sys.argv[1]
    full_path = os.path.expanduser(file_name)

    if not os.path.exists(full_path):
        logging.error(f"File not found: {full_path}")
        return

    user_error_report = []
    cleaned_rows = [] # We store dictionaries here to build a new DF

    try:
        # 2. Load File
        df = pd.read_excel(full_path)
        df.columns = [str(c).strip().lower() for c in df.columns]
        logging.info(f"File loaded. Processing {len(df)} rows...")

        # 3. Processing Loop (Logic Layer)
        for index, row in df.iterrows():
            row_no = index + 2
            try:
                name_final = format_name(row.get('name'))
                if name_final is None: continue 

                addr_final = str(row.get('address', '')).strip().upper()
                mob_final = clean_mobile(row.get('mobile number'))
                user_name, domain_name = split_email_data(row.get('email'))

                # Collect into a list of dictionaries
                cleaned_rows.append({
                    "name": name_final,
                    "address": addr_final,
                    "mobile_number": mob_final,
                    "email": user_name,
                    "domain": domain_name
                })

            except Exception as e:
                user_error_report.append(f"Row {row_no}: {str(e)}")

        # 4. Use the Built-in Pandas method
        total_inserted = 0
        if cleaned_rows:
            # Create a new DataFrame from our cleaned data
            df_final = pd.DataFrame(cleaned_rows)
            
            engine = get_db_engine()
            
            # This is the built-in function that performs the query automatically
            df_final.to_sql(
                name='etl_import', 
                con=engine, 
                if_exists='append', 
                index=False, 
                chunksize=1000 # This is the built-in batching!
            )
            total_inserted = len(df_final)

        # 5. Final Report
        generate_final_report(total_inserted, user_error_report)

    except Exception as main_err:
        logging.critical(f"Critical System Failure: {main_err}")

if __name__ == "__main__":
    start_import()