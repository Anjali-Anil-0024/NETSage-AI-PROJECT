from flask import Flask, render_template_string
import csv
import os
from collections import Counter

app = Flask(__name__)

# ---------------------------------------------------------
# FILE PATHS
# ---------------------------------------------------------

CASES_FILE = "data/cases.csv"
REVIEW_FILE = "logs/review_log.csv"


# ---------------------------------------------------------
# LOAD CSV
# ---------------------------------------------------------

def load_csv(file_path):

    if not os.path.exists(file_path):
        return []

    try:
        with open(
            file_path,
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as file:

            reader = csv.DictReader(file)

            rows = []

            for row in reader:

                clean_row = {}

                for key, value in row.items():

                    if key is not None:
                        clean_key = key.strip()
                        clean_value = value.strip() if value else ""

                        clean_row[clean_key] = clean_value

                rows.append(clean_row)

            return rows

    except Exception as error:

        print("CSV Error:", error)

        return []


# ---------------------------------------------------------
# DASHBOARD DATA
# ---------------------------------------------------------

def get_dashboard_data():

    cases = load_csv(CASES_FILE)
    reviews = load_csv(REVIEW_FILE)

    # -----------------------------------------------------
    # Total cases
    # -----------------------------------------------------

    total_cases = len(cases)

    # -----------------------------------------------------
    # Severity distribution
    # -----------------------------------------------------

    severities = Counter()

    for case in cases:

        severity = case.get(
            "severity",
            "Unknown"
        ).strip()

        if not severity:
            severity = "Unknown"

        severities[severity] += 1

    # -----------------------------------------------------
    # Concept distribution
    # -----------------------------------------------------

    concepts = Counter()

    for case in cases:

        concept = case.get(
            "concept",
            "Unknown"
        ).strip()

        if not concept:
            concept = "Unknown"

        concepts[concept] += 1

    # -----------------------------------------------------
    # IMPORTANT:
    # Only latest review for each Case ID is counted.
    #
    # This prevents:
    #
    # C001 Accepted
    # C001 Edited
    # C001 Accepted
    #
    # from being counted as 3 reviewed cases.
    # -----------------------------------------------------

    latest_reviews = {}

    for review in reviews:

        case_id = review.get(
            "case_id",
            ""
        ).strip()

        if case_id:

            latest_reviews[case_id] = review

    # -----------------------------------------------------
    # Review decisions
    # -----------------------------------------------------

    decisions = Counter()

    for review in latest_reviews.values():

        decision = review.get(
            "human_decision",
            ""
        ).strip()

        if decision:
            decisions[decision] += 1

    accepted = decisions.get(
        "Accepted",
        0
    )

    edited = decisions.get(
        "Edited",
        0
    )

    rejected = decisions.get(
        "Rejected",
        0
    )

    # -----------------------------------------------------
    # Reviewed count
    # -----------------------------------------------------

    reviewed = (
        accepted
        + edited
        + rejected
    )

    # Never allow reviewed > total cases
    reviewed = min(
        reviewed,
        total_cases
    )

    # -----------------------------------------------------
    # AI Agreement
    # -----------------------------------------------------

    if reviewed > 0:

        agreement = (
            accepted / reviewed
        ) * 100

    else:

        agreement = 0

    # -----------------------------------------------------
    # Remaining cases
    # -----------------------------------------------------

    remaining = max(
        total_cases - reviewed,
        0
    )

    # -----------------------------------------------------
    # Return dashboard data
    # -----------------------------------------------------

    return {

        "total_cases": total_cases,

        "reviewed": reviewed,

        "remaining": remaining,

        "accepted": accepted,

        "edited": edited,

        "rejected": rejected,

        "agreement": round(
            agreement,
            1
        ),

        "severities": severities,

        "concepts": concepts
    }


# ---------------------------------------------------------
# HTML DASHBOARD
# ---------------------------------------------------------

HTML = """

<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>NETSage-AI Dashboard</title>


<style>

/* -------------------------------------------------------
   GLOBAL
------------------------------------------------------- */

* {
    box-sizing: border-box;
}

body {

    margin: 0;

    font-family:
        Arial,
        Helvetica,
        sans-serif;

    background:
        linear-gradient(
            135deg,
            #eef4ff,
            #f8fbff
        );

    color: #172033;
}


/* -------------------------------------------------------
   HEADER
------------------------------------------------------- */

.header {

    background:
        linear-gradient(
            135deg,
            #071b52,
            #0b5ed7
        );

    color: white;

    padding: 35px 7%;

    box-shadow:
        0 8px 25px
        rgba(0,0,0,0.15);
}

.header h1 {

    margin: 0;

    font-size: 42px;

    letter-spacing: 1px;
}

.header h1 span {

    color: #38bdf8;
}

.header p {

    margin-top: 10px;

    font-size: 17px;

    opacity: 0.9;
}


/* -------------------------------------------------------
   CONTAINER
------------------------------------------------------- */

.container {

    width: 90%;

    max-width: 1400px;

    margin: 30px auto;
}


/* -------------------------------------------------------
   SYSTEM STATUS
------------------------------------------------------- */

.status {

    background: white;

    border-radius: 18px;

    padding: 22px 28px;

    display: flex;

    justify-content: space-between;

    align-items: center;

    box-shadow:
        0 8px 25px
        rgba(31,45,61,0.08);

    margin-bottom: 25px;
}

.status h2 {

    margin: 0;

    font-size: 22px;
}

.status p {

    margin: 7px 0 0;

    color: #64748b;
}

.online {

    color: #16a34a;

    font-weight: bold;

    display: flex;

    align-items: center;

    gap: 8px;
}

.dot {

    width: 11px;

    height: 11px;

    background: #22c55e;

    border-radius: 50%;

    display: inline-block;
}


/* -------------------------------------------------------
   CARDS
------------------------------------------------------- */

.cards {

    display: grid;

    grid-template-columns:
        repeat(
            5,
            1fr
        );

    gap: 18px;

    margin-bottom: 25px;
}

.card {

    background: white;

    border-radius: 18px;

    padding: 25px;

    box-shadow:
        0 8px 25px
        rgba(31,45,61,0.08);

    transition:
        transform 0.2s,
        box-shadow 0.2s;
}

.card:hover {

    transform:
        translateY(-4px);

    box-shadow:
        0 14px 30px
        rgba(31,45,61,0.12);
}

.card-title {

    color: #64748b;

    font-size: 13px;

    font-weight: bold;

    text-transform:
        uppercase;

    letter-spacing: 1px;
}

.card-value {

    font-size: 35px;

    font-weight: bold;

    margin-top: 10px;
}

.blue {
    color: #2563eb;
}

.green {
    color: #16a34a;
}

.orange {
    color: #f59e0b;
}

.red {
    color: #dc2626;
}

.purple {
    color: #7c3aed;
}


/* -------------------------------------------------------
   GRID
------------------------------------------------------- */

.grid {

    display: grid;

    grid-template-columns:
        repeat(
            2,
            1fr
        );

    gap: 25px;
}


/* -------------------------------------------------------
   SECTION
------------------------------------------------------- */

.section {

    background: white;

    border-radius: 18px;

    padding: 25px;

    box-shadow:
        0 8px 25px
        rgba(31,45,61,0.08);
}

.section h2 {

    margin-top: 0;

    font-size: 21px;
}

.subtitle {

    color: #64748b;

    margin-top: -8px;

    margin-bottom: 20px;
}


/* -------------------------------------------------------
   TABLE
------------------------------------------------------- */

table {

    width: 100%;

    border-collapse:
        collapse;
}

th {

    text-align: left;

    padding: 13px;

    background: #f1f5f9;

    color: #334155;

    font-size: 13px;

    text-transform:
        uppercase;
}

td {

    padding: 13px;

    border-bottom:
        1px solid #e2e8f0;
}

tr:last-child td {

    border-bottom: none;
}


/* -------------------------------------------------------
   BADGES
------------------------------------------------------- */

.badge {

    display: inline-block;

    padding: 6px 12px;

    border-radius: 20px;

    font-size: 12px;

    font-weight: bold;
}

.badge-green {

    background: #dcfce7;

    color: #15803d;
}

.badge-orange {

    background: #fef3c7;

    color: #b45309;
}

.badge-red {

    background: #fee2e2;

    color: #b91c1c;
}


/* -------------------------------------------------------
   RESPONSIBLE AI
------------------------------------------------------- */

.responsible {

    margin-top: 25px;

    background:
        linear-gradient(
            135deg,
            #eff6ff,
            #f5f3ff
        );

    border: 1px solid #dbeafe;
}

.responsible p {

    color: #475569;

    line-height: 1.7;
}


/* -------------------------------------------------------
   FOOTER
------------------------------------------------------- */

.footer {

    text-align: center;

    color: #64748b;

    padding: 30px;

    font-size: 13px;
}


/* -------------------------------------------------------
   RESPONSIVE
------------------------------------------------------- */

@media(max-width: 1100px) {

    .cards {

        grid-template-columns:
            repeat(
                3,
                1fr
            );
    }
}

@media(max-width: 750px) {

    .cards {

        grid-template-columns:
            repeat(
                2,
                1fr
            );
    }

    .grid {

        grid-template-columns:
            1fr;
    }

    .header h1 {

        font-size: 32px;
    }

}

@media(max-width: 500px) {

    .cards {

        grid-template-columns:
            1fr;
    }

    .status {

        flex-direction:
            column;

        align-items:
            flex-start;

        gap: 15px;
    }
}

</style>

</head>


<body>


<!-- =====================================================
     HEADER
===================================================== -->

<div class="header">

    <h1>
        NET<span>Sage-AI</span>
    </h1>

    <p>
        AI-Assisted Network Troubleshooting Dashboard
    </p>

</div>


<div class="container">


<!-- =====================================================
     STATUS
===================================================== -->

<div class="status">

    <div>

        <h2>
            Network Intelligence Center
        </h2>

        <p>
            AI diagnosis and human review monitoring
        </p>

    </div>

    <div class="online">

        <span class="dot"></span>

        SYSTEM ONLINE

    </div>

</div>


<!-- =====================================================
     MAIN CARDS
===================================================== -->

<div class="cards">


<div class="card">

    <div class="card-title">
        Total Cases
    </div>

    <div class="card-value blue">
        {{ data.total_cases }}
    </div>

</div>


<div class="card">

    <div class="card-title">
        Reviewed
    </div>

    <div class="card-value purple">
        {{ data.reviewed }}
    </div>

</div>


<div class="card">

    <div class="card-title">
        Accepted
    </div>

    <div class="card-value green">
        {{ data.accepted }}
    </div>

</div>


<div class="card">

    <div class="card-title">
        Edited
    </div>

    <div class="card-value orange">
        {{ data.edited }}
    </div>

</div>


<div class="card">

    <div class="card-title">
        AI Agreement
    </div>

    <div class="card-value blue">
        {{ data.agreement }}%
    </div>

</div>


</div>


<!-- =====================================================
     TABLES
===================================================== -->

<div class="grid">


<!-- HUMAN REVIEW -->

<div class="section">

    <h2>
        Human Review Summary
    </h2>

    <p class="subtitle">
        AI diagnosis validation results
    </p>


    <table>

        <tr>

            <th>
                Decision
            </th>

            <th>
                Count
            </th>

        </tr>


        <tr>

            <td>
                <span class="badge badge-green">
                    Accepted
                </span>
            </td>

            <td>
                {{ data.accepted }}
            </td>

        </tr>


        <tr>

            <td>
                <span class="badge badge-orange">
                    Edited
                </span>
            </td>

            <td>
                {{ data.edited }}
            </td>

        </tr>


        <tr>

            <td>
                <span class="badge badge-red">
                    Rejected
                </span>
            </td>

            <td>
                {{ data.rejected }}
            </td>

        </tr>


        <tr>

            <td>
                <strong>
                    Remaining
                </strong>
            </td>

            <td>
                {{ data.remaining }}
            </td>

        </tr>

    </table>

</div>


<!-- SEVERITY -->

<div class="section">

    <h2>
        Severity Distribution
    </h2>

    <p class="subtitle">
        Network issue severity analysis
    </p>


    <table>

        <tr>

            <th>
                Severity
            </th>

            <th>
                Cases
            </th>

        </tr>


        {% for severity, count in data.severities.items() %}

        <tr>

            <td>

                {% if severity == "Critical" %}

                    <span class="badge badge-red">
                        {{ severity }}
                    </span>

                {% elif severity == "High" %}

                    <span class="badge badge-red">
                        {{ severity }}
                    </span>

                {% elif severity == "Medium" %}

                    <span class="badge badge-orange">
                        {{ severity }}
                    </span>

                {% elif severity == "Low" %}

                    <span class="badge badge-green">
                        {{ severity }}
                    </span>

                {% else %}

                    {{ severity }}

                {% endif %}

            </td>

            <td>
                {{ count }}
            </td>

        </tr>

        {% endfor %}

    </table>

</div>


<!-- NETWORK CONCEPTS -->

<div class="section">

    <h2>
        Network Issue Types
    </h2>

    <p class="subtitle">
        Troubleshooting concept distribution
    </p>


    <table>

        <tr>

            <th>
                Concept
            </th>

            <th>
                Cases
            </th>

        </tr>


        {% for concept, count in data.concepts.items() %}

        <tr>

            <td>
                {{ concept }}
            </td>

            <td>
                {{ count }}
            </td>

        </tr>

        {% endfor %}

    </table>

</div>


<!-- RESPONSIBLE AI -->

<div class="section responsible">

    <h2>
        Responsible AI
    </h2>

    <p>
        NETSage-AI provides network troubleshooting
        recommendations, but configuration changes
        always require human validation.
    </p>

    <p>
        Every diagnosis can be
        <strong>Accepted</strong>,
        <strong>Edited</strong>,
        or
        <strong>Rejected</strong>
        by a human reviewer.
    </p>

    <p>
        <strong>
            Human-corrected cases:
        </strong>

        {{ data.edited }}
    </p>

</div>


</div>


<!-- =====================================================
     FOOTER
===================================================== -->

<div class="footer">

    NETSage-AI • Responsible AI Network Troubleshooting

</div>


</div>


</body>

</html>

"""


# ---------------------------------------------------------
# DASHBOARD ROUTE
# ---------------------------------------------------------

@app.route("/")
def dashboard():

    data = get_dashboard_data()

    return render_template_string(
        HTML,
        data=data
    )


# ---------------------------------------------------------
# RUN APPLICATION
# ---------------------------------------------------------

if __name__ == "__main__":

    print()
    print("=" * 55)
    print(" NETSage-AI")
    print(" AI-Assisted Network Troubleshooting")
    print("=" * 55)
    print()
    print("Dashboard:")
    print("http://127.0.0.1:5000/")
    print()
    print("Press CTRL+C to stop.")
    print("=" * 55)

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )