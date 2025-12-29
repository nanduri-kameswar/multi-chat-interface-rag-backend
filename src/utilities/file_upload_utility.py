from enum import Enum

import fitz
from fastapi import UploadFile
from langchain_core.documents import Document

from src.core.exceptions.exceptions import ProcessingFailedError


class FileType(str, Enum):
    NONE = "none"
    PDF = "pdf"
    TXT = "txt"
    DOCX = "docx"


class FileParser:
    def __init__(self, file: UploadFile):
        self.file = file
        self.filename = file.filename.lower()

    def _detect_type(self) -> FileType:
        if self.filename.endswith(".pdf"):
            return FileType.PDF
        if self.filename.endswith(".txt"):
            return FileType.TXT
        if self.filename.endswith(".docx"):
            return FileType.DOCX
        return FileType.NONE

    async def parse(self) -> list[Document]:
        file_type = self._detect_type()

        if file_type == FileType.PDF:
            return await self._parse_pdf()

        if file_type == FileType.TXT:
            return await self._parse_txt()

        raise ProcessingFailedError(f"Unsupported file type: {file_type}")

    async def _parse_pdf(self) -> list[Document]:
        try:
            pdf_bytes = await self.file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")

            return [
                Document(
                    page_content=doc.load_page(i).get_text(),
                    metadata={
                        "page": i + 1,
                        "source": self.filename,
                    },
                )
                for i in range(doc.page_count)
            ]

        except Exception as exc:
            raise ProcessingFailedError(str(exc)) from exc

    async def _parse_txt(self) -> list[Document]:
        text = (await self.file.read()).decode()
        return [Document(page_content=text, metadata={"source": self.filename})]
