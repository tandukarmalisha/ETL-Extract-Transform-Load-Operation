import os

def generate_final_report(total_inserted: int, user_error_report: list, duration: float):
    """Prints a summary to the console and saves errors to a file."""
    
    # 1. Console Output
    print("\n" + "="*40)
    print("          FINAL IMPORT REPORT")
    print("="*40)
    print(f"✅ Success: {total_inserted} rows saved.")
    print(f"❌ Failed:  {len(user_error_report)} rows skipped.")
    print(f"⏱️ Time Taken: {duration:.2f} seconds")
    print("="*40)
    
    # 2. Handle Error File Generation
    if user_error_report:
        error_filename = "user_error_report.txt"
        try:
            with open(error_filename, "w") as f:
                f.write("THE FOLLOWING ROWS HAD ERRORS AND WERE NOT IMPORTED:\n")
                f.write("="*50 + "\n")
                for err in user_error_report:
                    f.write(f"{err}\n")
            
            print(f"\n⚠️  Detailed errors saved to: {error_filename}")
            print("Please check this file to fix your Excel data.")
        except Exception as e:
            print(f"❌ Could not save error report file: {e}")
            
        # def generate_final_report(total_inserted, user_error_report, duration):
    # ... existing report code ...
       
            
    print("="*40)