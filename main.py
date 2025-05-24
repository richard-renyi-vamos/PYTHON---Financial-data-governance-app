from ingestion import load_data
from validation import validate_data
from classification import classify_fields
from audit import log_change
from reporting import generate_report

def run_governance_pipeline(file_path):
    print("📥 Loading data...")
    df = load_data(file_path)

    print("✅ Validating data...")
    issues = validate_data(df)

    print("🏷️ Classifying fields...")
    metadata = classify_fields(df)

    print("📝 Logging changes...")
    log_change("Data loaded and validated.")

    print("📊 Generating report...")
    generate_report(df, issues, metadata)

    print("✅ Governance check complete.")

if __name__ == "__main__":
    run_governance_pipeline("financial_data.csv")
