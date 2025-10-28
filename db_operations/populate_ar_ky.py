#!/usr/bin/env python3
"""
Populate ar_ky table from cohort data for Thomas More University (KY)
"""
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def populate_ar_ky():
    """Extract analysis-ready data from cohort table and insert into ar_ky"""
    
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=int(os.getenv('DB_PORT', '3306')),
        database='Thomas_More_University'
    )
    
    cursor = conn.cursor()
    
    # Check if cohort table has data
    cursor.execute('SELECT COUNT(*) FROM cohort')
    cohort_count = cursor.fetchone()[0]
    print(f'Cohort table has {cohort_count} rows')
    
    if cohort_count == 0:
        print('No cohort data to process. Exiting.')
        cursor.close()
        conn.close()
        return
    
    # Clear existing ar_ky data
    print('Clearing existing ar_ky data...')
    cursor.execute('DELETE FROM ar_ky')
    conn.commit()
    
    # Insert analysis-ready data from cohort
    print('Populating ar_ky from cohort data...')
    
    insert_query = """
    INSERT INTO ar_ky (
        student_id,
        years_to_bachelors_cohort,
        years_to_bachelor_other,
        first_year_bachelors_cohort,
        first_year_bachelor_other,
        years_to_assoc_cert_cohort,
        years_to_assoc_cert_other,
        first_year_assoc_cert_cohort,
        first_year_assoc_cert_other,
        naspa_first_gen,
        recent_assoc_cert_other_state,
        recent_assoc_cert_other_carnegie,
        first_assoc_cert_other_carnegie,
        recent_assoc_cert_other_locale,
        school,
        created_at
    )
    SELECT 
        Student_GUID as student_id,
        CAST(Years_to_Bachelors_at_cohort_inst_ AS CHAR) as years_to_bachelors_cohort,
        CAST(Years_to_Bachelor_at_other_inst_ AS CHAR) as years_to_bachelor_other,
        CAST(First_Year_to_Bachelors_at_cohort_inst_ AS CHAR) as first_year_bachelors_cohort,
        CAST(First_Year_to_Bachelor_at_other_inst_ AS CHAR) as first_year_bachelor_other,
        CAST(Years_to_Associates_or_Certificate_at_cohort_inst_ AS CHAR) as years_to_assoc_cert_cohort,
        CAST(Years_to_Associates_or_Certificate_at_other_inst_ AS CHAR) as years_to_assoc_cert_other,
        CAST(First_Year_to_Associates_or_Certificate_at_cohort_inst_ AS CHAR) as first_year_assoc_cert_cohort,
        CAST(First_Year_to_Associates_or_Certificate_at_other_inst_ AS CHAR) as first_year_assoc_cert_other,
        CAST(NASPA_First_Generation AS CHAR) as naspa_first_gen,
        Most_Recent_Associates_or_Certificate_at_Other_Ins_dccdad65 as recent_assoc_cert_other_state,
        Most_Recent_Associates_or_Certificate_at_Other_Ins_5a42b456 as recent_assoc_cert_other_carnegie,
        First_Associates_or_Certificate_at_Other_Instituti_9c09d367 as first_assoc_cert_other_carnegie,
        Most_Recent_Associates_or_Certificate_at_Other_Ins_9cc1796c as recent_assoc_cert_other_locale,
        school,
        NOW() as created_at
    FROM cohort
    WHERE Student_GUID IS NOT NULL
    """
    
    cursor.execute(insert_query)
    rows_inserted = cursor.rowcount
    conn.commit()
    
    print(f'Successfully inserted {rows_inserted} rows into ar_ky')
    
    # Verify
    cursor.execute('SELECT COUNT(*) FROM ar_ky')
    ar_count = cursor.fetchone()[0]
    print(f'ar_ky now has {ar_count} rows')
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    populate_ar_ky()
