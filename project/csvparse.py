import csv
import sqlite3
import os


class CSVParse:

    def __init__(self, db_name, table_name):
        """
        :param db_name: Name for sqllite database
        :param table_name: Name for table to store CSV data
        """
        self.db_name = db_name
        self.table_name = db_name

    def remove_db(self):
        """ Removes specified db file if it exists 
        """
        if os.path.isfile(self.db_name):
            os.remove(self.db_name)

    def get_sanitised_row(self, row):
        """ Basic sanitisation for data. (Remove quotation mark)

        :param row: CSV row
        """
        row_list = []
        for r in row:
            r = r.replace('"', "")
            row_list.append(r)

        return row_list

    def get_sanitised_columns(self, field_names):
        """ Basic sanitisation for data. Remove quotation mark,
        prevent empty string as column name

        :param field_names: CSV Headers
        """
        columns = []

        for col in field_names:
            col = col.strip().lower()
            col = col.replace(" ", "_")

            if len(col) < 1:
                col = "_"

            columns.append(col)

        return columns

    def create_database(self, field_names):
        """ Create sqllite database with table schema based on CSV headers

        :param field_names: CSV Headers
        """
        columns = self.get_sanitised_columns(field_names)

        table_sql = ""
        for c in columns:
            table_sql = table_sql + c + " TEXT,"

        table_sql = table_sql[:-1]

        table_sql = "(" + table_sql + ")"

        try:
            db = sqlite3.connect(self.db_name)
            cursor = db.cursor()
            # Check if table does not exist and create it
            cursor.execute(('''CREATE TABLE IF NOT EXISTS
                            {0} {1}''').format(self.table_name, table_sql))
            db.commit()

            return True, None

        except Exception as e:
            db.rollback()

            return False, e

        finally:
            db.close()

    def get_row_count(self):
        """ Counts table entries
        """
        db = sqlite3.connect(self.db_name)

        # Get a cursor object
        cursor = db.cursor()

        try:
            cursor.execute('''SELECT count(*) FROM {0}'''.format(self.db_name))
            result = cursor.fetchone()
        except Exception as e:
            print(e)
            pass

        db.close()

        if result is not None and len(result) > 0:
            return result[0]

        return 0

    def write_data_to_db(self, data):
        """ Write rows to table based on CSV Headers

        :param data: CSV row
        """
        db = sqlite3.connect(self.db_name)

        # Get a cursor object
        cursor = db.cursor()

        columns = self.get_sanitised_columns(data.fieldnames)
        column_items = '"{0}"'.format('", "'.join(columns))

        insertion_count = 0

        try:
            for row in data:
                row_items = self.get_sanitised_row(row.values())
                row_items = '"{0}"'.format('", "'.join(row_items))

                insert_row_sql = ('''
                INSERT INTO {0} ({1}) VALUES({2})
                '''.format(self.table_name, column_items, row_items))

                # Insert row
                cursor.execute(insert_row_sql)
                db.commit()

                insertion_count += 1

            db.close()

        except Exception as e:
            print(e)
            db.rollback()
            return False, 0, 0

        finally:
            db.close()

        """ Get total row count will be the same as insertion_count above
        as the db is recreated each run. This is done for verification.
        """
        total_rows = self.get_row_count()

        return True, insertion_count, total_rows

    def process_csv(self, filename):
        try:
            with open(filename, 'r') as csv_file:
                dr = csv.DictReader(csv_file, delimiter=',')

                # Removed sqlite db if exists.
                self.remove_db()

                # Creates the db schema
                result, err = self.create_database(dr.fieldnames)
                if err is not None:
                    print("Database error occurred:" + str(err))
                    return

                # Write csv rows to db
                success, inserted, total_rows = self.write_data_to_db(dr)

                return success, inserted, total_rows

        except Exception as e:
            print(str(e))
