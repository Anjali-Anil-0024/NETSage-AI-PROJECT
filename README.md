# NETSage-AI

## AI-Assisted Network Troubleshooting & Security Diagnosis System

NETSage-AI is an AI-assisted network troubleshooting and security analysis tool built with a human-in-the-loop review model. It analyzes network cases and logs, generates rule-based diagnoses, and lets a human reviewer Accept, Edit, or Reject every AI-generated recommendation before any action is taken — because in production networks, configuration changes should always require human validation.

This project draws on networking fundamentals learned through Cisco Networking Academy, applied to a practical, AI-driven diagnostic workflow.

## Features

- Security & network case analysis across common domains: VLAN trunking, routing (OSPF, static), DHCP, NAT/PAT, ACLs, DNS, subnetting, and wireless
- AI-assisted diagnosis with automated diagnosis prompts
- Log review and analysis
- Rule-based security checking
- Human-in-the-loop review — every diagnosis is Accepted, Edited, or Rejected by a reviewer
- Structured, severity-tagged security data (Critical / High / Medium)
- Python-based implementation

## Dashboard Snapshot

| Metric | Value |
|---|---|
| Total Cases | 30 |
| Reviewed | 25 |
| Accepted | 23 |
| Edited | 2 |
| Rejected | 0 |
| AI Agreement Rate | 92.0% |

## Project Structure

NETSage-AI/
├── data/
│   └── cases.csv
├── logs/
│   ├── review-log.csv
│   └── review_log.csv
├── prompt/
│   └── diagnose_prompt.md
├── src/
│   ├── app.py
│   ├── diagnose.py
│   ├── main.py
│   ├── review.py
│   └── rule_checker.py
└── README.md

## How It Works

1. Case ingestion — Network issues are loaded from data/cases.csv
2. Diagnosis — diagnose.py uses the prompt defined in prompt/diagnose_prompt.md to generate an AI diagnosis for each case
3. Rule checking — rule_checker.py validates diagnoses against defined network/security rules
4. Human review — review.py logs reviewer decisions (Accept / Edit / Reject) to logs/review_log.csv
5. Dashboard — app.py surfaces review stats, severity distribution, and issue-type breakdowns

## Responsible AI

NETSage-AI provides network troubleshooting recommendations, but configuration changes always require human validation. No diagnosis is auto-applied — every case passes through human review before it's marked resolved.

## Tech Stack

- Language: Python
- Logic: Rule-based diagnostic engine + AI-assisted prompting
- Data: CSV-based case and log storage

## Status

System Online — actively logging and reviewing cases.