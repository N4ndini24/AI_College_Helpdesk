
import sqlite3
from pathlib import Path

# Use the database inside this project folder
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "college_faq.db"

faqs = [
    # 1. Admissions
    (
        "admission apply application process",
        "To apply for admission, check the college's official admission notice, verify your course eligibility, prepare the required documents, and submit the application as instructed."
    ),
    (
        "admission documents required certificates",
        "Commonly required documents include previous examination marksheets, a leaving or transfer certificate if applicable, identity proof, photographs, and category certificates if applicable. Confirm the official list with your college."
    ),
    (
        "bca eligibility qualification",
        "BCA eligibility depends on the college and university rules. Check the current admission notice for the required qualification and subjects."
    ),
    (
        "admission start date last date deadline",
        "Admission dates vary by college, course, and academic year. Please check the latest official college admission notice."
    ),
    (
        "online admission form website",
        "If online admission is available, use the official college admission portal. Follow the instructions in the latest admission notice."
    ),

    # 2. Courses
    (
        "courses available list programs",
        "The courses listed in this helpdesk project are BCA, BBA, B.Com, B.Sc, B.A., MCA, and MBA. Please confirm current availability with your college."
    ),
    (
        "bca duration years",
        "The duration of BCA depends on the applicable university curriculum. Check your university's current course structure for the exact duration."
    ),
    (
        "bca bba difference comparison",
        "BCA focuses mainly on computer applications and IT, while BBA focuses on business administration and management."
    ),
    (
        "mca after bca eligibility",
        "BCA graduates may be eligible for MCA, subject to the university's admission rules and any required subjects or entrance examinations."
    ),
    (
        "bcom career jobs options",
        "Career options after B.Com may include accounting, taxation, banking, finance, auditing support, and further studies such as M.Com or professional qualifications."
    ),

    # 3. Exams and Results
    (
        "exam timetable schedule date",
        "Check the official college or university examination notice for the latest exam timetable and dates."
    ),
    (
        "hall ticket admit card download",
        "Hall ticket download instructions are usually announced before examinations. Check the official student portal or contact the examination office."
    ),
    (
        "exam result marksheet check",
        "Check your official university result portal or college examination notice to find the latest result information."
    ),
    (
        "revaluation reassessment apply",
        "To apply for revaluation, check the university's official notification for eligibility, application deadlines, fees, and submission instructions."
    ),
    (
        "fail backlog supplementary exam",
        "If you fail a subject, check your university's rules for backlog or supplementary examinations and confirm the next examination schedule."
    ),

    # 4. Scholarships and Fees
    (
        "scholarship available schemes",
        "Scholarship availability depends on eligibility, course, category, income criteria, and current government or institutional schemes. Check the official scholarship portal and college notices."
    ),
    (
        "scholarship apply application process",
        "To apply for a scholarship, identify an eligible scheme, read its official requirements, prepare the documents, and submit the application through the prescribed portal."
    ),
    (
        "scholarship documents required",
        "Common scholarship documents may include an income certificate, previous marksheet, bank details, identity proof, admission proof, and category certificate if applicable. Check the scheme-specific requirements."
    ),
    (
        "college fees structure amount",
        "The exact fee depends on the course, academic year, and applicable college rules. Contact the college accounts office for the current fee structure."
    ),
    (
        "fees installment payment facility",
        "Fee installment facilities depend on college policy. Please contact the accounts office to confirm whether installments are available and what conditions apply."
    ),

    # 5. Student Services
    (
        "library timing opening hours",
        "Library timings can vary by college and academic schedule. Please confirm the current timings with the college library."
    ),
    (
        "wifi internet campus availability",
        "Campus Wi-Fi availability and access rules depend on college facilities. Contact the IT support desk or college office for details."
    ),
    (
        "bonafide certificate application",
        "To request a bonafide certificate, contact the college office and ask about the application form, required documents, processing time, and fees if any."
    ),
    (
        "college office contact phone email",
        "Please refer to the college's official website or notice board for verified office contact details and working hours."
    ),
    (
        "placement assistance jobs campus recruitment",
        "Placement support may include career guidance, resume preparation, interview practice, and recruitment drives. Contact your college placement cell to confirm the services offered."
    ),
]


def main():
    if not DB_PATH.exists():
        print(f"Database not found: {DB_PATH}")
        print("Please check that college_faq.db exists in the project folder.")
        return

    conn = sqlite3.connect(str(DB_PATH))

    try:
        cursor = conn.cursor()

        # Confirm that the expected table and columns exist.
        cursor.execute("PRAGMA table_info(faqs)")
        columns = {row[1] for row in cursor.fetchall()}

        if not {"keywords", "answer"}.issubset(columns):
            print("The faqs table does not have the expected columns.")
            print("No FAQs were added. Please check your database schema.")
            return

        added = 0
        skipped = 0

        for keywords, answer in faqs:
            cursor.execute(
                "SELECT 1 FROM faqs WHERE lower(keywords) = lower(?) LIMIT 1",
                (keywords,)
            )

            if cursor.fetchone():
                skipped += 1
                continue

            cursor.execute(
                "INSERT INTO faqs (keywords, answer) VALUES (?, ?)",
                (keywords, answer)
            )
            added += 1

        conn.commit()

        print("\n=== College FAQ Update Complete ===")
        print(f"New FAQs added: {added}")
        print(f"Existing FAQs skipped: {skipped}")
        print(f"Total FAQs in this batch: {len(faqs)}")

    except sqlite3.Error as error:
        conn.rollback()
        print(f"Database error: {error}")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
