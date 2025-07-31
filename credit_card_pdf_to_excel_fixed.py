import pdfplumber
import pandas as pd
import re
from datetime import datetime
import os
from pathlib import Path

def load_merchant_categories_from_csv(csv_file_path):
    """
    Load merchant-to-category mappings from CSV file with robust encoding handling.
    Expected columns: Merchant, Category Note, Category Note Add1
    """
    print(f"Attempting to load CSV from: {csv_file_path}")
    
    # Check if file exists
    if not Path(csv_file_path).exists():
        print(f"Error: CSV file does not exist: {csv_file_path}")
        return {}, {}
    
    # Try multiple approaches to read the CSV
    encodings_to_try = ['cp1252', 'latin-1', 'iso-8859-1', 'utf-8-sig', 'utf-8']
    
    for encoding in encodings_to_try:
        try:
            print(f"Trying encoding: {encoding}")
            df = pd.read_csv(csv_file_path, encoding=encoding)
            print(f"Successfully loaded CSV with {encoding} encoding")
            
            # Initialize dictionaries
            MERCHANT_NOTES = {}
            MERCHANT_NOTES_ADD1 = {}
            
            # Process the data
            for _, row in df.iterrows():
                merchant = str(row['Merchant']).strip()
                if merchant and merchant != 'nan':
                    # Handle Category Note
                    category_note = str(row['Category Note']).strip() if pd.notna(row['Category Note']) else ''
                    if category_note and category_note != 'nan':
                        MERCHANT_NOTES[merchant] = category_note
                    
                    # Handle Category Note Add1
                    category_note_add1 = str(row['Category Note Add1']).strip() if pd.notna(row['Category Note Add1']) else ''
                    if category_note_add1 and category_note_add1 != 'nan':
                        MERCHANT_NOTES_ADD1[merchant] = category_note_add1
            
            print(f"Loaded {len(MERCHANT_NOTES)} Category Note entries")
            print(f"Loaded {len(MERCHANT_NOTES_ADD1)} Category Note Add1 entries")
            return MERCHANT_NOTES, MERCHANT_NOTES_ADD1
            
        except UnicodeDecodeError as e:
            print(f"Encoding {encoding} failed: {e}")
            continue
        except Exception as e:
            print(f"Error with {encoding}: {e}")
            continue
    
    # If all pandas methods fail, try manual parsing
    print("Pandas methods failed, trying manual parsing...")
    try:
        with open(csv_file_path, 'rb') as f:
            content = f.read()
        
        for encoding in encodings_to_try:
            try:
                decoded_content = content.decode(encoding)
                print(f"Manual decoding successful with {encoding}")
                
                lines = decoded_content.split('\n')
                if len(lines) < 2:
                    print("CSV file appears to be empty or has no data rows")
                    return {}, {}
                
                # Skip header and process data
                MERCHANT_NOTES = {}
                MERCHANT_NOTES_ADD1 = {}
                
                for line in lines[1:]:  # Skip header
                    if line.strip():
                        parts = line.split(',')
                        if len(parts) >= 3:
                            merchant = parts[0].strip().strip('"')
                            category_note = parts[1].strip().strip('"')
                            category_note_add1 = parts[2].strip().strip('"')
                            
                            if merchant and merchant.lower() != 'merchant':
                                MERCHANT_NOTES[merchant] = category_note
                                MERCHANT_NOTES_ADD1[merchant] = category_note_add1
                
                print(f"Manually loaded {len(MERCHANT_NOTES)} merchants")
                return MERCHANT_NOTES, MERCHANT_NOTES_ADD1
                
            except UnicodeDecodeError:
                continue
    
    except Exception as e:
        print(f"Manual parsing also failed: {e}")
    
    print("All methods failed to load CSV file")
    return {}, {}

