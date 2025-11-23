# Finance Tracker (CLI)

Small command-line app to log and analyze your personal finances.   Transactions are stored in a simple CSV file so you keep full control over your data.

- ✅ Add income and expenses
- 🔎 Filter transactions by date range
- 📊 Get totals (income, expenses, and net)
- 📈 Optionally plot daily trends using Matplotlib

---

## Tech Stack

- **Python 3.12**
- **pandas** – CSV I/O, filtering, summaries
- **matplotlib** – plotting daily trends
- **Standard library** – `datetime`, `csv`, etc.

---

# (Recommended) Create & activate a virtual environment

Windows PowerShell

python -m venv .venv

.\.venv\Scripts\Activate.ps1


macOS / Linux

python -m venv .venv

source .venv/bin/activate

Install the libraries directly:

pip install pandas matplotlib

How to Run

From the project root:

cd Finance-Tracker

.\.venv\Scripts\Activate.ps1   # if using the venv

python main.py

This starts the CLI and you’ll see a simple text menu (exact wording may differ), e.g.:

Finance Tracker

1) Add transaction
   
3) View summary
   
5) Filter by date range
   
7) Plot daily trends
  
9) Exit
