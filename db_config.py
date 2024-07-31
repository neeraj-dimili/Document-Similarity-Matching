import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

blocks = """
    CREATE TABLE IF NOT EXISTS block (
        block_id int primary key,
        co_ords varchar not null,
        is_image boolean,
        lines_in_block int,
        data varchar not null,
        page_id int
    )
"""

page = """
    CREATE TABLE IF NOT EXISTS page (
        page_id int primary key,
        page_number int not null,
        total_blocks int not null,
        template_id int not null
    )
"""

template = """
    CREATE TABLE template (
        template_id int primary key,
        name varchar(255) not null,
        name_regex varchar(255) not null,
        total_pages int not null,
        total_images int not null default 0
    )
"""
#
# invoice = """
#     CREATE TABLE template (
#         template_id int primary key,
#         name varchar not null,
#         total_pages int not null
#     )
# """

invoice_table = """
    CREATE TABLE IF NOT EXISTS invoice (
        invoice_id int primary key,
        template_id int foreign key references template(template_id),
        match_percentage int not null,
        data varchar not null
    )
"""

# keyword_table = """
#     CREATE TABLE IF NOT EXISTS keyword (
#         keyword_id int primary key,
#         keyword varchar(255) not null
#     )
# """
#
# invoice_keyword = """
#     CREATE TABLE IF NOT EXISTS keyword (
#         invoice_keyword_association_id int primary key,
#         keyword_id int FOREIGN key references keyword_table(keyword_id),
#         invoice_id int FOREIGN key references invoice_table(invoice_id)
#     )
# """


class DbConfig:

    @staticmethod
    def setup():
        print("establishing connection with in memory db....")
        DbConfig.clear_db()
        cursor.execute(blocks)
        cursor.execute(page)
        cursor.execute(template)
        conn.commit()
        print("connection established")

    @staticmethod
    def clear_db():
        print("dropping everything if existing...")
        cursor.execute("drop table if exists block")
        cursor.execute("drop table if exists page")
        cursor.execute("drop table if exists template")

    @staticmethod
    def close_connection():
        cursor.close()
        conn.close()
        print("connection closed...")
