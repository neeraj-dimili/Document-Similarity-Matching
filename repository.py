from db_config import cursor, conn


class Repository:

    @staticmethod
    def save_template(name: str, name_regex, blocks: list[list], page_nums, total_images):

        # blocks -> contains length of number of pages and each ele
        # contains some number of blocks that indicates total no of blocks per page

        last_block_id = Repository.get_row_count("block")

        last_template_id = Repository.get_row_count("template") + 1

        last_page_id = Repository.get_row_count("page")

        conn.execute(
            f"insert into template values ({last_template_id}, '{name}', '{name_regex}', {page_nums}, {total_images})"
        )

        conn.commit()

        save_page_query = """
                insert into page values ({id}, {page_number}, {blocks}, {template_id});
            """

        save_block_query = """
            insert into block values ({id}, '{co_ords}', {is_image}, {total_lines}, '{data}', {page_id});
        """

        for (index, blocks_per_page) in enumerate(blocks):
            last_page_id += 1
            cursor.execute(save_page_query
                           .replace('{id}', str(last_page_id))
                           .replace('{page_number}', str(index))
                           .replace('{blocks}', str(len(blocks_per_page)))
                           .replace('{template_id}', last_template_id.__str__())
                           )

            for block in blocks_per_page:
                last_block_id += 1
                cursor.execute(save_block_query
                               .replace('{id}', str(last_block_id))
                               .replace('{co_ords}', str(block[0: 4: 1]))
                               .replace('{is_image}', 'true' if block[6] == 0 else 'false')
                               .replace('{total_lines}', str(len(block[4])))
                               .replace('{data}', str(block[4].count('\n')))
                               .replace('{page_id}', last_page_id.__str__())
                               )
        conn.commit()

    @staticmethod
    def get_templates_matching_pages_and_names(total_pages, name_regex):
        query = f"""
            select * from template
            where total_pages between ({total_pages - 2} and {total_pages + 2}) 
            and (name_regex = '{name_regex}'
            or name_regex like '{name_regex}%'
            or name_regex like '%{name_regex}')
        """
        cursor.execute(query)
        return cursor.fetchall()

    @staticmethod
    def get_pages_by_template_id(template_id):
        return cursor.execute(f"select * from page where template_id={template_id}").fetchall()

    @staticmethod
    def get_blocks_by_page_id(page_id):
        return cursor.execute(f"select * from block where page_id={page_id}").fetchall()

    @staticmethod
    def get_row_count(name):
        cursor.execute(f"select * from {name}")
        return len(cursor.fetchall())
