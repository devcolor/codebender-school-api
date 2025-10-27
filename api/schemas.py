from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import date
from decimal import Decimal

class CohortRecord(BaseModel):
    # Primary Key
    id: Optional[int] = None
    
    # Core Identifying Fields
    Institution_ID: Optional[int] = None
    Cohort: Optional[str] = None
    Student_GUID: Optional[str] = None
    Cohort_Term: Optional[str] = None
    Student_Age: Optional[str] = None
    
    # Enrollment Information
    Enrollment_Type: Optional[str] = None
    Enrollment_Intensity_First_Term: Optional[str] = None
    
    # Placement Information
    Math_Placement: Optional[str] = None
    English_Placement: Optional[str] = None
    Reading_Placement: Optional[str] = None
    Dual_and_Summer_Enrollment: Optional[str] = None
    
    # Demographics
    Race: Optional[str] = None
    Ethnicity: Optional[str] = None
    Gender: Optional[str] = None
    First_Gen: Optional[str] = None
    
    # Financial Aid
    Pell_Status_First_Year: Optional[str] = None
    
    # Academic Status - Term 1
    Attendance_Status_Term_1: Optional[str] = None
    Credential_Type_Sought_Year_1: Optional[str] = None
    Program_of_Study_Term_1: Optional[int] = None
    GPA_Group_Term_1: Optional[Decimal] = None
    GPA_Group_Year_1: Optional[Decimal] = None
    
    # Credits by Year
    Number_of_Credits_Attempted_Year_1: Optional[int] = None
    Number_of_Credits_Earned_Year_1: Optional[int] = None
    Number_of_Credits_Attempted_Year_2: Optional[int] = None
    Number_of_Credits_Earned_Year_2: Optional[int] = None
    Number_of_Credits_Attempted_Year_3: Optional[int] = None
    Number_of_Credits_Earned_Year_3: Optional[int] = None
    Number_of_Credits_Attempted_Year_4: Optional[int] = None
    Number_of_Credits_Earned_Year_4: Optional[int] = None
    
    # Gateway Courses
    Gateway_Math_Status: Optional[str] = None
    Gateway_English_Status: Optional[str] = None
    AttemptedGatewayMathYear1: Optional[str] = None
    AttemptedGatewayEnglishYear1: Optional[str] = None
    CompletedGatewayMathYear1: Optional[str] = None
    CompletedGatewayEnglishYear1: Optional[str] = None
    GatewayMathGradeY1: Optional[str] = None
    GatewayEnglishGradeY1: Optional[str] = None
    
    # Developmental Courses
    AttemptedDevMathY1: Optional[str] = None
    AttemptedDevEnglishY1: Optional[str] = None
    CompletedDevMathY1: Optional[str] = None
    CompletedDevEnglishY1: Optional[str] = None
    
    # Retention and Persistence
    Retention: Optional[int] = None
    Persistence: Optional[int] = None
    
    # Completion Time - Bachelors
    Years_to_Bachelors_at_cohort_inst_: Optional[int] = None
    Years_to_Bachelor_at_other_inst_: Optional[int] = None
    First_Year_to_Bachelors_at_cohort_inst_: Optional[int] = None
    First_Year_to_Bachelor_at_other_inst_: Optional[int] = None
    
    # Completion Time - Associates/Certificate at Cohort Institution
    Years_to_Associates_or_Certificate_at_cohort_inst_: Optional[int] = None
    First_Year_to_Associates_or_Certificate_at_cohort_inst_: Optional[int] = None
    Years_to_Latest_Associates_at_Cohort_Inst: Optional[Decimal] = None
    Years_to_Latest_Certificate_at_Cohort_Inst: Optional[Decimal] = None
    First_Year_to_Associates_at_Cohort_Inst: Optional[Decimal] = None
    First_Year_to_Certificate_at_Cohort_Inst: Optional[Decimal] = None
    
    # Completion Time - Associates/Certificate at Other Institution
    Years_to_Associates_or_Certificate_at_other_inst_: Optional[int] = None
    First_Year_to_Associates_or_Certificate_at_other_inst_: Optional[int] = None
    Years_to_Latest_Associates_at_Other_Inst: Optional[Decimal] = None
    Years_to_Latest_Certificate_at_Other_Inst: Optional[Decimal] = None
    First_Year_to_Associates_at_Other_Inst: Optional[Decimal] = None
    First_Year_to_Certificate_at_Other_Inst: Optional[Decimal] = None
    
    # Last Enrollment
    Years_of_Last_Enrollment_at_cohort_institution: Optional[int] = None
    Years_of_Last_Enrollment_at_other_institution: Optional[int] = None
    
    # General Completion
    Time_to_Credential: Optional[Decimal] = None
    
    # Special Programs and Status
    Special_Program: Optional[str] = None
    NASPA_First_Generation: Optional[int] = None
    Incarcerated_Status: Optional[str] = None
    Military_Status: Optional[int] = None
    Employment_Status: Optional[int] = None
    Disability_Status: Optional[str] = None
    Foreign_Language_Completion: Optional[str] = None
    
    # Program Information
    Program_of_Study_Year_1: Optional[int] = None
    
    # Other Institution Details - STATE
    Most_Recent_Bachelors_at_Other_Institution_STATE: Optional[str] = None
    Most_Recent_Associates_or_Certificate_at_Other_Ins_dccdad65: Optional[str] = None
    Most_Recent_Last_Enrollment_at_Other_institution_STATE: Optional[str] = None
    First_Bachelors_at_Other_Institution_STATE: Optional[str] = None
    First_Associates_or_Certificate_at_Other_Institution_STATE: Optional[str] = None
    
    # Other Institution Details - CARNEGIE
    Most_Recent_Bachelors_at_Other_Institution_CARNEGIE: Optional[str] = None
    Most_Recent_Associates_or_Certificate_at_Other_Ins_5a42b456: Optional[str] = None
    Most_Recent_Last_Enrollment_at_Other_institution_CARNEGIE: Optional[str] = None
    First_Bachelors_at_Other_Institution_CARNEGIE: Optional[str] = None
    First_Associates_or_Certificate_at_Other_Instituti_9c09d367: Optional[str] = None
    
    # Other Institution Details - LOCALE
    Most_Recent_Bachelors_at_Other_Institution_LOCALE: Optional[str] = None
    Most_Recent_Associates_or_Certificate_at_Other_Ins_9cc1796c: Optional[str] = None
    Most_Recent_Last_Enrollment_at_Other_institution_LOCALE: Optional[str] = None
    First_Bachelors_at_Other_Institution_LOCALE: Optional[str] = None
    First_Associates_or_Certificate_at_Other_Institution_LOCALE: Optional[str] = None
    
    # Metadata
    school: Optional[str] = None
    dataset_type: Optional[str] = None
    created_at: Optional[str] = None

