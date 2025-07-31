import pdfplumber
import pandas as pd
import re
from datetime import datetime
import os
from pathlib import Path

def load_merchant_categories_from_csv(csv_file_path):
    """
    Load merchant-to-category mappings from CSV file and merge with existing dictionaries.
    Expected columns: Merchant, Category Note, Category Note Add1
    """
    try:
        # Try different encodings to handle Excel-created CSV files
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        df = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv(csv_file_path, encoding=encoding)
                print(f"Successfully loaded CSV with {encoding} encoding")
                break
            except UnicodeDecodeError:
                continue
        
        if df is None:
            print("Could not read CSV file with any supported encoding")
            return {}, {}
        
        # Initialize with existing dictionaries
        MERCHANT_NOTES = {
            # Add your existing merchant notes here
            # Example: 'WALMART': 'Retail',
            # Example: 'SHELL': 'Transportation',
        }
        
        MERCHANT_NOTES_ADD1 = {
            # Add your existing merchant notes add1 here
            # Example: 'WALMART': 'Additional Note 1',
            # Example: 'SHELL': 'Additional Note 2',
        }
        
        # Update with CSV data
        for _, row in df.iterrows():
            merchant = row['Merchant'].strip()
            if merchant:
                # Update Category Note
                if pd.notna(row['Category Note']) and str(row['Category Note']).strip():
                    MERCHANT_NOTES[merchant] = str(row['Category Note']).strip()
                
                # Update Category Note Add1
                if pd.notna(row['Category Note Add1']) and str(row['Category Note Add1']).strip():
                    MERCHANT_NOTES_ADD1[merchant] = str(row['Category Note Add1']).strip()
        
        print(f"Updated merchant mappings from CSV:")
        print(f"- Category Note entries: {len(MERCHANT_NOTES)}")
        print(f"- Category Note Add1 entries: {len(MERCHANT_NOTES_ADD1)}")
        
        return MERCHANT_NOTES, MERCHANT_NOTES_ADD1
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        print("Trying alternative method...")
        
        # Try reading as bytes and decoding manually
        try:
            with open(csv_file_path, 'rb') as f:
                content = f.read()
            
            # Try different encodings manually
            for encoding in ['cp1252', 'latin-1', 'iso-8859-1', 'utf-8-sig']:
                try:
                    decoded_content = content.decode(encoding)
                    print(f"Successfully decoded with {encoding}")
                    
                    # Parse manually
                    lines = decoded_content.split('\n')
                    headers = lines[0].strip().split(',')
                    
                    MERCHANT_NOTES = {}
                    MERCHANT_NOTES_ADD1 = {}
                    
                    for line in lines[1:]:
                        if line.strip():
                            parts = line.split(',')
                            if len(parts) >= 3:
                                merchant = parts[0].strip().strip('"')
                                category_note = parts[1].strip().strip('"')
                                category_note_add1 = parts[2].strip().strip('"')
                                
                                if merchant:
                                    MERCHANT_NOTES[merchant] = category_note
                                    MERCHANT_NOTES_ADD1[merchant] = category_note_add1
                    
                    print(f"Manually loaded {len(MERCHANT_NOTES)} merchants")
                    return MERCHANT_NOTES, MERCHANT_NOTES_ADD1
                    
                except UnicodeDecodeError:
                    continue
            
            print("Could not decode file with any encoding")
            return {}, {}
            
        except Exception as e2:
            print(f"Alternative method also failed: {e2}")
            return {}, {}

def save_merchant_categories_to_csv(MERCHANT_NOTES, MERCHANT_NOTES_ADD1, csv_file_path):
    """
    Save current merchant categories to CSV file for backup or editing
    """
    try:
        # Get all unique merchants
        all_merchants = set(MERCHANT_NOTES.keys()) | set(MERCHANT_NOTES_ADD1.keys())
        
        # Create data for CSV
        data = []
        for merchant in sorted(all_merchants):
            data.append({
                'Merchant': merchant,
                'Category Note': MERCHANT_NOTES.get(merchant, ''),
                'Category Note Add1': MERCHANT_NOTES_ADD1.get(merchant, '')
            })
        
        # Create DataFrame and save to CSV
        df = pd.DataFrame(data)
        df.to_csv(csv_file_path, index=False)
        print(f"Saved {len(data)} merchant categories to {csv_file_path}")
        
    except Exception as e:
        print(f"Error saving CSV file: {e}")

