import pathlib
import unittest

from project.whitebox_reports.doc_report.doc_data import TemplateInfo
from project.whitebox_reports.doc_report.render import DocReportRenderer
from project.whitebox_reports.doc_report.doc_data import DocDataItem, EmbedFileInfo, DocDataItemType


class TestDocReport(unittest.TestCase):
    def test_doc_report_render_text(self):
        tpl_fn = "tests/fixtures/doc_report_template_text.docx"
        output_fn = "tests/fixtures/output/doc_report_output_text.docx"
        tpl_info = TemplateInfo(file_path=pathlib.Path(tpl_fn))
        render = DocReportRenderer(tpl_info, output_fn)
        doc_data = [DocDataItem(name="test_text", type=DocDataItemType("text"), value="张三\n李四"),]
        render.render(doc_data)

    def test_doc_report_render_table(self):
        tpl_fn = "tests/fixtures/doc_report_template_table.docx"
        output_fn = "tests/fixtures/output/doc_report_output_table.docx"
        table = {
            'cols': ['fruit', 'vegetable', 'stone', 'thing'],
            'contents': [
                {'cols': ['banana', 'capsicum', 'pyrite', 'taxi']},
                {'cols': ['apple', 'tomato', 'cinnabar', 'doubledecker']},
                {'cols': ['guava', 'cucumber', 'aventurine', 'card']},
            ],
        }
        tpl_info = TemplateInfo(file_path=pathlib.Path(tpl_fn))
        render = DocReportRenderer(tpl_info, output_fn)
        doc_data = [DocDataItem(name="test_table", type=DocDataItemType("table"), value=table),]
        render.render(doc_data)

    def test_doc_report_render_raw(self):
        tpl_fn = "tests/fixtures/doc_report_template_raw.docx"
        output_fn = "tests/fixtures/output/doc_report_output_raw.docx"
        tpl_info = TemplateInfo(file_path=pathlib.Path(tpl_fn))
        render = DocReportRenderer(tpl_info, output_fn)
        raw_fn = "tests/fixtures/raw.txt"
        doc_data = [DocDataItem(name="test_raw", type=DocDataItemType("raw"), src_path=pathlib.Path(raw_fn)),]
        render.render(doc_data)

    def test_doc_report_render_image(self):
        tpl_fn = "tests/fixtures/doc_report_template_image.docx"
        output_fn = "tests/fixtures/output/doc_report_output_image.docx"
        tpl_info = TemplateInfo(file_path=pathlib.Path(tpl_fn))
        render = DocReportRenderer(tpl_info, output_fn)
        image_fn = "tests/fixtures/screen_shot_1.jpeg"
        doc_data = [DocDataItem(name="test_image", type=DocDataItemType("image"), src_path=pathlib.Path(image_fn)),]
        render.render(doc_data)

    def test_doc_report_render_excel(self):
        tpl_fn = "tests/fixtures/doc_report_template_excel.docx"
        output_fn = "tests/fixtures/output/doc_report_output_excel.docx"
        tpl_info = TemplateInfo(file_path=pathlib.Path(tpl_fn))
        render = DocReportRenderer(tpl_info, output_fn)
        excel_fn = "tests/fixtures/sample.xlsx"
        doc_data = [DocDataItem(name="test_excel", type=DocDataItemType("excel"), src_path=pathlib.Path(excel_fn)),]
        render.render(doc_data)

    def test_doc_report_render_embed_file(self):
        tpl_fn = "tests/fixtures/doc_report_template_embed_file.docx"
        output_fn = "tests/fixtures/output/doc_report_output_embed_file.docx"
        sample_execl_fn = "tests/fixtures/sample.xlsx"
        sample_zip_fn = "tests/fixtures/sample.zip"
        embed_1 = EmbedFileInfo(name="sample_execl", place_holder="word/embeddings/Microsoft_Excel_Worksheet.xlsx")
        embed_2 = EmbedFileInfo(name="sample_zip", place_holder="word/embeddings/oleObject1.bin")
        tpl_info = TemplateInfo(file_path=pathlib.Path(tpl_fn), embed_files=[embed_1, embed_2])
        render = DocReportRenderer(tpl_info, output_fn)
        doc_data_1 = DocDataItem(name="sample_execl", type=DocDataItemType("embed_file"), src_path=pathlib.Path(sample_execl_fn))
        doc_data_2 = DocDataItem(name="sample_zip", type=DocDataItemType("embed_file"), src_path=pathlib.Path(sample_zip_fn))
        doc_data = [doc_data_1, doc_data_2]
        render.render(doc_data)
