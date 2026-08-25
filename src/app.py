from flask import Flask, render_template_string
import csv
import os
from collections import Counter

app = Flask(__name__)

CASES_FILE = "data/cases.csv"
REVIEW_FILE = "logs/review_log.csv"


# -----------------------------
# LOAD CSV
# -----------------------------

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

            return list(csv.DictReader(file))

    except Exception:
        return []


# -----------------------------
# DASHBOARD DATA
# -----------------------------

def get_dashboard_data():

    cases = load_csv(CASES_FILE)
    reviews = load_csv(REVIEW_FILE)

    total_cases = len(cases)

    severity_counter = Counter()

    concept_counter = Counter()

    for case in cases:

        severity = str(
            case.get("severity", "Unknown")
        ).strip()

        concept = str(
            case.get("concept", "Unknown")
        ).strip()

        severity_counter[severity] += 1
        concept_counter[concept] += 1


    accepted = 0
    edited = 0
    rejected = 0

    for review in reviews:

        decision = str(
            review.get("human_decision", "")
        ).strip()

        if decision.lower() == "accepted":
            accepted += 1

        elif decision.lower() == "edited":
            edited += 1

        elif decision.lower() == "rejected":
            rejected += 1


    reviewed = accepted + edited + rejected

    if reviewed > 0:
        agreement = round(
            (accepted / reviewed) * 100,
            1
        )
    else:
        agreement = 0


    return {
        "total_cases": total_cases,

        "reviewed": reviewed,

        "accepted": accepted,

        "edited": edited,

        "rejected": rejected,

        "agreement": agreement,

        "severities": dict(
            severity_counter
        ),

        "concepts": dict(
            concept_counter
        )
    }


# -----------------------------
# HTML
# -----------------------------

