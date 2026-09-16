from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def create_sample_pdf(filename: str, title: str, sections: list):
    os.makedirs("documents", exist_ok=True)
    filepath = os.path.join("documents", filename)
    c = canvas.Canvas(filepath, pagesize=letter)
    
    # Page 1
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 750, title)
    
    y = 710
    for section_title, paragraphs in sections:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, section_title)
        y -= 25
        c.setFont("Helvetica", 11)
        for p in paragraphs:
            # Basic text wrap
            words = p.split()
            line = ""
            for w in words:
                if len(line + " " + w) > 75:
                    c.drawString(50, y, line)
                    y -= 15
                    line = w
                else:
                    line += " " + w if line else w
            if line:
                c.drawString(50, y, line)
                y -= 20
        y -= 15
        if y < 100:
            c.showPage()
            y = 750

    c.save()
    
    # Also save TXT version for easy inspection
    txt_filepath = os.path.join("documents", filename.replace(".pdf", ".txt"))
    with open(txt_filepath, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        for section_title, paragraphs in sections:
            f.write(f"## {section_title}\n")
            for p in paragraphs:
                f.write(f"{p}\n\n")

print("Generating 5 sample employee policy documents...")

create_sample_pdf(
    "Leave_Policy.pdf",
    "Acme Corp - Employee Leave Policy",
    [
        ("Section 1: Vacation Leave Policy", [
            "All full-time employees accrue 15 days of paid vacation leave per calendar year during their first three years of service.",
            "Employees with more than 3 years of service accrue 20 days of paid vacation per year. Vacation requests must be submitted at least 2 weeks in advance via HR Portal."
        ]),
        ("Section 2: Sick and Personal Leave", [
            "Employees receive 10 days of paid sick leave annually. Unused sick leave up to 5 days can be carried over into the next calendar year.",
            "Sick leave taken for 3 or more consecutive business days requires a physician certificate note."
        ]),
        ("Section 3: Parental Leave", [
            "Acme Corp provides up to 12 weeks of fully paid parental leave for primary caregivers following the birth, adoption, or foster placement of a child.",
            "Secondary caregivers are eligible for 4 weeks of fully paid parental leave."
        ])
    ]
)

create_sample_pdf(
    "Remote_Work_Policy.pdf",
    "Acme Corp - Remote & Hybrid Work Policy",
    [
        ("Section 1: Work Location & Remote Eligibility", [
            "Full-time employees whose roles do not require physical presence may request a hybrid or fully remote work arrangement subject to manager approval.",
            "Hybrid employees are expected to work from the office at least 2 designated core days per week."
        ]),
        ("Section 2: Home Office Equipment Allowance", [
            "Approved remote employees receive a one-time home office setup stipend of up to $500 for ergonomic chairs, external monitors, and desktop accessories.",
            "A monthly internet reimbursement stipend of $50 is provided to all full-time remote staff."
        ]),
        ("Section 3: Core Working Hours & Availability", [
            "Remote employees must remain available on Slack and email during core business hours between 9:00 AM and 3:00 PM local time."
        ])
    ]
)

create_sample_pdf(
    "Travel_Expense_Policy.pdf",
    "Acme Corp - Travel & Expense Reimbursement Policy",
    [
        ("Section 1: Business Meals Reimbursement Limit", [
            "The maximum business meal reimbursement limit is $75 per person for dinner and $30 per person for lunch.",
            "Itemized receipts are strictly required for all expense claims exceeding $25."
        ]),
        ("Section 2: Airfare and Lodging Standards", [
            "All domestic flights must be booked in Economy Class at least 14 days in advance.",
            "Hotel accommodations are capped at $250 per night in standard tier cities and $350 per night in high-cost metro areas (NYC, SF, London)."
        ]),
        ("Section 3: Mileage and Ground Transportation", [
            "Personal vehicle mileage used for official business is reimbursed at the current IRS standard rate of 67 cents per mile."
        ])
    ]
)

create_sample_pdf(
    "Benefits_Guide.pdf",
    "Acme Corp - Employee Health & Benefits Guide",
    [
        ("Section 1: Health & Dental Coverage", [
            "Acme Corp covers 85% of monthly healthcare premiums for employees and 70% for enrolled dependents across PPO and HSA eligible plans.",
            "Wellness incentives include up to $300 annual gym or fitness subscription reimbursement."
        ]),
        ("Section 2: 401(k) Retirement Matching", [
            "Acme Corp matches 100% of employee 401(k) contributions up to 4% of base salary, with immediate 100% vesting upon hire."
        ]),
        ("Section 3: Professional Development & Tuition", [
            "Employees are eligible for up to $2,500 per calendar year in tuition or professional certification reimbursement after completing 6 months of employment."
        ])
    ]
)

create_sample_pdf(
    "Working_Hours_Policy.pdf",
    "Acme Corp - Standard Working Hours Policy",
    [
        ("Section 1: Standard Workweek", [
            "The standard workweek consists of 40 hours, typically scheduled Monday through Friday from 9:00 AM to 5:00 PM local time with a 1-hour lunch break.",
            "Flexible scheduling options (e.g. 8:00 AM - 4:00 PM) may be arranged with supervisor confirmation."
        ]),
        ("Section 2: Overtime & Time Off in Lieu", [
            "Non-exempt employees working beyond 40 hours per week will receive overtime pay at 1.5 times their regular hourly rate in compliance with federal law."
        ])
    ]
)

print("All sample policy documents generated in documents/")
