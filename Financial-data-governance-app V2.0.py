import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

from ingestion import load_data
from validation import validate_data
from classification import classify_fields
from audit import log_change
from reporting import generate_report

def run_governance_pipeline(file_path, output_console):
    try:
        output_console.insert(tk.END, "📥 Loading data...\n")
        df = load_data(file_path)

        output_console.insert(tk.END, "✅ Validating data...\n")
        issues = validate_data(df)

        output_console.insert(tk.END, "🏷️ Classifying fields...\n")
        metadata = classify_fields(df)

        output_console.insert(tk.END, "📝 Logging changes...\n")
        log_change("Data loaded and validated.")

        output_console.insert(tk.END, "📊 Generating report...\n")
        generate_report(df, issues, metadata)

        output_console.insert(tk.END, "🎉 Governance check complete.\n")
    except Exception as e:
        output_console.insert(tk.END, f"❌ Error: {str(e)}\n")
        messagebox.showerror("Pipeline Error", str(e))

def browse_file(entry):
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def create_gui():
    window = tk.Tk()
    window.title("📊 Data Governance Pipeline")
    window.geometry("600x400")

    # File selection section
    tk.Label(window, text="CSV File Path:").pack(pady=5)
    file_entry = tk.Entry(window, width=60)
    file_entry.pack(padx=10)
    tk.Button(window, text="📂 Browse", command=lambda: browse_file(file_entry)).pack(pady=5)

    # Console output
    output_console = scrolledtext.ScrolledText(window, width=70, height=15)
    output_console.pack(pady=10)

    # Run pipeline button
    tk.Button(
        window,
        text="🚀 Run Governance Pipeline",
        command=lambda: run_governance_pipeline(file_entry.get(), output_console),
        bg="lightgreen"
    ).pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    create_gui()
