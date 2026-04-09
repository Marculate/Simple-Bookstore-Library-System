import csv
import os


class FileHandler:
    def __init__(self, data_dirctiory):
        self.data_directory = os.path.abspath(data_dirctiory)
        os.makedirs(self.data_directory, exist_ok=True)


    def original_file_path(self, file_name):
        return os.path.join(self.data_directory, file_name)


    def file_exist_confirmation(self, file_name, field_names=None):
        path = self.original_file_path(file_name)

        file_exist = os.path.isfile(path)

        if not os.path.exists(path):
            with open(path, "w", newline="", encoding="utf-8") as csvfile:
                if field_names is not None:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()



    def read_csv_file(self, file_name):
        path = self.original_file_path(file_name)
        if not os.path.exists(path):
            return []
        try:
            with open(path, "r", newline="", encoding="utf-8") as fh:
                reader = csv.DictReader(fh)
                return [dict(row) for row in reader]
        except PermissionError as exc:
            raise IOError(f"Permisson to read the file was denied: ´{path}` ") from exc



    def write_csv_file(self, file_name, rows, field_names):
        path = self.original_file_path(file_name)
        if field_names is not None:
            headers = field_names
        else:
            headers = list(rows[0].keys()) if rows else []
        try:
            with open(path, "w", newline="", encoding="utf-8") as fh:
                writer = csv.DictWriter(fh, fieldnames=headers)
                writer.writeheader()
                writer.writerows(rows)
        except PermissionError as exc:
            raise IOError(f"Permisson to write the file was denied: ´{path}`") from exc



    def append_csv_file(self, file_name, row, field_names=None):
        path = self.original_file_path(file_name)
        headers = field_names or list(row.keys())
        file_exist = os.path.isfile(path)
        try:
            with open(path, "a", newline="", encoding="utf-8") as fh:
                writer = csv.DictWriter(fh, fieldnames=headers)
                if not file_exist:
                    writer.writeheader()
                writer.writerow(row)
        except PermissionError as exc:
            raise IOError(f"Permission when appending to the file '{path}' was denied") from exc





    def delete_csv_file(self, file_name):
        path = self.original_file_path(file_name)
        if os.path.exists(path):
            os.remove(path)
            return True
        return False
