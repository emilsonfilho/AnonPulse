from .classroom import Classroom
from .enrollment import Enrollment
from .feedback import Feedback
from .monitor_assignment import MonitorAssignment
from .monitor import Monitor
from .professor import Professor
from .student import Student
from .subject import Subject
from .document_metadata import DocumentMetadata

Classroom.model_rebuild()
Enrollment.model_rebuild()
Feedback.model_rebuild()
MonitorAssignment.model_rebuild()
Monitor.model_rebuild()
Professor.model_rebuild()
Student.model_rebuild()
Subject.model_rebuild()
DocumentMetadata.model_rebuild()

__all__ = [
    "Classroom",
    "Enrollment",
    "Feedback",
    "MonitorAssignment",
    "Monitor",
    "Professor",
    "Student",
    "Subject",
    "DocumentMetadata",
]
