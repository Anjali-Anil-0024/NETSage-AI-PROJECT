# rule_checker.py

# ---------------------------------------------------------
# NETSage-AI Rule Checker
# ---------------------------------------------------------


def check_diagnosis(diagnosis):
    """
    Checks an AI-generated diagnosis
    using predefined networking rules.
    """

    root_cause = str(
        diagnosis.get("root_cause", "")
    ).strip()

    concept = str(
        diagnosis.get("concept", "")
    ).strip().lower()

    severity = str(
        diagnosis.get("severity", "")
    ).strip().lower()

    evidence = str(
        diagnosis.get("evidence", "")
    ).strip()


    issues = []


    # -----------------------------------------------------
    # Rule 1 - Root cause must exist
    # -----------------------------------------------------

    if not root_cause:
        issues.append(
            "Root cause is missing."
        )


    # -----------------------------------------------------
    # Rule 2 - Evidence must exist
    # -----------------------------------------------------

    if not evidence:
        issues.append(
            "Diagnostic evidence is missing."
        )


    # -----------------------------------------------------
    # Rule 3 - DNS
    # -----------------------------------------------------

    if "dns" in concept:

        if "dns" not in root_cause.lower():

            issues.append(
                "DNS concept does not match the root cause."
            )


    # -----------------------------------------------------
    # Rule 4 - DHCP
    # -----------------------------------------------------

    if "dhcp" in concept:

        if "dhcp" not in root_cause.lower():

            issues.append(
                "DHCP concept does not match the root cause."
            )


    # -----------------------------------------------------
    # Rule 5 - VLAN
    # -----------------------------------------------------

    if "vlan" in concept:

        if "vlan" not in root_cause.lower():

            issues.append(
                "VLAN concept does not match the root cause."
            )


    # -----------------------------------------------------
    # Rule 6 - Routing
    # -----------------------------------------------------

    if (
        "routing" in concept
        or "route" in concept
    ):

        keywords = [
            "route",
            "routing",
            "gateway"
        ]

        if not any(
            word in root_cause.lower()
            for word in keywords
        ):

            issues.append(
                "Routing concept does not match the root cause."
            )


    # -----------------------------------------------------
    # Rule 7 - OSPF
    # -----------------------------------------------------

    if "ospf" in concept:

        if "ospf" not in root_cause.lower():

            issues.append(
                "OSPF concept does not match the root cause."
            )


    # -----------------------------------------------------
    # Rule 8 - ACL
    # -----------------------------------------------------

    if "acl" in concept:

        if "acl" not in root_cause.lower():

            issues.append(
                "ACL concept does not match the root cause."
            )


    # -----------------------------------------------------
    # Rule 9 - NAT
    # -----------------------------------------------------

    if "nat" in concept:

        if "nat" not in root_cause.lower():

            issues.append(
                "NAT concept does not match the root cause."
            )


    # -----------------------------------------------------
    # Rule 10 - Severity
    # -----------------------------------------------------

    valid_severity = [
        "low",
        "medium",
        "high",
        "critical"
    ]

    if severity not in valid_severity:

        issues.append(
            "Invalid severity level."
        )


    # -----------------------------------------------------
    # Final Result
    # -----------------------------------------------------

    if len(issues) == 0:

        return {
            "status": "VALID",

            "message":
                "Diagnosis passed all rule checks.",

            "issues": [],

            "corrected_diagnosis":
                root_cause
        }


    else:

        return {
            "status": "REVIEW",

            "message":
                "Diagnosis requires human review.",

            "issues": issues,

            "corrected_diagnosis":
                root_cause
                + " - Requires verification"
        }


# ---------------------------------------------------------
# Display Result
# ---------------------------------------------------------

def display_result(result):

    print("\n==============================================")

    print(" NETSage-AI RULE CHECKER")

    print("==============================================")

    print(
        "Status :",
        result["status"]
    )

    print(
        "Message :",
        result["message"]
    )


    if result["issues"]:

        print("\nDetected Issues:")

        for issue in result["issues"]:

            print(
                " -",
                issue
            )


    print(
        "\nCorrected Diagnosis :",
        result["corrected_diagnosis"]
    )

    print("==============================================")


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    test_diagnosis = {

        "root_cause":
            "DNS configuration issue",

        "concept":
            "DNS",

        "severity":
            "High",

        "evidence":
            "DNS resolution failed"
    }


    result = check_diagnosis(
        test_diagnosis
    )

    display_result(
        result
    )
