import os
import mysql.connector
import gradio as gr
import fitz  # PyMuPDF
import pandas as pd
import json
import mimetypes
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv
import tempfile

# ------------------ CONFIG ------------------
load_dotenv()  # Load .env file
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # Retrieve API key from .env file
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

genai.configure(api_key=GOOGLE_API_KEY)
MODEL_CONFIG = {
    "temperature": 0.2,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]
gemini_1_5_flash = genai.GenerativeModel(
    model_name="models/gemini-1.5-flash",
    generation_config=MODEL_CONFIG,
    safety_settings=safety_settings
)

# ------------------ PROMPTS ------------------
METADATA_PROMPT = """
You are an invoice parser. Extract general metadata using flexible key names. Look for common variations like:
invoice_number / i_number / inv_no
invoice_date / inv_date
seller / vendor / seller_name
buyer / client / buyer_name

Respond in JSON with flexible keys:
Example output:
{
    "invoice_number": "12345",  # Could also be i_number or inv_no
    "invoice_date": "2025-04-22",  # Could also be inv_date
    "seller_name": "Seller Name",  # Could also be vendor or seller
    "buyer_name": "Buyer Name"  # Could also be client or buyer
}
"""

ITEMS_PROMPT = """
Extract all item line details as JSON with flexible keys. Look for variations like:
description / item_name / line_description
quantity / qty
price / unit_price
total / line_total / item_total

Respond in JSON format:
{
    "items": [
        {"description": "item 1", "quantity": 1, "price": 10.0, "total": 10.0},
        {"description": "item 2", "quantity": 2, "price": 20.0, "total": 40.0}
    ]
}
"""

TOTALS_PROMPT = """
Extract totals and tax values as JSON. Look for variations like:
subtotal / total_before_tax
tax / tax_amount
total_amount / total_due
payment_method / payment_type / method_of_payment

Respond in JSON format:
{
    "subtotal": 50.0,
    "tax": 5.0,
    "total_amount": 55.0,
    "payment_method": "Credit Card"
}
"""

SQL_PROMPT = """
You are a helpful SQL query generator. Your task is to convert natural language questions into SQL queries that can be executed against a MySQL database with the following schema:

CREATE TABLE invoices (
    description TEXT,
    quantity INTEGER,
    price REAL,
    total REAL,
    invoice_number VARCHAR(255),
    invoice_date VARCHAR(255),
    source_file VARCHAR(255),
    subtotal REAL,
    tax REAL,
    total_amount REAL,
    payment_method VARCHAR(255)
);

Only generate the SQL query. Do not provide any explanations or additional text.

For example:
User: Show me all invoice numbers.
SQL: SELECT DISTINCT invoice_number FROM invoices;

User: What are the descriptions of items with a quantity greater than 1?
SQL: SELECT description FROM invoices WHERE quantity > 1;

User: Find the total amount for invoice number 'INV-123'.
SQL: SELECT total_amount FROM invoices WHERE invoice_number = 'INV-123';

User: How many unique source files are there?
SQL: SELECT COUNT(DISTINCT source_file) FROM invoices;

User: What is the average price of items?
SQL: SELECT AVG(price) FROM invoices;

Now, convert the following natural language question into a SQL query:
{natural_language_query}
"""

# ------------------ HELPERS ------------------
def image_format(image_path):
    mime_type, _ = mimetypes.guess_type(image_path)
    return [{"mime_type": mime_type, "data": Path(image_path).read_bytes()}]

def gemini_image_parse(image_path, prompt):
    image_info = image_format(image_path)
    result = gemini_1_5_flash.generate_content([prompt, image_info[0]])
    return result.text

def gemini_text_to_sql(natural_language_query):
    prompt = SQL_PROMPT.format(natural_language_query=natural_language_query)
    response = gemini_1_5_flash.generate_content([prompt])
    raw_sql = response.text.strip()
    # Remove ```sql and ``` if present
    if raw_sql.startswith("```sql"):
        raw_sql = raw_sql[len("```sql"):].strip()
    if raw_sql.endswith("```"):
        raw_sql = raw_sql[:-len("```")].strip()
    return raw_sql.strip()

def clean_and_parse_json(raw_output):
    try:
        cleaned = raw_output.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[len("```json"):].lstrip()
        if cleaned.endswith("```"):
            cleaned = cleaned[:-len("```")].rstrip()
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}, Raw Output: '{raw_output}'")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred: {e}, Raw Output: '{raw_output}'")
        return {}

def gemini_pdf_parse_with_vision(pdf_path, prompt):
    try:
        pdf = fitz.open(pdf_path)
        full_output = ""
        for page in pdf:
            img_path = f"temp_page_{page.number}.png"
            try:
                pix = page.get_pixmap(dpi=300)
                pix.save(img_path)
                full_output += gemini_image_parse(img_path, prompt) + "\n"
            except Exception as e:
                print(f"Error processing page {page.number} of {pdf_path}: {e}")
            finally:
                if os.path.exists(img_path):
                    os.remove(img_path)
        return full_output
    except Exception as e:
        print(f"Error opening or processing PDF {pdf_path}: {e}")
        return ""