class CourseRecord(BaseModel):
    # Primary Key
    id: Optional[int] = None
    
    # Student Identification
    Student_GUID: Optional[str] = None
    Student_Age: Optional[str] = None
    
    # Demographics
    Race: Optional[str] = None
    Ethnicity: Optional[str] = None
    Gender: Optional[str] = None
    
    # Institution and Cohort
    Institution_ID: Optional[int] = None
    Cohort: Optional[str] = None
    Cohort_Term: Optional[str] = None
    Academic_Year: Optional[str] = None
    Academic_Term: Optional[str] = None
    
    # Course Details
    Course_Prefix: Optional[str] = None
    Course_Number: Optional[int] = None
    Section_ID: Optional[int] = None
    Course_Name: Optional[str] = None
    Course_CIP: Optional[int] = None
    Course_Type: Optional[str] = None
    
    # Course Indicators
    Math_or_English_Gateway: Optional[str] = None
    Co_requisite_Course: Optional[str] = None
    Core_Course: Optional[str] = None
    Core_Course_Type: Optional[str] = None
    Core_Competency_Completed: Optional[str] = None
    
    # Scheduling
    Course_Begin_Date: Optional[int] = None
    Course_End_Date: Optional[int] = None
    Delivery_Method: Optional[str] = None
    
    # Performance
    Grade: Optional[str] = None
    Number_of_Credits_Attempted: Optional[int] = None
    Number_of_Credits_Earned: Optional[int] = None
    
    # Transfer and External
    Enrolled_at_Other_Institutions: Optional[str] = None
    Enrollment_Record_at_Other_Institutions_STATEs: Optional[str] = None
    Enrollment_Record_at_Other_Institutions_CARNEGIEs: Optional[Decimal] = None
    Enrollment_Record_at_Other_Institutions_LOCALEs: Optional[str] = None
    
    # Additional Details
    Credential_Engine_Identifier: Optional[Decimal] = None
    Course_Instructor_Employment_Status: Optional[str] = None
    Course_Instructor_Rank: Optional[int] = None
    Term_Program_of_Study: Optional[int] = None
    
    # Metadata
    school: Optional[str] = None
    dataset_type: Optional[str] = None
    created_at: Optional[str] = None

class FinancialAidRecord(BaseModel):
    # Primary Key
    id: Optional[int] = None
    
    # Student Identification
    Student_ID: Optional[int] = None
    Institution_ID: Optional[int] = None
    
    # Cohort Information
    Cohort: Optional[str] = None
    Cohort_Term: Optional[str] = None
    Academic_Year: Optional[str] = None
    
    # Personal Information
    First_Name: Optional[str] = None
    Middle_Name: Optional[str] = None
    Last_Name: Optional[str] = None
    SSN: Optional[int] = None
    Student_Age: Optional[str] = None
    Date_of_Birth: Optional[int] = None
    
    # Financial Dependency and Housing
    Dependency_Status: Optional[str] = None
    Housing_Status: Optional[str] = None
    
    # Financial Aid Details
    Cost_of_Attendance: Optional[int] = None
    EFC: Optional[int] = None
    Total_Institutional_Grants: Optional[int] = None
    Total_State_Grants: Optional[int] = None
    Total_Federal_Grants: Optional[int] = None
    Unmet_Need: Optional[int] = None
    Net_Price: Optional[int] = None
    Applied_Aid: Optional[str] = None
    
    # Metadata
    school: Optional[str] = None
    dataset_type: Optional[str] = None
    created_at: Optional[str] = None

class TableCount(BaseModel):
    database: str
    table: str
    count: int

class DatabaseInfo(BaseModel):
    acronym: str
    full_name: str
    available_tables: List[str] = ["cohort", "course", "financial_aid"]
