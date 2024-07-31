# -*- coding: utf-8 -*-
import json

import pymupdf
import pathlib

from repository import Repository


# block_start = "=============BLOCK_START============type: {type}\n"
# block_end = "=============BLOCK_END===========\n\n\n"


class Invoice:
    def __init__(self, filename, directory="train"):
        self.directory = directory
        self.filename: str = filename
        self.name_regex = self.extract_name()
        self.page_nums = 0
        self.blocks = []  # list contains [] that contains text as blocks for each page
        self.total_images = 0

    def extract_text(self):
        self.extract_name()
        with pymupdf.open(f"./document_similarity/{self.directory}/" + self.filename) as doc:
            for (index, page) in enumerate(doc):
                blocks_in_page = page.get_text("blocks")
                self.blocks.append(blocks_in_page)
                if index == 0:
                    self.total_images = len(list(filter(lambda block: block[6] == 1, blocks_in_page)))
                self.page_nums += 1

    def extract_name(self):
        filename = self.filename.replace('.pdf', '')
        result = ""
        ints = 0
        chars = 0
        regex_vals = ["-", "_", "."]
        for char in filename:
            if char in regex_vals:
                result += f"{ints}i{chars}s{char}"
                ints = 0
                chars = 0
            else:
                if char.isdigit():
                    ints += 1
                else:
                    chars += 1
        result += f"{ints}i{chars}s"
        return result

    def save(self):
        self.extract_text()
        Repository.save_template(self.filename, self.name_regex, self.blocks, self.page_nums, self.total_images)

    def get_similar_templates(self):
        self.extract_text()
        similar_templates = []
        page_number_and_name = Repository.get_templates_matching_pages_and_names(self.page_nums, self.name_regex)
        for template in page_number_and_name:
            matching_percentage = self.get_template_similarity_percentage(template)

            if matching_percentage > 60:
                similar_templates.append({"template": template[1], "matching_percentage": f"{matching_percentage}%"})

        return similar_templates

    def get_template_similarity_percentage(self, template):
        pages = Repository.get_pages_by_template_id(template[0])
        first_page_blocks_check = 0
        last_page_blocks_check = 0
        middle_page_blocks_check = 0
        for page in pages:
            page_number = page[1]
            page_blocks = page[2]  # no of blocks in that page
            if page_number == len(pages) - 1:
                if len(self.blocks[len(self.blocks) - 1]) in range(page_blocks - 10,
                                                                   page_blocks + 11):
                    last_page_blocks_check = 33*Invoice.get_abs_diff(len(self.blocks[len(self.blocks) - 1]), page_blocks)
                    last_page_blocks_check *= self.get_page_similarity_percentage(page)
            if page_number == 0:
                if len(self.blocks[0]) in range(page_blocks - 10, page_blocks + 10):
                    first_page_blocks_check = 33*Invoice.get_abs_diff(len(self.blocks[0]), page_blocks)
                    first_page_blocks_check *= self.get_page_similarity_percentage(page)
            if page_number == int(len(pages) / 2 - 1):
                if len(self.blocks[int(len(self.blocks) / 2 - 1)]) in range(page_blocks - 10,
                                                                            page_blocks + 10):
                    middle_page_blocks_check = 33*Invoice.get_abs_diff(len(self.blocks[int(len(self.blocks) / 2 - 1)]), page_blocks)
                    middle_page_blocks_check *= self.get_page_similarity_percentage(page)

        page_percentage_similarity = last_page_blocks_check + first_page_blocks_check + middle_page_blocks_check

        return page_percentage_similarity

    def get_page_similarity_percentage(self, page):
        page_blocks = Repository.get_blocks_by_page_id(page[0])
        curr_invoice_blocks = self.blocks[page[1]]

        return 1

    @staticmethod
    def get_abs_diff(a, b):
        return (100 - abs(- a + b))/100
