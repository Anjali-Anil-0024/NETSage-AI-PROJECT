import csv
import os
import sys


LOG_FILE = "logs/review_log.csv"


def save_review(case_id, ai_diagnosis, decision, correction=""):
    file_exists = os.path.exists(LOG_FILE)

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "case_id",
                "ai_diagnosis",
                "human_decision",
                "human_correction",
                "reviewer"
            ])

        writer.writerow([
            case_id,
            ai_diagnosis,
            decision,
            correction,
            "Human Reviewer"
        ])


def review_case(case_id, ai_diagnosis):

    print("\n===== NETSage-AI Human Review =====")
    print("Case ID:", case_id)
    print("AI Diagnosis:", ai_diagnosis)

    print("\nChoose decision:")
    print("1. Accept")
    print("2. Edit")
    print("3. Reject")

    choice = input("Enter choice: ")

    if choice == "1":
        decision = "Accepted"
        correction = ""

    elif choice == "2":
        decision = "Edited"
        correction = input("Enter corrected diagnosis: ")

    elif choice == "3":
        decision = "Rejected"
        correction = input("Reason for rejection: ")

    else:
        print("Invalid choice.")
        return

    save_review(
        case_id,
        ai_diagnosis,
        decision,
        correction
    )

    print("\nReview saved successfully!")
    print("Decision:", decision)


if __name__ == "__main__":

    if len(sys.argv) >= 3:
        case_id = sys.argv[1]
        ai_diagnosis = sys.argv[2]

        review_case(case_id, ai_diagnosis)

    else:
        print("Error: Case ID and AI Diagnosis were not provided.")
