import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import os
import time

from ingestion import load_data
from validation import validate_data
from classification import classify_fields
from audit import log_change
from reporting import generate_report

def run_governance_pipeline(file_path, output_console, progress, run_button):
    try:
        start_time = time.time()
        output_console.insert(tk.END, f"📥 Loading data from: {file_path}\n")
        progress['value'] = 10
        output_console.update()

        df = load_data(file_path)

        output_console.insert(tk.END, "✅ Validating data...\n")
        progress['value'] = 30
        output_console.update()
        issues = validate_data(df)

        output_console.insert(tk.END, "🏷️ Classifying fields...\n")
        progress['value'] = 50
        output_console.update()
        metadata = classify_fields(df)

        output_console.insert(tk.END, "📝 Logging changes...\n")
        progress['value'] = 70
        output_console.update()
        log_change("Data loaded and validated.")

        output_console.insert(tk.END, "📊 Generating report...\n")
        progress['value'] = 90
        output_console.update()
        generate_report(df, issues, metadata)

        elapsed = round(time.time() - start_time, 2)
        output_console.insert(tk.END, f"🎉 Governance check complete in {elapsed}s.\n")
        progress['value'] = 100
    except Exception as e:
        output_console.insert(tk.END, f"❌ Error: {str(e)}\n")
        messagebox.showerror("Pipeline Error", str(e))
    finally:
        run_button.config(state=tk.NORMAL)

def browse_file(entry, output_console):
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)

        file_size = os.path.getsize(file_path) / 1024
        output_console.insert(tk.END, f"📄 Selected file: {os.path.basename(file_path)} ({file_size:.2f} KB)\n")

def export_log(output_console):
    content = output_console.get("1.0", tk.END)
    if not content.strip():
        messagebox.showinfo("No Content", "Console is empty.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as f:
            f.write(content)
        messagebox.showinfo("Success", f"Console log saved to {file_path}")

def create_gui():
    window = tk.Tk()
    window.title("📊 Data Governance Pipeline")
    window.geometry("700x500")

    # File selection
    tk.Label(window, text="CSV File Path:").pack(pady=5)
    file_entry = tk.Entry(window, width=60)
    file_entry.pack(padx=10)
    output_console = scrolledtext.ScrolledText(window, width=85, height=15)
    tk.Button(window, text="📂 Browse", command=lambda: browse_file(file_entry, output_console)).pack(pady=5)

    # Console
    output_console.pack(pady=10)

    # Progress bar
    progress = ttk.Progressbar(window, length=500, mode='determinate')
    progress.pack(pady=5)

    # Buttons Frame
    btn_frame = tk.Frame(window)
    btn_frame.pack(pady=10)

    run_btn = tk.Button(
        btn_frame,
        text="🚀 Run Pipeline",
        bg="lightgreen",
        command=lambda: [run_btn.config(state=tk.DISABLED), run_governance_pipeline(file_entry.get(), output_console, progress, run_btn)]
    )
    run_btn.grid(row=0, column=0, padx=10)

    tk.Button(btn_frame, text="🧹 Clear Console", command=lambda: output_console.delete("1.0", tk.END)).grid(row=0, column=1, padx=10)

    tk.Button(btn_frame, text="💾 Export Log", command=lambda: export_log(output_console)).grid(row=0, column=2, padx=10)

    window.mainloop()

if __name__ == "__main__":
    create_gui()