def extract_transactions_from_pdf(pdf_path):
    """Extract transaction data from PDF credit card statement"""
    transactions = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    lines = text.split('\n')
                    print(f"Page {page_num + 1}: Processing {len(lines)} lines")
                    
                    for line_num, line in enumerate(lines):
                        # Try multiple transaction patterns for different statement formats
                        patterns = [
                            # Pattern 1: MM/DD Merchant Amount
                            r'(\d{2}/\d{2})\s+([A-Za-z0-9\s\-\.]+?)\s+([\d,]+\.\d{2})',
                            # Pattern 2: MM/DD/YY Merchant Amount (Citi format)
                            r'(\d{2}/\d{2}/\d{2})\s+([A-Za-z0-9\s\-\.]+?)\s+([\d,]+\.\d{2})',
                            # Pattern 3: MM/DD Merchant Amount (with possible extra spaces)
                            r'(\d{2}/\d{2})\s+([A-Za-z0-9\s\-\.]+?)\s+([\d,]+\.[\d]{2})',
                            # Pattern 4: Date at start, amount at end
                            r'^(\d{2}/\d{2})\s+(.+?)\s+([\d,]+\.[\d]{2})$',
                            # Pattern 5: Citi specific format
                            r'(\d{2}/\d{2}/\d{2})\s+(.+?)\s+([\d,]+\.[\d]{2})'
                        ]
                        
                        for pattern in patterns:
                            transaction_match = re.search(pattern, line)
                            if transaction_match:
                                date_str = transaction_match.group(1)
                                merchant = transaction_match.group(2).strip()
                                amount = transaction_match.group(3)
                                
                                try:
                                    # Parse date (handle both MM/DD and MM/DD/YY formats)
                                    if len(date_str.split('/')) == 2:
                                        date_obj = datetime.strptime(date_str, '%m/%d')
                                        date_obj = date_obj.replace(year=datetime.now().year)
                                    else:
                                        date_obj = datetime.strptime(date_str, '%m/%d/%y')
                                        if date_obj.year < 2000:
                                            date_obj = date_obj.replace(year=date_obj.year + 2000)
                                    
                                    transaction = {
                                        'Date': date_obj.strftime('%m/%d/%Y'),
                                        'Merchant': merchant,
                                        'Amount': float(amount.replace(',', '')),
                                        'Category Note': '',
                                        'Category Note Add1': ''
                                    }
                                    
                                    transactions.append(transaction)
                                    print(f"Found transaction: {date_str} {merchant} {amount}")
                                    break  # Found a match, don't try other patterns
                                except ValueError:
                                    continue
                    
                    # Show sample text if no transactions found
                    if not transactions and page_num == 0:
                        print("No transactions found. Sample text from first page:")
                        for i, line in enumerate(lines[:10]):
                            if line.strip():
                                print(f"  Line {i+1}: {line}")
                    
                    # Show more sample text from other pages if still no transactions
                    elif not transactions and page_num < 3:
                        print(f"Sample text from page {page_num + 1}:")
                        for i, line in enumerate(lines[:5]):
                            if line.strip():
                                print(f"  Line {i+1}: {line}")
                    
                    # If we're on page 2 or 3 and still no transactions, show more lines
                    elif not transactions and (page_num == 1 or page_num == 2):
                        print(f"More sample text from page {page_num + 1}:")
                        for i, line in enumerate(lines[5:15]):  # Show lines 6-15
                            if line.strip():
                                print(f"  Line {i+6}: {line}")
    
    except Exception as e:
        print(f"Error processing PDF {pdf_path}: {e}")
    
    return transactions

