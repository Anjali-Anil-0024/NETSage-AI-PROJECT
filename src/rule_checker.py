def check_diagnosis(case, diagnosis):
    expected_fault = case.get("expected_fault", "").lower()
    diagnosis_text = diagnosis.lower()

    if not expected_fault:
        return "INSUFFICIENT DATA"

    # Direct match
    if expected_fault in diagnosis_text:
        return "PASS"

    # Important keywords
    keywords = expected_fault.replace("-", " ").split()

    matched = 0

    for word in keywords:
        if len(word) > 2 and word in diagnosis_text:
            matched += 1

    # If most important words are present
    if len(keywords) > 0 and matched / len(keywords) >= 0.5:
        return "PASS"

    return "FAIL"


def review_case(case, diagnosis):
    result = check_diagnosis(case, diagnosis)

    print("\n==============================")
    print(" Rule Checker")
    print("==============================")
    print("Case ID:", case.get("case_id", "Unknown"))
    print("Expected Fault:", case.get("expected_fault", "Unknown"))
    print("Diagnosis:", diagnosis)
    print("Result:", result)
    print("Human Review: Required")
    print("==============================")


if __name__ == "__main__":

    sample_case = {
        "case_id": "C001",
        "expected_fault": "VLAN missing"
    }

    sample_diagnosis = "The VLAN is missing from the switch."

    review_case(sample_case, sample_diagnosis)

  