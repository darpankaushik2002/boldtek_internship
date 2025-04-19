🧾 ParseMate:
-----------------------------------------------------
 AI-Powered Invoice Parser with Gemini in Colab
ParseMate is a Google Colab-based project that automates the extraction of structured data from invoices in PDF and image formats. It uses Google's Gemini 1.5 Flash model to intelligently parse invoice metadata, line items, and totals into structured JSON and saves them to CSV.

🚀 Features
----------------------------------------------------------------------
🔍 Extracts invoice metadata, item details, and totals using LLM prompts.

🧠 Uses Gemini 1.5 Flash via the Google Generative AI API.

📄 Supports both image (.jpg, .jpeg, .png) and PDF invoice formats.

🧹 Cleans and validates JSON outputs from the model.

📤 Saves all parsed line-item details to a downloadable CSV.

💡 Modular prompt structure for flexible and extendable parsing logic.

🛠️ Setup & Requirements
------------------------------------------------------------------------
This project runs entirely in Google Colab and requires:

A Google API Key for Gemini models

File upload permissions for invoices

Internet access to install dependencies

📦 Dependencies (auto-installed in Colab)
-----------------------------------------------

pip install -q -U google-generativeai pymupdf
🔑 API Key Configuration
Before running the main code, store your Google API key securely using:


from google.colab import userdata
GOOGLE_API_KEY = userdata.get('GOOGLE_API_KEY')
📁 How It Works
-------------------------------------------------------------------
Upload image or PDF invoices via Colab.

Parse them using Gemini 1.5 Flash with three structured prompts:

Invoice Metadata

Item Line Details

Totals & Taxes

Clean and validate JSON responses.

Save results into a CSV file (parsed_invoice_items.csv) for download.

📸 Sample Prompts Used
Metadata Extraction

json
Copy
Edit
{
  "invoice_number": "",
  "invoice_date": "",
  "seller_name": "",
  "buyer_name": ""
}
Line Item Details

json
Copy
Edit
{
  "items": [
    {"description": "", "quantity": 0, "price": 0.0, "total": 0.0}
  ]
}
Totals and Tax

json
Copy
Edit
{
  "subtotal": 0.0,
  "tax": 0.0,
  "total_amount": 0.0,
  "payment_method": ""
}
📊 Output
----------------------------------------------------------------
Each parsed invoice outputs a structured JSON and adds all line items into a final downloadable CSV (parsed_invoice_items.csv) with metadata and totals included for each item.

📂 Example Output (CSV)

description	quantity	price	total	invoice_number	...
Widget A	2	10.0	20.0	INV-123	...
Widget B	1	5.0	5.0	INV-123	...
✅ Use Cases
---------------------------------------------------------------
Financial automation

Invoice auditing

Expense tracking

Receipt digitization

🧠 Tech Stack
-------------------------------------------------------------
Google Generative AI (Gemini 1.5 Flash)

Python

Google Colab

PyMuPDF

Pandas

📌 Notes
-------------------------------------------------------


Supports multi-prompt parsing for better accuracy.

Easily extendable to handle more fields and formats.

