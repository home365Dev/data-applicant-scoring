import src.data_applicant_scoring.db_connections as db


#
def execute_to_db(**kwargs):
    data = kwargs.get('data', {})
    app_id = kwargs.get('applicant_id')

    for address in app_id:
        query = """INSERT INTO applicant_scoring_log(applicant_id, ml_response)
        VALUES ('""" + app_id + """', '""" + data + """');"""

        conn = db.connectToPost()
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()