def update_merchant_categories_interactive(MERCHANT_NOTES, MERCHANT_NOTES_ADD1):
    """
    Interactive function to update merchant categories
    """
    print("\n=== Merchant Category Update Tool ===")
    print("Commands:")
    print("  1. Add/update merchant")
    print("  2. Remove merchant")
    print("  3. Show all current categories")
    print("  4. Save current categories to CSV")
    print("  5. Load categories from CSV")
    print("  6. Exit update tool")
    
    while True:
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == '6':
            break
        elif choice == '3':
            print("\nCurrent Categories:")
            if not MERCHANT_NOTES and not MERCHANT_NOTES_ADD1:
                print("  No categories loaded yet.")
            else:
                for merchant in sorted(MERCHANT_NOTES.keys() | MERCHANT_NOTES_ADD1.keys()):
                    note = MERCHANT_NOTES.get(merchant, '')
                    note_add1 = MERCHANT_NOTES_ADD1.get(merchant, '')
                    print(f"  {merchant}: {note} | {note_add1}")
        elif choice == '1':
            print("\nAdd/Update Merchant:")
            merchant = input("Enter merchant name: ").strip()
            if merchant:
                category_note = input("Enter category note: ").strip()
                category_note_add1 = input("Enter category note add1: ").strip()
                MERCHANT_NOTES[merchant] = category_note
                MERCHANT_NOTES_ADD1[merchant] = category_note_add1
                print(f"Updated: {merchant}")
            else:
                print("Merchant name cannot be empty.")
        elif choice == '2':
            print("\nRemove Merchant:")
            merchant = input("Enter merchant name to remove: ").strip()
            if merchant in MERCHANT_NOTES:
                del MERCHANT_NOTES[merchant]
            if merchant in MERCHANT_NOTES_ADD1:
                del MERCHANT_NOTES_ADD1[merchant]
            print(f"Removed: {merchant}")
        elif choice == '4':
            print("\nSave Categories:")
            filename = input("Enter CSV filename to save: ").strip()
            if filename:
                save_merchant_categories_to_csv(MERCHANT_NOTES, MERCHANT_NOTES_ADD1, filename)
        elif choice == '5':
            print("\nLoad Categories from CSV:")
            filename = input("Enter CSV filename to load: ").strip()
            if filename:
                try:
                    new_notes, new_notes_add1 = load_merchant_categories_from_csv(filename)
                    MERCHANT_NOTES.update(new_notes)
                    MERCHANT_NOTES_ADD1.update(new_notes_add1)
                    print(f"Loaded categories from {filename}")
                except Exception as e:
                    print(f"Error loading CSV: {e}")
        else:
            print("Invalid choice. Please enter 1-6.")
    
    return MERCHANT_NOTES, MERCHANT_NOTES_ADD1