def parse_single_invoice(file):
    file_path = file.name
    parsed_data = {}

    # Extract metadata
    result_metadata = gemini_pdf_parse_with_vision(file_path, METADATA_PROMPT)
    metadata = clean_and_parse_json(result_metadata)
    standardized_data = {
        "invoice_number": metadata.get("invoice_number") or metadata.get("i_number") or metadata.get("inv_no"),
        "invoice_date": metadata.get("invoice_date") or metadata.get("inv_date"),
        "seller_name": metadata.get("seller_name") or metadata.get("vendor") or metadata.get("seller"),
        "buyer_name": metadata.get("buyer_name") or metadata.get("client") or metadata.get("buyer")
    }
    parsed_data.update(standardized_data)

    # Extract item details
    result_items = gemini_pdf_parse_with_vision(file_path, ITEMS_PROMPT)
    item_details = clean_and_parse_json(result_items)
    if item_details and "items" in item_details:
        normalized_items = []
        for item in item_details["items"]:
            normalized_item = {
                "description": item.get("description") or item.get("item_name") or item.get("line_description"),
                "quantity": item.get("quantity") or item.get("qty"),
                "price": item.get("price") or item.get("unit_price"),
                "total": item.get("total") or item.get("line_total") or item.get("item_total")
            }
            normalized_items.append(normalized_item)
        parsed_data["items"] = normalized_items

    # Extract totals and tax
    result_totals = gemini_pdf_parse_with_vision(file_path, TOTALS_PROMPT)
    totals_and_tax = clean_and_parse_json(result_totals)
    if totals_and_tax:
        parsed_data["subtotal"] = totals_and_tax.get("subtotal") or totals_and_tax.get("total_before_tax")
        parsed_data["tax"] = totals_and_tax.get("tax") or totals_and_tax.get("tax_amount")
        parsed_data["total_amount"] = totals_and_tax.get("total_amount") or totals_and_tax.get("total_due")
        parsed_data["payment_method"] = totals_and_tax.get("payment_method") or totals_and_tax.get("payment_type") or totals_and_tax.get("method_of_payment")

    # Finalize and store
    file_name = os.path.basename(file_path)
    if "items" in parsed_data:
        for item in parsed_data["items"]:
            item["invoice_number"] = parsed_data.get("invoice_number")
            item["invoice_date"] = parsed_data.get("invoice_date")
            item["source_file"] = file_name
            item["subtotal"] = parsed_data.get("subtotal")
            item["tax"] = parsed_data.get("tax")
            item["total_amount"] = parsed_data.get("total_amount")
            item["payment_method"] = parsed_data.get("payment_method")
        save_items_to_csv(parsed_data["items"])
        store_in_database(parsed_data["items"])

    return json.dumps(parsed_data, indent=2)

def save_items_to_csv(items):
    df = pd.DataFrame(items)
    df.to_csv("parsed_items.csv", mode='a', index=False, header=not os.path.exists("parsed_items.csv"))

def get_db_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

def store_in_database(items):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO invoices (
            description, quantity, price, total, invoice_number,
            invoice_date, source_file, subtotal, tax, total_amount, payment_method
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        for item in items:
            cursor.execute(insert_query, (
                item.get("description"),
                item.get("quantity"),
                item.get("price"),
                item.get("total"),
                item.get("invoice_number"),
                item.get("invoice_date"),
                item.get("source_file"),
                item.get("subtotal"),
                item.get("tax"),
                item.get("total_amount"),
                item.get("payment_method"),
            ))
        conn.commit()
    except mysql.connector.Error as e:
        print(f"MySQL Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def execute_query(query):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=columns)
        return df
    except mysql.connector.Error as e:
        print(f"MySQL Error: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

# ------------------ GRADIO INTERFACE ------------------
def parse_multiple_invoices(files):
    if not files:
        return "No files uploaded."
    results = []
    for file in files:
        result = parse_single_invoice(file)
        results.append(json.loads(result))
    return json.dumps(results, indent=2)

def natural_language_query_to_sql_and_execute(nl_query):
    sql = gemini_text_to_sql(nl_query)
    df = execute_query(sql)
    if df is None or df.empty:
        return f"Query executed: {sql}\n\nNo results found or error occurred."
    return df

with gr.Blocks() as demo:
    gr.Markdown("# Invoice Parser & Query App with Gemini 1.5 Flash + MySQL")

    with gr.Tab("Parse Invoices"):
        file_input = gr.File(file_types=[".pdf", ".png", ".jpg", ".jpeg"], file_count="multiple", label="Upload invoice PDFs or images")
        parse_button = gr.Button("Parse and Store")
        parse_output = gr.Textbox(label="Parsed Invoice Data (JSON)", lines=20, interactive=False)
        csv_download = gr.File(label="Download Parsed Items CSV")

        def parse_and_prepare_csv(files):
            output_json = parse_multiple_invoices(files)
            if os.path.exists("parsed_items.csv"):
                csv_path = "parsed_items.csv"
            else:
                csv_path = None
            return output_json, csv_path

        parse_button.click(parse_and_prepare_csv, inputs=file_input, outputs=[parse_output, csv_download])

    with gr.Tab("Natural Language SQL Query"):
        query_input = gr.Textbox(label="Enter your natural language query about invoices")
        query_button = gr.Button("Generate SQL & Execute")
        query_output = gr.Dataframe(headers=None, interactive=False)

        def query_and_display(nl_query):
            df = natural_language_query_to_sql_and_execute(nl_query)
            if isinstance(df, pd.DataFrame):
                return df
            else:
                return pd.DataFrame([[df]], columns=["Error"])

        query_button.click(query_and_display, inputs=query_input, outputs=query_output)

if __name__ == "__main__":
    demo.launch()
