
from . import whitebox_reports_router
from .tasks import make_doc_report



@whitebox_reports_router.post("/doc-report")
def start_project():
    task = make_doc_report.delay()
    return {"task_id": task.id}