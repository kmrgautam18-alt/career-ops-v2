from backend.app.database.db import get_connection
import sqlite3


def get_all_jobs():
    """
    Retrieve all jobs from the database.
    Returns:
        List[dict]
    """

    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            company,
            title,
            status
        FROM jobs
        ORDER BY id
    """)

    jobs = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return jobs


def create_job(company, title, url):
    """
    Insert a new job into the database.
    Returns:
        int: Newly created job ID
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO jobs (
            company,
            title,
            url,
            status
        )
        VALUES (?, ?, ?, ?)
    """, (
        company,
        title,
        url,
        "NEW"
    ))

    conn.commit()

    job_id = cursor.lastrowid

    conn.close()

    return job_id


def get_job_by_id(job_id):
    """
    Retrieve a single job by its ID.
    Returns:
        dict | None
    """

    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            company,
            title,
            status
        FROM jobs
        WHERE id = ?
    """, (job_id,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return dict(row)

    return None

def update_job(job_id, company, title, url):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE jobs
        SET
            company = ?,
            title = ?,
            url = ?
        WHERE id = ?
    """, (
        company,
        title,
        url,
        job_id
    ))

    conn.commit()

    updated = cursor.rowcount

    conn.close()

    return updated

def delete_job(job_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM jobs
        WHERE id = ?
    """, (job_id,))

    conn.commit()

    deleted = cursor.rowcount

    conn.close()

    return deleted
