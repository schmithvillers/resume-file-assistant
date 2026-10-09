
"""Generate fictional resume files for assignment testing."""

from pathlib import Path

from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

BASE_DIR = Path(__file__).resolve().parent
RESUME_DIR = BASE_DIR / "sample_data" / "resumes"
RESUME_DIR.mkdir(parents=True, exist_ok=True)

RESUMES = [
    {
        "name": "john_doe",
        "format": "pdf",
        "text": """John Doe
Python Backend Developer

Experience:
3 years building backend applications using Python and Django.
Created REST APIs and automated deployments using AWS.

Skills:
Python, Django, PostgreSQL, Docker, AWS, Git

Education:
BSc Computer Science, 2022

Projects:
Built a task management API using Django REST Framework.
""",
    },
    {
        "name": "jane_smith",
        "format": "txt",
        "text": """Jane Smith
Java Software Engineer

Experience:
2 years developing enterprise applications with Java.
Built REST services using Spring Boot.

Skills:
Java, Spring Boot, SQL, Maven, Git

Education:
BTech Information Technology, 2023
""",
    },
    {
        "name": "alex_kumar",
        "format": "docx",
        "text": """Alex Kumar
Data Analyst

Experience:
Analyzed datasets and automated reports using Python.
Created dashboards and SQL queries for business teams.

Skills:
Python, Pandas, SQL, Excel, Power BI

Education:
BSc Statistics, 2021
""",
    },
    {
        "name": "emily_wilson",
        "format": "pdf",
        "text": """Emily Wilson
Frontend Developer

Experience:
Built responsive websites and reusable user interfaces.
Worked with React and modern JavaScript.

Skills:
JavaScript, React, HTML, CSS, Git

Education:
BSc Software Engineering, 2022
""",
    },
    {
        "name": "rahul_mehta",
        "format": "txt",
        "text": """Rahul Mehta
Automation Engineer

Experience:
Developed Python scripts for infrastructure automation.
Created monitoring tools and deployment workflows.

Skills:
Python, Linux, Bash, Git, Docker

Education:
BTech Computer Science, 2020
""",
    },
    {
        "name": "sarah_lee",
        "format": "docx",
        "text": """Sarah Lee
Cloud Infrastructure Engineer

Experience:
Managed cloud infrastructure and network configurations.
Automated infrastructure provisioning and monitoring.

Skills:
AWS, Terraform, Linux, Networking, Kubernetes

Education:
BSc Information Systems, 2021
""",
    },
    {
        "name": "michael_brown",
        "format": "pdf",
        "text": """Michael Brown
Database Administrator

Experience:
Maintained relational databases and optimized SQL queries.
Managed database backups and access controls.

Skills:
SQL, PostgreSQL, MySQL, Database Administration

Education:
BSc Computer Science, 2020
""",
    },
    {
        "name": "priya_shah",
        "format": "txt",
        "text": """Priya Shah
Machine Learning Engineer

Experience:
Built machine learning prototypes using Python.
Processed data and evaluated classification models.

Skills:
Python, Machine Learning, Pandas, NumPy, SQL

Education:
MSc Data Science, 2024
""",
    },
]


def create_pdf(path: Path, text: str) -> None:
    pdf = canvas.Canvas(str(path), pagesize=letter)
    width, height = letter
    y = height - 50

    for line in text.splitlines():
        if y < 50:
            pdf.showPage()
            y = height - 50

        pdf.drawString(50, y, line[:100])
        y -= 16

    pdf.save()


for resume in RESUMES:
    path = RESUME_DIR / f"{resume['name']}.{resume['format']}"
    text = resume["text"]

    if resume["format"] == "txt":
        path.write_text(text, encoding="utf-8")

    elif resume["format"] == "docx":
        document = Document()
        for line in text.splitlines():
            document.add_paragraph(line)
        document.save(path)

    elif resume["format"] == "pdf":
        create_pdf(path, text)

    print(f"Created: {path.name}")

print(f"\nCreated {len(RESUMES)} resumes in: {RESUME_DIR}")
