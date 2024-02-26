import random

import requests
from asgiref.sync import async_to_sync
from celery import shared_task
from celery.signals import task_postrun
from celery.utils.log import get_task_logger
from project.database import db_context

logger = get_task_logger(__name__)


@shared_task(name="default:start_code_trusty")
def start_code_trusty(search_version: str, group_name: str, b_version: str):
    logger.info(f"start_code_trusty: {search_version}, {group_name}, {b_version}")

    
@shared_task
def start_code_metric(search_version: str, group_name: str, b_version: str):
    logger.info(f"start_code_metric: {search_version}, {group_name}, {b_version}")


whitebox_report_task_dict = {
    'code_trusty': start_code_trusty,
    'code_metric': start_code_metric,
    # 'build_trusty': start_build_trusty,
    # 'secbinary_check': start_secbianry_check,
    # 'life_cycle': start_life_cycle,
}