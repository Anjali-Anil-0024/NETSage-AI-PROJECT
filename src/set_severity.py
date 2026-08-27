import csv
import os

# ---------------------------------------------------------
# NETSage-AI - Set Severity for all 30 Cases
# ---------------------------------------------------------

FILE_PATH = os.path.join("data", "cases.csv")


# ---------------------------------------------------------
# Severity for each case
# ---------------------------------------------------------

SEVERITY = {
    "C001": "Medium",
    "C002": "High",
    "C003": "High",
    "C004": "High",
    "C005": "High",
    "C006": "High",
    "C007": "Medium",
    "C008": "High",
    "C009": "High",
    "C010": "High",
    "C011": "Medium",
    "C012": "High",
    "C013": "Critical",
    "C014": "High",
    "C015": "High",
    "C016": "High",
    "C017": "High",
    "C018": "High",
    "C019": "Medium",
    "C020": "Medium",
    "C021": "High",
    "C022": "Medium",
    "C023": "Medium",
    "C024": "High",
    "C025": "High",
    "C026": "High",
    "C027": "High",
    "C028": "Medium",
    "C029": "High",
    "C030": "Medium"
}


# ---------------------------------------------------------
# Check CSV file
# ---------------------------------------------------------

if not os.path.exists(FILE_PATH):
    print("ERROR: data/cases.csv not found.")
    exit()


# ---------------------------------------------------------
# Read CSV
# ---------------------------------------------------------

with open(
    FILE_PATH,
    "r",
    encoding="utf-8-sig",
    newline=""
) as file:

    reader = csv.DictReader(file)

    rows = list(reader)

    fieldnames = reader.fieldnames


# ---------------------------------------------------------
# Check Case ID column
# ---------------------------------------------------------

if not fieldnames or "case_id" not in fieldnames:

    print("ERROR: 'case_id' column not found in cases.csv.")
    print("Available columns:", fieldnames)
    exit()


# ---------------------------------------------------------
# Create severity column if missing
# ---------------------------------------------------------

if "severity" not in fieldnames:

    fieldnames.append("severity")

    print("Severity column was missing.")
    print("Creating 'severity' column...")


# ---------------------------------------------------------
# Update severity
# ---------------------------------------------------------

updated = 0

for row in rows:

    case_id = row.get("case_id", "").strip()

    if case_id in SEVERITY:

        row["severity"] = SEVERITY[case_id]

        updated += 1

    else:

        row["severity"] = "Medium"


# ---------------------------------------------------------
# Save updated CSV
# ---------------------------------------------------------

with open(
    FILE_PATH,
    "w",
    encoding="utf-8",
    newline=""
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(rows)


# ---------------------------------------------------------
# Display result
# ---------------------------------------------------------

print()
print("==============================================")
print(" NETSage-AI SEVERITY UPDATE")
print("==============================================")

print("Cases updated :", updated)
print("Total cases :", len(rows))

print("----------------------------------------------")

for case_id, severity in SEVERITY.items():

    print(f"{case_id} -> {severity}")

print("----------------------------------------------")

if updated == 30:

    print("SUCCESS: All 30 cases updated.")

else:

    print(
        f"WARNING: Only {updated} cases were matched."
    )

print("Severity column saved to cases.csv.")
print("==============================================")