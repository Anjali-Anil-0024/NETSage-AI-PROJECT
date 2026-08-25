import csv
import os
import sys
import subprocess

from rule_checker import check_diagnosis, display_result


# ---------------------------------------------------------
# Load all troubleshooting cases
# ---------------------------------------------------------

def load_cases():

    cases = []

    file_path = os.path.join(
        "data",
        "cases.csv"
    )

    with open(
        file_path,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            clean_row = {}

            for key, value in row.items():

                if key is not None:

                    clean_key = key.strip()

                    clean_value = (
                        value.strip()
                        if value
                        else ""
                    )

                    clean_row[clean_key] = clean_value

            cases.append(clean_row)

    return cases


# ---------------------------------------------------------
# Generate evidence-based diagnosis
# ---------------------------------------------------------

def generate_diagnosis(case):

    case_id = case.get(
        "case_id",
        "Not specified"
    )

    symptom = case.get(
        "symptom",
        "Not specified"
    )

    evidence = case.get(
        "show_output",
        "Not specified"
    )

    expected_fault = case.get(
        "expected_fault",
        "Not specified"
    )

    osi_layer = case.get(
        "osi_layer",
        "Not specified"
    )

    concept = case.get(
        "concept",
        "Not specified"
    )

    severity = case.get(
        "severity",
        "Not specified"
    )


    # -----------------------------------------------------
    # Confidence
    # -----------------------------------------------------

    if evidence and evidence != "Not specified":

        confidence = "High"

    elif symptom and symptom != "Not specified":

        confidence = "Medium"

    else:

        confidence = "Low"


    # -----------------------------------------------------
    # Verification command
    # -----------------------------------------------------

    next_command = get_verification_command(
        concept,
        evidence
    )


    # -----------------------------------------------------
    # Suggested fix
    # -----------------------------------------------------

    suggested_fix = get_suggested_fix(
        expected_fault,
        concept
    )


    diagnosis = {

        "case_id": case_id,

        "symptom": symptom,

        "evidence": evidence,

        "root_cause": expected_fault,

        "confidence": confidence,

        "osi_layer": osi_layer,

        "concept": concept,

        "severity": severity,

        "next_command": next_command,

        "suggested_fix": suggested_fix
    }


    return diagnosis


# ---------------------------------------------------------
# Verification command
# ---------------------------------------------------------

def get_verification_command(
    concept,
    evidence
):

    concept_lower = concept.lower()


    if "vlan" in concept_lower:

        return "show vlan brief"


    elif "dhcp" in concept_lower:

        return "show ip dhcp binding"


    elif "dns" in concept_lower:

        return "nslookup <domain>"


    elif (
        "routing" in concept_lower
        or "route" in concept_lower
    ):

        return "show ip route"


    elif "ospf" in concept_lower:

        return "show ip ospf neighbor"


    elif "acl" in concept_lower:

        return "show access-lists"


    elif "nat" in concept_lower:

        return "show ip nat translations"


    elif "interface" in concept_lower:

        return "show interfaces"


    elif (
        "wireless" in concept_lower
        or "wifi" in concept_lower
    ):

        return "show interfaces"


    elif "switch" in concept_lower:

        return "show interfaces status"


    else:

        return "show running-config"


# ---------------------------------------------------------
# Suggested fix
# ---------------------------------------------------------

def get_suggested_fix(
    expected_fault,
    concept
):

    fault = expected_fault.lower()

    concept_lower = concept.lower()


    if "vlan missing" in fault:

        return (
            "Verify VLAN configuration and "
            "create/restore the required VLAN."
        )


    elif "dhcp" in concept_lower:

        return (
            "Verify DHCP pool, excluded "
            "addresses and client configuration."
        )


    elif "dns" in concept_lower:

        return (
            "Verify DNS server address and "
            "DNS service configuration."
        )


    elif (
        "route" in concept_lower
        or "routing" in concept_lower
    ):

        return (
            "Verify routing table and correct "
            "the missing or incorrect route."
        )


    elif "ospf" in concept_lower:

        return (
            "Verify OSPF network statements, "
            "area configuration and neighbor status."
        )


    elif "acl" in concept_lower:

        return (
            "Verify ACL rules, order and "
            "interface/direction where the ACL is applied."
        )


    elif "nat" in concept_lower:

        return (
            "Verify NAT configuration and "
            "inside/outside interface settings."
        )


    elif "interface" in concept_lower:

        return (
            "Verify interface status, IP configuration "
            "and physical connectivity."
        )


    else:

        return (
            "Verify the evidence and apply "
            "the appropriate configuration correction."
        )


# ---------------------------------------------------------
# Display AI Diagnosis
# ---------------------------------------------------------

def display_diagnosis(diagnosis):

    print("\n==============================================")

    print(
        " NETSage-AI Diagnosis"
    )

    print("==============================================")


    print(
        "Case ID :",
        diagnosis["case_id"]
    )

    print(
        "Symptom :",
        diagnosis["symptom"]
    )

    print(
        "Evidence :",
        diagnosis["evidence"]
    )


    print("----------------------------------------------")


    print(
        "Root Cause :",
        diagnosis["root_cause"]
    )

    print(
        "Confidence :",
        diagnosis["confidence"]
    )

    print(
        "OSI Layer :",
        diagnosis["osi_layer"]
    )

    print(
        "Concept :",
        diagnosis["concept"]
    )

    print(
        "Severity :",
        diagnosis["severity"]
    )


    print("----------------------------------------------")


    print(
        "Next Command :",
        diagnosis["next_command"]
    )

    print(
        "Suggested Fix :",
        diagnosis["suggested_fix"]
    )


    print("----------------------------------------------")


    print(
        "Human Review : REQUIRED"
    )

    print("==============================================")


# ---------------------------------------------------------
# Rule Checker
# ---------------------------------------------------------

def run_rule_checker(diagnosis):

    print("\n")
    print("==============================================")
    print(" Running Rule Checker...")
    print("==============================================")


    result = check_diagnosis(
        diagnosis
    )


    display_result(
        result
    )


    # -----------------------------------------------------
    # Update diagnosis with corrected result
    # -----------------------------------------------------

    diagnosis["corrected_diagnosis"] = (
        result["corrected_diagnosis"]
    )

    diagnosis["rule_status"] = (
        result["status"]
    )


    return diagnosis


# ---------------------------------------------------------
# Start Human Review
# ---------------------------------------------------------

def start_human_review(diagnosis):

    review_file = os.path.join(
        "src",
        "review.py"
    )


    if not os.path.exists(review_file):

        print(
            "\nWarning: src/review.py not found."
        )

        return


    print(
        "\nStarting Human Review..."
    )


    # -----------------------------------------------------
    # Send corrected diagnosis to human review
    # -----------------------------------------------------

    subprocess.run([
        sys.executable,
        review_file,
        diagnosis["case_id"],
        diagnosis["corrected_diagnosis"]
    ])


# ---------------------------------------------------------
# Select Case
# ---------------------------------------------------------

def select_case(cases):

    print("\n==============================================")

    print(
        " NETSage-AI Case Selection"
    )

    print("==============================================")


    print(
        "Total Cases:",
        len(cases)
    )


    for i, case in enumerate(
        cases,
        start=1
    ):

        print(
            f"{i}. "
            f"{case.get('case_id', 'Unknown')} - "
            f"{case.get('symptom', 'No symptom')}"
        )


    print(
        "=============================================="
    )


    while True:

        choice = input(
            f"Enter case number "
            f"(1-{len(cases)}) "
            f"or 0 to exit: "
        ).strip()


        if choice == "0":

            return None


        if choice.isdigit():

            number = int(choice)


            if (
                1 <= number
                <= len(cases)
            ):

                return cases[
                    number - 1
                ]


        print(
            "Invalid choice. Please try again."
        )


# ---------------------------------------------------------
# Main Program
# ---------------------------------------------------------

if __name__ == "__main__":

    try:

        cases = load_cases()


        print("\n==============================================")

        print(
            " NETSage-AI"
        )

        print(
            " AI-Assisted Network Troubleshooting"
        )

        print("==============================================")


        print(
            "Total Cases:",
            len(cases)
        )


        if len(cases) == 0:

            print(
                "No cases found in data/cases.csv"
            )

            sys.exit()


        while True:

            # -------------------------------------------------
            # Select case
            # -------------------------------------------------

            selected_case = select_case(
                cases
            )


            if selected_case is None:

                print(
                    "\nExiting NETSage-AI..."
                )

                break


            # -------------------------------------------------
            # Generate AI diagnosis
            # -------------------------------------------------

            diagnosis = generate_diagnosis(
                selected_case
            )


            # -------------------------------------------------
            # Display diagnosis
            # -------------------------------------------------

            display_diagnosis(
                diagnosis
            )


            # -------------------------------------------------
            # Run Rule Checker
            # -------------------------------------------------

            diagnosis = run_rule_checker(
                diagnosis
            )


            # -------------------------------------------------
            # Show final diagnosis
            # -------------------------------------------------

            print("\n==============================================")

            print(
                " FINAL DIAGNOSIS"
            )

            print("==============================================")


            print(
                "Original AI Diagnosis :",
                diagnosis["root_cause"]
            )

            print(
                "Rule Checker Status :",
                diagnosis["rule_status"]
            )

            print(
                "Corrected Diagnosis :",
                diagnosis["corrected_diagnosis"]
            )

            print("==============================================")


            # -------------------------------------------------
            # Human Review
            # -------------------------------------------------

            review_choice = input(
                "\nStart Human Review? (y/n): "
            ).strip().lower()


            if review_choice == "y":

                start_human_review(
                    diagnosis
                )


            # -------------------------------------------------
            # Another case
            # -------------------------------------------------

            again = input(
                "\nDiagnose another case? (y/n): "
            ).strip().lower()


            if again != "y":

                print(
                    "\nThank you for using NETSage-AI."
                )

                break


    except FileNotFoundError:

        print(
            "Error: data/cases.csv file not found."
        )


    except Exception as error:

        print(
            "Error:",
            error
        )
