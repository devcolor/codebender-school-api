#!/usr/bin/env python3
"""
Populate all ar_* tables from cohort data for all schools
"""
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# Database configurations
DATABASES = {
    'AL': {
        'db_name': 'Bishop_State_Community_College',
        'ar_table': 'ar_al'
    },
    'CSUSB': {
        'db_name': 'California_State_University_San_Bernardino',
        'ar_table': 'ar_csusb'
    },
    'KCTCS': {
        'db_name': 'Kentucky_Community_and_Technical_College_System',
        'ar_table': 'ar_kctcs'
    },
    'KY': {
        'db_name': 'Thomas_More_University',
        'ar_table': 'ar_ky'
    },
    'OH': {
        'db_name': 'University_of_Akron',
        'ar_table': 'ar_oh'
    }
}

def populate_ar_table(db_name, ar_table, school_code):
    """Extract analysis-ready data from cohort table and insert into ar_* table"""
    
    print(f"\n{'='*80}")
    print(f"Processing {school_code}: {db_name}")
    print('='*80)
    
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=int(os.getenv('DB_PORT', '3306')),
            database=db_name
        )
        
        cursor = conn.cursor()
        
        # Check if cohort table has data
        cursor.execute('SELECT COUNT(*) FROM cohort')
        cohort_count = cursor.fetchone()[0]
        print(f'Cohort table has {cohort_count} rows')
        
        if cohort_count == 0:
            print(f'⚠ No cohort data to process for {school_code}. Skipping.')
            cursor.close()
            conn.close()
            return
        
        # Clear existing ar data
        print(f'Clearing existing {ar_table} data...')
        cursor.execute(f'DELETE FROM {ar_table}')
        conn.commit()
        
        # Insert analysis-ready data from cohort
        print(f'Populating {ar_table} from cohort data...')
        
        insert_query = f"""
        INSERT INTO {ar_table} (
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
        
        print(f'✓ Successfully inserted {rows_inserted} rows into {ar_table}')
        
        # Verify
        cursor.execute(f'SELECT COUNT(*) FROM {ar_table}')
        ar_count = cursor.fetchone()[0]
        print(f'✓ {ar_table} now has {ar_count} rows')
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f'✗ Error processing {school_code}: {str(e)}')

def main():
    print("\n" + "="*80)
    print("POPULATING ALL ANALYSIS-READY TABLES")
    print("="*80)
    
    for school_code, config in DATABASES.items():
        populate_ar_table(
            config['db_name'],
            config['ar_table'],
            school_code
        )
    
    print("\n" + "="*80)
    print("✓ ALL ANALYSIS-READY TABLES POPULATED")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
