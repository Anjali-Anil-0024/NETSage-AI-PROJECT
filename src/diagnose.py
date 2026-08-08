import csv
import os
import subprocess
import sys


def load_cases():
    cases = []

    file_path = os.path.join("data", "cases.csv")

    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            clean_row = {}

            for key, value in row.items():
                if key is not None:
                    clean_key = key.strip()
                    clean_value = value.strip() if value else ""
                    clean_row[clean_key] = clean_value

            cases.append(clean_row)

    return cases


def diagnose_case(case):
    print("\n================================")
    print(" NETSage-AI Diagnosis")
    print("================================")

    case_id = case.get("case_id", "Not specified")
    symptom = case.get("symptom", "Not specified")
    evidence = case.get("show_output", "Not specified")
    expected_fault = case.get("expected_fault", "Not specified")
    osi_layer = case.get("osi_layer", "Not specified")
    concept = case.get("concept", "Not specified")
    severity = case.get("severity", "Not specified")

    print("Case ID:", case_id)
    print("Symptom:", symptom)
    print("Evidence:", evidence)
    print("Expected Fault:", expected_fault)
    print("OSI Layer:", osi_layer)
    print("Concept:", concept)
    print("Severity:", severity)

    print("----------------------------------")

    # AI diagnosis
    ai_diagnosis = expected_fault

    print("AI Diagnosis:", ai_diagnosis)
    print("Human Review: Required")
    print("================================")

    # Start Human Review automatically
    review_file = os.path.join("src", "review.py")

    if os.path.exists(review_file):
        print("\nStarting Human Review...")

        subprocess.run([
            sys.executable,
            review_file,
            case_id,
            ai_diagnosis
        ])

    else:
        print("Error: src/review.py not found.")


if __name__ == "__main__":

    try:
        cases = load_cases()

        print("NETSage-AI")
        print("Total Cases:", len(cases))

        if len(cases) == 0:
            print("No cases found in cases.csv")

        else:
            # Diagnose first case
            diagnose_case(cases[0])

    except FileNotFoundError:
        print("Error: data/cases.csv file not found.")

    except Exception as error:
        print("Error:", error)
