from typing import List, Optional
import random

from asgiref.sync import async_to_sync
from celery import shared_task
from celery.signals import task_postrun
from celery.utils.log import get_task_logger
from project.database import db_context

from . import whitebox_reports_router
from .tasks import start_code_trusty, start_code_metric



@whitebox_reports_router.post("/start-project")
def start_project(search_version: str, group_name: str, b_version: str, check_options: Optional[List[str]] = None):
    return {"search_version": search_version, "group_name": group_name, "b_version": b_version, "check_options": check_options}