def extract_transactions_from_pdf(pdf_path):
    """Extract transaction data from PDF credit card statement"""
    transactions = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                # Split text into lines and process each line
                lines = text.split('\n')
                print(f"Processing {len(lines)} lines from PDF")
                
                for i, line in enumerate(lines):
                    # Look for transaction patterns
                    # This pattern may need adjustment based on your specific PDF format
                    transaction_match = re.search(r'(\d{2}/\d{2})\s+([A-Za-z0-9\s\-\.]+?)\s+([\d,]+\.\d{2})', line)
                    if transaction_match:
                        date_str = transaction_match.group(1)
                        merchant = transaction_match.group(2).strip()
                        amount = transaction_match.group(3)
                        
                        try:
                            # Parse date
                            date_obj = datetime.strptime(date_str, '%m/%d')
                            # Assume current year for the date
                            date_obj = date_obj.replace(year=datetime.now().year)
                            
                            # Create transaction with category columns
                            transaction = {
                                'Date': date_obj.strftime('%m/%d/%Y'),
                                'Merchant': merchant,
                                'Amount': float(amount.replace(',', '')),
                                'Category Note': '',
                                'Category Note Add1': ''
                            }
                            
                            transactions.append(transaction)
                            print(f"Found transaction: {date_str} {merchant} {amount}")
                        except ValueError:
                            continue
                
                # If no transactions found, show a sample of the text
                if not transactions:
                    print("No transactions found. Sample of PDF text:")
                    for i, line in enumerate(lines[:10]):  # Show first 10 lines
                        if line.strip():
                            print(f"Line {i+1}: {line}")
    
    return transactions

def categorize_transactions(transactions, MERCHANT_NOTES, MERCHANT_NOTES_ADD1):
    """Add category notes based on merchant mappings"""
    for transaction in transactions:
        merchant = transaction['Merchant']
        amount = transaction['Amount']
        
        # Check if amount is negative (credit) and set Category Note to "Credit"
        if amount < 0:
            transaction['Category Note'] = 'Credit'
        else:
            # Apply Category Note from dictionary only for positive amounts
            if merchant in MERCHANT_NOTES:
                transaction['Category Note'] = MERCHANT_NOTES[merchant]
            
            # Apply Category Note Add1 from dictionary
            if merchant in MERCHANT_NOTES_ADD1:
                transaction['Category Note Add1'] = MERCHANT_NOTES_ADD1[merchant]
            
            # You can add more categorization logic here for automatic categorization
            # For example, based on keywords in merchant names
            if not transaction['Category Note']:  # Only if not already set by dictionary
                if any(keyword in merchant.lower() for keyword in ['gas', 'fuel', 'shell', 'exxon']):
                    transaction['Category Note'] = 'Gas'
                elif any(keyword in merchant.lower() for keyword in ['grocery', 'food', 'restaurant']):
                    transaction['Category Note'] = 'Food'
                # Add more categories as needed

def export_to_excel(transactions, output_path):
    """Export transactions to Excel file"""
    df = pd.DataFrame(transactions)
    
    # Reorder columns to match FileMaker Pro import format
    column_order = ['Date', 'Merchant', 'Amount', 'Category Note', 'Category Note Add1']
    df = df[column_order]
    
    # Export to Excel
    df.to_excel(output_path, index=False, sheet_name='Transactions')
    print(f"Exported {len(transactions)} transactions to {output_path}")
    print(f"Columns exported: {column_order}")

def main():
    try:
        print("=== Credit Card PDF to Excel Processor ===")
        print("1. Process PDF statements with existing categories")
        print("2. Update merchant categories")
        print("3. Exit")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == "1":
            process_pdf_statements()
        elif choice == "2":
            update_categories_mode()
        elif choice == "3":
            print("Goodbye!")
            return
        else:
            print("Invalid choice. Please run the script again.")
    except KeyboardInterrupt:
        print("\n\nScript interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        input("Press Enter to exit...")

def process_pdf_statements():
    """Main function to process PDF statements"""
    try:
        # Configuration
        print("\n=== PDF Processing Configuration ===")
        pdf_directory = input("Enter the directory path containing PDF statements: ").strip()
        if not pdf_directory:
            print("Error: PDF directory path is required.")
            return
            
        csv_file_path = input("Enter the path to the merchant categories CSV file: ").strip()
        if not csv_file_path:
            print("Error: CSV file path is required.")
            return
            
        output_directory = input("Enter the output directory for Excel files: ").strip()
        if not output_directory:
            print("Error: Output directory path is required.")
            return
    
        # Verify paths exist
        if not Path(pdf_directory).exists():
            print(f"Error: PDF directory does not exist: {pdf_directory}")
            return
            
        if not Path(csv_file_path).exists():
            print(f"Error: CSV file does not exist: {csv_file_path}")
            return
    
        # Create output directory if it doesn't exist
        Path(output_directory).mkdir(parents=True, exist_ok=True)
        print(f"Output directory: {output_directory}")
        
        # Load merchant categories from CSV and update dictionaries
        print("Loading merchant categories from CSV...")
        MERCHANT_NOTES, MERCHANT_NOTES_ADD1 = load_merchant_categories_from_csv(csv_file_path)
        
        if not MERCHANT_NOTES and not MERCHANT_NOTES_ADD1:
            print("No merchant categories loaded. Please check your CSV file.")
            return
        
        # Process each PDF file in the directory
        pdf_files = list(Path(pdf_directory).glob("*.pdf"))
        print(f"Found {len(pdf_files)} PDF files in directory")
        
        if not pdf_files:
            print("No PDF files found in the specified directory.")
            print(f"Directory searched: {pdf_directory}")
            return
        
        files_processed = 0
        for pdf_file in pdf_files:
            print(f"\nProcessing: {pdf_file.name}")
            
            # Extract transactions
            transactions = extract_transactions_from_pdf(pdf_file)
            
            if not transactions:
                print(f"No transactions found in {pdf_file.name}")
                continue
            
            print(f"Found {len(transactions)} transactions")
            
            # Categorize transactions
            categorize_transactions(transactions, MERCHANT_NOTES, MERCHANT_NOTES_ADD1)
            
            # Create output filename
            output_filename = f"{pdf_file.stem}_transactions.xlsx"
            output_path = Path(output_directory) / output_filename
            
            # Export to Excel
            export_to_excel(transactions, output_path)
            
            print(f"Successfully processed {len(transactions)} transactions from {pdf_file.name}")
            print(f"Excel file created: {output_path}")
            files_processed += 1
        
        if files_processed == 0:
            print("\nNo files were processed. Check that:")
            print("1. PDF files exist in the specified directory")
            print("2. PDF files contain recognizable transaction patterns")
            print("3. CSV file has the correct format (Merchant, Category Note, Category Note Add1)")
        else:
            print(f"\nSuccessfully processed {files_processed} PDF files.")
        
        print("\nPress Enter to return to main menu...")
        input()
            
    except KeyboardInterrupt:
        print("\n\nProcessing interrupted by user.")
        input("Press Enter to continue...")
    except Exception as e:
        print(f"\nAn error occurred during processing: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to continue...")

def update_categories_mode():
    """Interactive mode for updating merchant categories"""
    print("\n=== Category Update Mode ===")
    
    # Initialize empty dictionaries
    MERCHANT_NOTES = {}
    MERCHANT_NOTES_ADD1 = {}
    
    # Option to load existing CSV
    load_existing = input("Load existing categories from CSV? (y/n): ").strip().lower()
    if load_existing == 'y':
        csv_file_path = input("Enter CSV file path: ").strip()
        MERCHANT_NOTES, MERCHANT_NOTES_ADD1 = load_merchant_categories_from_csv(csv_file_path)
    
    # Interactive update
    MERCHANT_NOTES, MERCHANT_NOTES_ADD1 = update_merchant_categories_interactive(MERCHANT_NOTES, MERCHANT_NOTES_ADD1)
    
    # Option to save updated categories
    save_updated = input("\nSave updated categories to CSV? (y/n): ").strip().lower()
    if save_updated == 'y':
        csv_file_path = input("Enter CSV file path to save: ").strip()
        save_merchant_categories_to_csv(MERCHANT_NOTES, MERCHANT_NOTES_ADD1, csv_file_path)

if __name__ == "__main__":
    print("Starting Credit Card PDF to Excel Processor...")
    print("Make sure you have the required packages installed:")
    print("- pdfplumber")
    print("- pandas")
    print("- openpyxl (for Excel export)")
    print()
    
    try:
        main()
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        input("Press Enter to exit...") 