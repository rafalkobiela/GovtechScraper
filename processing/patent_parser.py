import os
from enum import Enum
from typing import Dict, Optional
from tika import parser

import requests
from bs4 import BeautifulSoup

from processing.scan_validator import scanned_document
from config.tika_config import TikaConfig


class OCR(Enum):
    yes = 'ocr_only'
    no = 'no_ocr'


def ocr_headers(ocr: OCR) -> Dict[str, str]:
    return {
        'Content-Type': 'application/pdf',
        'Accept': 'text/html'
    }


class PatentParser:
    def __init__(self, name: str, folder: str, data: bytes) -> None:
        config = TikaConfig()
        self.name = name
        self.folder = folder
        self.data = data
        self.scanned = False  # we assume so
        self.soup = None
        self._server_url = config.url

    def parse_html(self) -> str:
        """
        Should parse normally and in the event of scanned pdf, use ocr with *pol*
        :return:
        """
        parsed = self.parse(ocr=OCR.no)
        parsed_decoded = parsed.decode('utf-8')
        self.soup = BeautifulSoup(parsed_decoded, features="html.parser")

        self.scanned = scanned_document(self.soup)
        if self.scanned:  # send request to use tesseract
            parsed_ocr = self.parse(ocr=OCR.yes)
            parsed_ocr_decoded = parsed_ocr.decode('utf-8')
            self.soup = BeautifulSoup(parsed_ocr_decoded, features="html.parser")

        return self.soup.prettify()

    def parse(self) -> Optional[str]:
        output = parser.from_buffer(self.data)

        if output["status"] != 200:
            print(f'> file {self.name} status code {output.status_code}')
            print(f'> {output.content}')
        else:
            return output["content"]
