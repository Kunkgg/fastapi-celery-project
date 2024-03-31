"""
使用 docxtpl 渲染 docx 模板
支持 docx 模板中的变量替换, 表格插入, 图片插入, 文件嵌入
"""

from typing import List

from docxtpl import DocxTemplate
from .doc_data import DocDataItem, EmbedFileInfo, TemplateInfo



class DocReportRenderer:
    def __init__(self, tpl_info: TemplateInfo, output_path):
        self.tpl_info = tpl_info
        self.tpl = DocxTemplate(tpl_info.file_path)
        self.output_path = output_path

    def render(self, doc_data: List[DocDataItem]):
        context = {}
        embed_file_infos: List[EmbedFileInfo] = []

        for item in doc_data:
            parsed_item = item.parse(self.tpl_info, self.tpl)
            context.update(parsed_item.context)
            if parsed_item.embed_file_info:
                embed_file_infos.append(parsed_item.embed_file_info)

        self.tpl.render(context)

        for embed_file_info in embed_file_infos:
            embed_file_info.apply(self.tpl)

        self.tpl.save(self.output_path)
