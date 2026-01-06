import psycopg2
from psycopg2 import extras  # Required for batch optimization
import pandas as pd
import re
import sys
import logging
import os
from dotenv import load_dotenv
from typing import List, Tuple, Optional, Any

# 1. Logging Setup (Requirement: Logging technique)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("import_log.log"), # Technical log for developers
        logging.StreamHandler(sys.stdout)
    ]
)

load_dotenv()
DB_CONFIG = {
  "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS")
}

# 2. Type Casted Function Definitions (Requirement: Type cast arguments)
def format_name(name_val: Any) -> Optional[str]:
    """Trims, applies initial capital, and limits to 250 characters."""
    name_str: str = str(name_val).strip() # Requirement: Trim all inputs
    if not name_str or name_str.lower() == 'nan':
        return None
    
    # Requirement: Initial Capital
    capitalized: str = " ".join([word.capitalize() for word in name_str.split()])
    return capitalized[:250]

def clean_mobile(mobile_val: Any) -> str:
    """Extracts last 10 digits from right to left."""
    digits: str = re.sub(r'\D', '', str(mobile_val))
    if len(digits) < 10:
        raise ValueError(f"Mobile number too short: {digits}")
    return digits[-10:]

# def clean_mobile(mobile_val: Any) -> str:
#     """Standardizes mobile number to exactly 10 digits."""
#     # 1. Strip all non-numeric characters
#     digits: str = re.sub(r'\D', '', str(mobile_val))
    
#     # 2. Strict validation: Must be exactly 10
#     if len(digits) != 10:
#         raise ValueError(f"Mobile number must be exactly 10 digits. Found: {len(digits)}")
    
#     return digits

def split_email_data(email_val: Any) -> Tuple[str, str]:
    """Splits email into username and domain."""
    email_clean: str = str(email_val).strip().lower() # Requirement: all small
    if "@" in email_clean:
        parts: List[str] = email_clean.split("@")
        return parts[0], parts[-1]
    return email_clean, "none"

def start_import():
    # 3. Passing Arguments (Requirement: Command line input)
    if len(sys.argv) < 2:
        logging.error("Missing file name. Usage: python3 etl.py <filename.xlsx>")
        return

    file_name: str = sys.argv[1]
    
    if not os.path.exists(os.path.expanduser(file_name)):
        logging.error(f"File not found: {file_name}")
        return

    # List to collect errors specifically for the end-user
    user_error_report: List[str] = []
    batch_data: List[Tuple[str, str, str, str, str]] = []

    try:
        df = pd.read_excel("~/Documents/info_10000.xlsx")  
        df.columns = [str(c).strip().lower() for c in df.columns]
        
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        logging.info(f"Connected to DB. Processing {len(df)} rows...")

        for index, row in df.iterrows():
            row_no: int = index + 2
            try:
                name_final = format_name(row.get('name'))
                
                # Requirement: Skip if name is empty
                if name_final is None:
                    continue 

                addr_final: str = str(row.get('address', '')).strip().upper() # Requirement: All Capital
                mob_final: str = clean_mobile(row.get('mobile number'))
                user_name, domain_name = split_email_data(row.get('email'))

                # Optimization: Add to batch list instead of executing immediately
                batch_data.append((name_final, addr_final, mob_final, user_name, domain_name))

            except Exception as e:
                # Requirement: Collect errors to show user at the end
                error_detail = f"Row {row_no}: {str(e)}"
                user_error_report.append(error_detail)
                logging.warning(f"Validation failed for {error_detail}")

        # 4. Optimized Batch Insert (Requirement: Optimize code)
        # if batch_data:
        #     insert_query: str = """
        #         INSERT INTO etl_import (name, address, mobile_number, email, domain)
        #         VALUES %s
        #     """
        #     extras.execute_values(cur, insert_query, batch_data)
        #     conn.commit()
        #     logging.info(f"Successfully inserted {len(batch_data)} rows.")

        # ... inside start_import ...
        
        batch_data: List[Tuple] = []
        batch_size = 1000  # Set your limit here
        total_inserted = 0

        for index, row in df.iterrows():
            row_no = index + 2
            try:
                # 1. Clean and Prepare data
                name_final = format_name(row.get('name'))
                if name_final is None: continue 

                addr_final = str(row.get('address', '')).strip().upper()
                mob_final = clean_mobile(row.get('mobile number'))
                user_name, domain_name = split_email_data(row.get('email'))

                # 2. Add to the current batch
                batch_data.append((name_final, addr_final, mob_final, user_name, domain_name))

                # 3. IF THE BATCH IS FULL (1000), SEND IT!
                if len(batch_data) >= batch_size:
                    extras.execute_values(cur, """
                        INSERT INTO etl_import (name, address, mobile_number, email, domain)
                        VALUES %s
                    """, batch_data)
                    conn.commit() # Save this chunk
                    
                    total_inserted += len(batch_data)
                    logging.info(f"Intermediate Batch: Inserted {total_inserted} rows...")
                    
                    batch_data = [] # Empty the "truck" for the next 1000 rows

            except Exception as e:
                user_error_report.append(f"Row {row_no}: {str(e)}")

        # 4. FINAL CLEANUP: Send any leftover rows (e.g., the last 400 rows)
        if batch_data:
            extras.execute_values(cur, """
                INSERT INTO etl_import (name, address, mobile_number, email, domain)
                VALUES %s
            """, batch_data)
            conn.commit()
            total_inserted += len(batch_data)

        logging.info(f"Done! Total successfully inserted: {total_inserted}")

        # 5. Display Result to User 
        print("\n" + "="*40)
        print("          FINAL IMPORT REPORT")
        print("="*40)
        print(f"✅ Success: {len(batch_data)} rows saved.")
        print(f"❌ Failed:  {len(user_error_report)} rows skipped.")
        
        if user_error_report:
            # Create the text file for the user
            error_filename = "user_error_report.txt"
            with open(error_filename, "w") as f:
                f.write("THE FOLLOWING ROWS HAD ERRORS AND WERE NOT IMPORTED:\n")
                f.write("="*50 + "\n")
                for err in user_error_report:
                    f.write(f"{err}\n")
            
            print(f"\n⚠️  Detailed errors saved to: user_error_report.txt")
            print("Please check this file to fix your Excel data.")
        
        print("="*40)
        # if user_error_report:
        #     print("\nDETAILED ERRORS:")
        #     for err in user_error_report:
        #         print(f"  - {err}")
        # print("="*40)

        cur.close()
        conn.close()

    except Exception as main_err:
        logging.critical(f"Critical System Failure: {main_err}")

if __name__ == "__main__":
    start_import()