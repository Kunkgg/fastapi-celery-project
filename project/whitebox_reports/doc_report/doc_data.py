"""
使用 docxtpl 渲染 docx 模板
支持 docx 模板中的变量替换, 表格插入, 图片插入, 文件嵌入
"""

from abc import abstractmethod
from typing import List, Optional, Dict, Union
from pathlib import Path
from enum import Enum

from pydantic import BaseModel, Field
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import pandas as pd


DEFAULT_DOC_IMAGE_WIDTH = 180

class DocDataItemType(Enum):
    text = "text"
    table = "table"
    image = "image"
    excel = "excel"
    raw = "raw"
    embed_file = "embed_file"


class EmbedFileInfo(BaseModel):
    name: str
    place_holder: str
    src_path: Optional[Path] = None

    def apply(self, tpl: DocxTemplate):
        tpl.replace_zipname(self.place_holder, self.src_path)


class TemplateInfo(BaseModel):
    file_path: Path
    embed_files: List[EmbedFileInfo] = Field(default_factory=list)

    def get_embed_file_place_holder(self, name: str) -> Optional[str]:
        for embed_file in self.embed_files:
            if embed_file.name == name:
                return embed_file.place_holder
        return None


class DocDataItem(BaseModel):
    name: str
    type: DocDataItemType
    src_path: Optional[Path] = None
    value: Optional[Union[str, Dict]] = None

    def parse(self, tpl_info: TemplateInfo, tpl: DocxTemplate):
        parser_dict = {
            DocDataItemType.text: TextDocDataItemParser,
            DocDataItemType.table: TabelDocDataItemParser,
            DocDataItemType.image: ImageDocDataItemParser,
            DocDataItemType.excel: ExcelDocDataItemParser,
            DocDataItemType.raw: RawDocDataItemParser,
            DocDataItemType.embed_file: EmbedFileDocDataItemParser,
        }
        parser = parser_dict[self.type](self)
        return parser.parse(tpl_info, tpl)

class ParsedDocDataItem(BaseModel):
    context: Dict
    embed_file_info: Optional[EmbedFileInfo] = None


class DocDataItemParser:
    def __init__(self, item: DocDataItem):
        self.item = item

    @abstractmethod
    def parse(self, tpl_info: TemplateInfo, tpl: DocxTemplate) -> ParsedDocDataItem:
        pass


class TextDocDataItemParser(DocDataItemParser):
    def parse(self, tpl_info: TemplateInfo, tpl: DocxTemplate) -> ParsedDocDataItem:
        return ParsedDocDataItem(context={self.item.name: self.item.value})

class TabelDocDataItemParser(DocDataItemParser):
    def parse(self, tpl_info: TemplateInfo, tpl: DocxTemplate) -> ParsedDocDataItem:
        return ParsedDocDataItem(context={self.item.name: self.item.value})

class ImageDocDataItemParser(DocDataItemParser):
    def parse(self, tpl_info: TemplateInfo, tpl: DocxTemplate) -> ParsedDocDataItem:
        return ParsedDocDataItem(context={self.item.name: InlineImage(tpl, str(self.item.src_path), width=Mm(DEFAULT_DOC_IMAGE_WIDTH))})
        
class ExcelDocDataItemParser(DocDataItemParser):
    """Excel 数据解析器, 导入 excel 第一个 sheet 的数据到 docx 模板中"""
    def parse(self, tpl_info: TemplateInfo, tpl: DocxTemplate) -> ParsedDocDataItem:
        if not self.item.src_path:
            raise ValueError("Excel data item must have src_path")

        return ParsedDocDataItem(context={self.item.name: self.read_excel(self.item.src_path)})

    def read_excel(self, src_path: Path) -> Dict:
        df = pd.read_excel(src_path)
        return {
            "cols": df.columns,
            "contents": [{"cols": row} for row in df.to_records(index=False)]
        }

class RawDocDataItemParser(DocDataItemParser):
    def parse(self, tpl_info: TemplateInfo, tpl: DocxTemplate) -> ParsedDocDataItem:
        if not self.item.src_path:
            raise ValueError("Raw data item must have src_path")

        return ParsedDocDataItem(context={self.item.name: self.item.src_path.read_text()})

class EmbedFileDocDataItemParser(DocDataItemParser):
    def parse(self, tpl_info: TemplateInfo, tpl: DocxTemplate) -> ParsedDocDataItem:
        place_holder = tpl_info.get_embed_file_place_holder(self.item.name)
        if not place_holder:
            raise ValueError(f"Embed file place holder not found for {self.item.name}")

        if not self.item.src_path:
            raise ValueError("Embed file data item must have src_path")

        return ParsedDocDataItem(context={}, embed_file_info=EmbedFileInfo(
            name=self.item.name,
            place_holder=place_holder,
            src_path=self.item.src_path
        ))
