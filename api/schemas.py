from pydantic import BaseModel
from typing import Optional, List

class CohortRecord(BaseModel):
    id: int
    name: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    school: Optional[str] = None
    created_at: Optional[str] = None

class CourseRecord(BaseModel):
    id: int
    code: str
    title: str
    credits: Optional[int] = None
    description: Optional[str] = None
    school: Optional[str] = None
    created_at: Optional[str] = None

class FinancialAidRecord(BaseModel):
    id: int
    student_id: str
    aid_type: str
    amount: float
    semester: Optional[str] = None
    academic_year: Optional[str] = None
    school: Optional[str] = None
    created_at: Optional[str] = None

class TableCount(BaseModel):
    database: str
    table: str
    count: int

class DatabaseInfo(BaseModel):
    acronym: str
    full_name: str
    available_tables: List[str] = ["cohort", "course", "financial_aid"]