HTML = """
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>NETSage-AI Dashboard</title>


<style>

/* ---------------------------
   BASIC
--------------------------- */

* {
    box-sizing: border-box;
}

body {

    margin: 0;

    font-family:
        Arial,
        Helvetica,
        sans-serif;

    background: #f1f5f9;

    color: #1e293b;

}


/* ---------------------------
   HEADER
--------------------------- */

.header {

    background:
        linear-gradient(
            135deg,
            #0f172a,
            #1e3a8a
        );

    color: white;

    padding: 28px 40px;

}


.header-content {

    max-width: 1200px;

    margin: auto;

}


.logo {

    font-size: 30px;

    font-weight: bold;

    letter-spacing: 1px;

}


.logo span {

    color: #38bdf8;

}


.header p {

    margin: 8px 0 0;

    color: #cbd5e1;

    font-size: 14px;

}


/* ---------------------------
   MAIN
--------------------------- */

.container {

    max-width: 1200px;

    margin: 30px auto;

    padding: 0 20px;

}


/* ---------------------------
   STATUS
--------------------------- */

.status {

    background: white;

    border-radius: 12px;

    padding: 16px 20px;

    margin-bottom: 22px;

    display: flex;

    justify-content: space-between;

    align-items: center;

    box-shadow:
        0 3px 12px
        rgba(0,0,0,0.06);

}


.status-title {

    font-weight: bold;

}


.online {

    color: #16a34a;

    font-size: 14px;

    font-weight: bold;

}


.dot {

    display: inline-block;

    width: 9px;

    height: 9px;

    background: #22c55e;

    border-radius: 50%;

    margin-right: 6px;

}


/* ---------------------------
   CARDS
--------------------------- */

.cards {

    display: grid;

    grid-template-columns:
        repeat(5, 1fr);

    gap: 16px;

}


.card {

    background: white;

    border-radius: 14px;

    padding: 20px;

    box-shadow:
        0 4px 15px
        rgba(0,0,0,0.06);

    border: 1px solid #e2e8f0;

    transition: 0.2s;

}


.card:hover {

    transform: translateY(-4px);

}


.card-title {

    color: #64748b;

    font-size: 12px;

    font-weight: bold;

}


.card-value {

    font-size: 30px;

    font-weight: bold;

    margin-top: 10px;

}


/* ---------------------------
   SECTIONS
--------------------------- */

.grid {

    display: grid;

    grid-template-columns:
        1fr 1fr;

    gap: 20px;

    margin-top: 22px;

}


.section {

    background: white;

    border-radius: 14px;

    padding: 22px;

    box-shadow:
        0 4px 15px
        rgba(0,0,0,0.05);

}


.section h2 {

    margin-top: 0;

    font-size: 19px;

}


.section-subtitle {

    color: #64748b;

    font-size: 13px;

    margin-bottom: 20px;

}


/* ---------------------------
   REVIEW
--------------------------- */

.review-row {

    display: flex;

    justify-content: space-between;

    align-items: center;

    padding: 13px;

    margin-bottom: 10px;

    border-radius: 9px;

    background: #f8fafc;

}


.review-count {

    font-weight: bold;

    font-size: 18px;

}


.accepted {

    color: #16a34a;

}


.edited {

    color: #d97706;

}


.rejected {

    color: #dc2626;

}


/* ---------------------------
   SEVERITY
--------------------------- */

.severity-row {

    margin-bottom: 18px;

}


.severity-top {

    display: flex;

    justify-content: space-between;

    margin-bottom: 7px;

    font-size: 13px;

    font-weight: bold;

}


.bar {

    height: 9px;

    background: #e2e8f0;

    border-radius: 10px;

    overflow: hidden;

}


.fill {

    height: 100%;

    border-radius: 10px;

}


/* ---------------------------
   TABLE
--------------------------- */

table {

    width: 100%;

    border-collapse: collapse;

}


th {

    text-align: left;

    background: #f8fafc;

    padding: 13px;

    color: #475569;

    font-size: 13px;

}


td {

    padding: 13px;

    border-bottom:
        1px solid #e2e8f0;

    font-size: 14px;

}


/* ---------------------------
   CONCEPT
--------------------------- */

.concept-row {

    display: flex;

    justify-content: space-between;

    padding: 13px 0;

    border-bottom:
        1px solid #e2e8f0;

}


.concept-count {

    color: #2563eb;

    font-weight: bold;

}


/* ---------------------------
   RESPONSIVE
--------------------------- */

@media(max-width: 1000px) {

    .cards {

        grid-template-columns:
            repeat(3, 1fr);

    }

}


@media(max-width: 700px) {

    .cards {

        grid-template-columns:
            repeat(2, 1fr);

    }

    .grid {

        grid-template-columns: 1fr;

    }

}


@media(max-width: 450px) {

    .cards {

        grid-template-columns: 1fr;

    }

    .header {

        padding: 25px 20px;

    }

}


/* ---------------------------
   FOOTER
--------------------------- */

.footer {

    text-align: center;

    color: #64748b;

    font-size: 12px;

    padding: 30px;

}

</style>

</head>


<body>


<!-- HEADER -->

<div class="header">

    <div class="header-content">

        <div class="logo">

            NET<span>Sage</span>-AI

        </div>

        <p>

            AI-Assisted Network
            Troubleshooting Dashboard

        </p>

    </div>

</div>


<div class="container">


<!-- SYSTEM STATUS -->

<div class="status">

    <div>

        <div class="status-title">
            Network Intelligence Center
        </div>

        <small>
            AI diagnosis and human review monitoring
        </small>

    </div>


    <div class="online">

        <span class="dot"></span>

        SYSTEM ONLINE

    </div>

</div>


<!-- KPI CARDS -->

<div class="cards">


    <div class="card">

        <div class="card-title">
            TOTAL CASES
        </div>

        <div class="card-value">
            {{ data.total_cases }}
        </div>

    </div>


    <div class="card">

        <div class="card-title">
            REVIEWED
        </div>

        <div class="card-value">
            {{ data.reviewed }}
        </div>

    </div>


    <div class="card">

        <div class="card-title">
            ACCEPTED
        </div>

        <div class="card-value accepted">
            {{ data.accepted }}
        </div>

    </div>


    <div class="card">

        <div class="card-title">
            EDITED
        </div>

        <div class="card-value edited">
            {{ data.edited }}
        </div>

    </div>


    <div class="card">

        <div class="card-title">
            AI AGREEMENT
        </div>

        <div class="card-value">
            {{ data.agreement }}%
        </div>

    </div>


</div>


<!-- TWO COLUMNS -->

<div class="grid">


<!-- HUMAN REVIEW -->

<div class="section">

    <h2>Human Review Summary</h2>

    <div class="section-subtitle">
        AI diagnosis validation results
    </div>


    <div class="review-row">

        <span class="accepted">
            ● Accepted
        </span>

        <span class="review-count">
            {{ data.accepted }}
        </span>

    </div>


    <div class="review-row">

        <span class="edited">
            ● Edited
        </span>

        <span class="review-count">
            {{ data.edited }}
        </span>

    </div>


    <div class="review-row">

        <span class="rejected">
            ● Rejected
        </span>

        <span class="review-count">
            {{ data.rejected }}
        </span>

    </div>


</div>


<!-- SEVERITY -->

<div class="section">

    <h2>Severity Distribution</h2>

    <div class="section-subtitle">
        Network issue severity analysis
    </div>


    {% set total =
        data.total_cases
        if data.total_cases > 0
        else 1
    %}


    {% for severity, count in data.severities.items() %}

    <div class="severity-row">

        <div class="severity-top">

            <span>
                {{ severity }}
            </span>

            <span>
                {{ count }}
            </span>

        </div>


        <div class="bar">

            <div
                class="fill"
                style="
                width: {{ (count / total) * 100 }}%;
                background:
                {% if severity|lower == 'critical' %}
                    #dc2626
                {% elif severity|lower == 'high' %}
                    #f97316
                {% elif severity|lower == 'medium' %}
                    #eab308
                {% else %}
                    #22c55e
                {% endif %};
                ">
            </div>

        </div>

    </div>

    {% endfor %}


</div>


</div>


<!-- NETWORK ISSUES -->

<div class="section" style="margin-top:22px;">

    <h2>Network Issue Types</h2>

    <div class="section-subtitle">
        Detected troubleshooting concepts
    </div>


    {% if data.concepts %}

        {% for concept, count in data.concepts.items() %}

        <div class="concept-row">

            <span>
                {{ concept }}
            </span>

            <span class="concept-count">
                {{ count }} cases
            </span>

        </div>

        {% endfor %}

    {% else %}

        <p style="color:#64748b;">
            No network issue data available.
        </p>

    {% endif %}


</div>


<!-- RESPONSIBLE AI -->

<div class="section" style="margin-top:22px;">

    <h2>Responsible AI</h2>

    <div class="section-subtitle">
        Human-in-the-loop safety mechanism
    </div>


    <div style="
        background:#eff6ff;
        padding:18px;
        border-radius:10px;
        line-height:1.7;
        font-size:14px;
    ">

        <strong>
            Human verification is required.
        </strong>

        <p>
            NETSage-AI provides network diagnosis
            recommendations, but configuration changes
            require human validation.
        </p>

        <p style="margin-bottom:0;">

            ✓ Accept AI diagnosis

            &nbsp;&nbsp;

            ✎ Edit diagnosis

            &nbsp;&nbsp;

            ✕ Reject diagnosis

        </p>

    </div>

</div>


</div>


<div class="footer">

    NETSage-AI © 2026
    | AI-Assisted Network Troubleshooting

</div>


</body>

</html>
"""


# -----------------------------
# ROUTE
# -----------------------------

@app.route("/")
def dashboard():

    data = get_dashboard_data()

    return render_template_string(
        HTML,
        data=data
    )


# -----------------------------
# START SERVER
# -----------------------------

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