def categorize_transactions(transactions, MERCHANT_NOTES, MERCHANT_NOTES_ADD1):
    """Add category notes based on merchant mappings"""
    for transaction in transactions:
        merchant = transaction['Merchant']
        amount = transaction['Amount']
        
        # Check if amount is negative (credit)
        if amount < 0:
            transaction['Category Note'] = 'Credit'
        else:
            # Apply Category Note from dictionary
            if merchant in MERCHANT_NOTES:
                transaction['Category Note'] = MERCHANT_NOTES[merchant]
            
            # Apply Category Note Add1 from dictionary
            if merchant in MERCHANT_NOTES_ADD1:
                transaction['Category Note Add1'] = MERCHANT_NOTES_ADD1[merchant]
            
            # Fallback categorization
            if not transaction['Category Note']:
                if any(keyword in merchant.lower() for keyword in ['gas', 'fuel', 'shell', 'exxon']):
                    transaction['Category Note'] = 'Gas'
                elif any(keyword in merchant.lower() for keyword in ['grocery', 'food', 'restaurant']):
                    transaction['Category Note'] = 'Food'

def export_to_excel(transactions, output_path):
    """Export transactions to Excel file"""
    try:
        df = pd.DataFrame(transactions)
        
        # Reorder columns to match FileMaker Pro import format
        column_order = ['Date', 'Merchant', 'Amount', 'Category Note', 'Category Note Add1']
        df = df[column_order]
        
        # Export to Excel
        df.to_excel(output_path, index=False, sheet_name='Transactions')
        print(f"Exported {len(transactions)} transactions to {output_path}")
        print(f"Columns exported: {column_order}")
        
    except Exception as e:
        print(f"Error exporting to Excel: {e}")

def main():
    print("=== Credit Card PDF to Excel Processor (Fixed Version) ===")
    print("1. Process PDF statements with existing categories")
    print("2. Exit")
    
    choice = input("\nSelect option (1-2): ").strip()
    
    if choice == "1":
        process_pdf_statements()
    elif choice == "2":
        print("Goodbye!")
        return
    else:
        print("Invalid choice. Please run the script again.")

def process_pdf_statements():
    """Main function to process PDF statements"""
    try:
        print("\n=== PDF Processing Configuration ===")
        
        # Get PDF directory
        pdf_directory = input("Enter the directory path containing PDF statements: ").strip()
        if not pdf_directory:
            print("Error: PDF directory path is required.")
            return
        
        # Get CSV file path
        csv_file_path = input("Enter the path to the merchant categories CSV file: ").strip()
        if not csv_file_path:
            print("Error: CSV file path is required.")
            return
        
        # Get output directory
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
        
        # Create output directory
        Path(output_directory).mkdir(parents=True, exist_ok=True)
        print(f"Output directory: {output_directory}")
        
        # Load merchant categories
        print("\nLoading merchant categories from CSV...")
        MERCHANT_NOTES, MERCHANT_NOTES_ADD1 = load_merchant_categories_from_csv(csv_file_path)
        
        if not MERCHANT_NOTES and not MERCHANT_NOTES_ADD1:
            print("No merchant categories loaded. Please check your CSV file.")
            input("Press Enter to continue...")
            return
        
        # Find PDF files
        pdf_files = list(Path(pdf_directory).glob("*.pdf"))
        print(f"Found {len(pdf_files)} PDF files in directory")
        
        if not pdf_files:
            print("No PDF files found in the specified directory.")
            print(f"Directory searched: {pdf_directory}")
            input("Press Enter to continue...")
            return
        
        # Process each PDF
        files_processed = 0
        for pdf_file in pdf_files:
            print(f"\nProcessing: {pdf_file.name}")
            
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
            
            # Create a sample Excel file to show the format
            sample_transactions = [
                {
                    'Date': '12/01/2024',
                    'Merchant': 'SAMPLE MERCHANT',
                    'Amount': 100.00,
                    'Category Note': 'Sample Category',
                    'Category Note Add1': 'Sample Note'
                }
            ]
            
            sample_output_path = Path(output_directory) / "sample_format.xlsx"
            export_to_excel(sample_transactions, sample_output_path)
            print(f"\nCreated sample Excel file: {sample_output_path}")
            print("This shows the expected format for FileMaker import.")
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

if __name__ == "__main__":
    print("Starting Credit Card PDF to Excel Processor (Fixed Version)...")
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