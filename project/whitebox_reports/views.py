from typing import List, Optional
import random

from asgiref.sync import async_to_sync
from celery import shared_task
from celery.signals import task_postrun
from celery.utils.log import get_task_logger
from project.database import db_context

from .tasks import start_code_trusty, start_code_metric



def start_project(search_version: str, group_name: str, b_version: str, check_options: Optional[List[str]] = None):
    pass