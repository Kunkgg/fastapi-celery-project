import random
import pathlib

import requests
from asgiref.sync import async_to_sync
from celery import shared_task
from celery.signals import task_postrun
from celery.utils.log import get_task_logger
from project.database import db_context

from project.whitebox_reports.doc_report.doc_data import TemplateInfo
from project.whitebox_reports.doc_report.render import DocReportRenderer
from project.whitebox_reports.doc_report.doc_data import DocDataItem, EmbedFileInfo, DocDataItemType

logger = get_task_logger(__name__)


@shared_task(name="default:start_code_trusty")
def start_code_trusty(search_version: str, group_name: str, b_version: str):
    logger.info(f"start_code_trusty: {search_version}, {group_name}, {b_version}")

    
@shared_task
def start_code_metric(search_version: str, group_name: str, b_version: str):
    logger.info(f"start_code_metric: {search_version}, {group_name}, {b_version}")

@shared_task
def make_doc_report():
    tpl_fn = "tests/fixtures/doc_report_template_text.docx"
    output_fn = "report_files/doc_report_output_text.docx"
    tpl_info = TemplateInfo(file_path=pathlib.Path(tpl_fn))
    render = DocReportRenderer(tpl_info, output_fn)
    doc_data = [DocDataItem(name="test_text", type=DocDataItemType("text"), value="张三\n李四\n王五"),]
    render.render(doc_data)


whitebox_report_task_dict = {
    'code_trusty': start_code_trusty,
    'code_metric': start_code_metric,
    # 'build_trusty': start_build_trusty,
    # 'secbinary_check': start_secbianry_check,
    # 'life_cycle': start_life_cycle,
}