import pandas as pd
import logging
import sys
import os
import time
from logic import format_name, clean_mobile, split_email_data
from database import get_db_engine
from reporting import generate_final_report

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
    start_time = time.time()  # Record start
    duration = 0.0            # Initialize default value
    total_inserted = 0
    user_error_report = []

    # 1. Path Handling
    if len(sys.argv) < 2:
        logging.error("Usage: python3 main.py <filename.xlsx>")
        return

    file_name = sys.argv[1]
    full_path = os.path.expanduser(file_name)

    if not os.path.exists(full_path):
        logging.error(f"File not found: {full_path}")
        return

    try:
        # 2. Load File
        df = pd.read_excel(full_path)
        df.columns = [str(c).strip().lower() for c in df.columns]
        logging.info(f"File loaded. Processing {len(df)} rows...")

        # 3. Processing Loop
        cleaned_rows = []
        for index, row in df.iterrows():
            row_no = index + 2
            try:
                name_final = format_name(row.get('name'))
                if name_final is None: continue 

                addr_final = str(row.get('address', '')).strip().upper()
                mob_final = clean_mobile(row.get('mobile number'))
                user_name, domain_name = split_email_data(row.get('email'))

                cleaned_rows.append({
                    "name": name_final,
                    "address": addr_final,
                    "mobile_number": mob_final,
                    "email": user_name,
                    "domain": domain_name
                })
            except Exception as e:
                user_error_report.append(f"Row {row_no}: {str(e)}")

        # 4. Built-in Pandas method (to_sql)
        if cleaned_rows:
            df_final = pd.DataFrame(cleaned_rows)
            engine = get_db_engine()
            df_final.to_sql(
                name='etl_import', 
                con=engine, 
                if_exists='append', 
                index=False, 
                chunksize=1000 
            )
            total_inserted = len(df_final)

        # 5. Calculate Duration BEFORE generating report
        end_time = time.time()
        duration = end_time - start_time
        logging.info(f"⏱️ Process finished in {duration:.2f} seconds")

        # 6. Final Report
        generate_final_report(total_inserted, user_error_report, duration)

    except Exception as main_err:
        logging.critical(f"Critical System Failure: {main_err}")

if __name__ == "__main__":
    start_import()