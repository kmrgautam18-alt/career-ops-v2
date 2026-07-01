from backend.app.database.db import get_connection

jobs = [
    (
        "Amazon",
        "Cloud Engineer",
        "https://amazon.jobs",
        "NEW"
    ),
    (
        "IBM",
        "Linux Administrator",
        "https://careers.ibm.com",
        "NEW"
    )
]

conn = get_connection()

cursor = conn.cursor()

for job in jobs:
    cursor.execute(
        """
        INSERT INTO jobs (
            company,
            title,
            url,
            status
        )
        VALUES (?, ?, ?, ?)
        """,
        job
    )

conn.commit()
conn.close()

print("Jobs imported")
