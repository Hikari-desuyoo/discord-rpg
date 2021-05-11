#Provides a class to deal with the sheets stored in the data base and its format
#information explaining sheet's format in readme
from unidecode import unidecode


class Result():
    def __init__(self, item_type, path, content):
        self.type = item_type
        self.path = path
        self.content = content

    def __repr__(self):
        repr_string = f"[{self.type}]'{self.content}' on /{'/'.join(self.path)}"
        return repr_string

class Field():
    #basically a tree Node
    def __init__(self, field_list):
        self.name = field_list[0]
        self.sheet_dict = field_list[1] 
        not_dict = field_list[2:]
        self.fields = {}
        self.raw_data = []
        for item in not_dict:
            if type(item) == list:#if there's a field
                field = Field(item)
                self.fields[field.name] = field
            else:
                self.raw_data.append(item) 

    def search(self, keyword, path=[]):
        #keep track on the directory
        path = path[:]
        path.append(self.name)

        #returns result list with information about each result
        results = []
        search_lists = [[self.name], self.sheet_dict.keys(), self.sheet_dict.values(), self.raw_data]
        result_types = ["name", "key", "value", "raw"]
        for i, search_list in enumerate(search_lists):
            for item in search_list:
                if unidecode(keyword.lower()) in unidecode(item.lower()):
                    results.append(Result(result_types[i], path, item))

        #searches for other fields recursively
        if self.fields:
            for field in self.fields.values():
                results = results + field.search(keyword, path=path)

        return results

    def get_field_dict(self):
        field_dict = [self.name, self.sheet_dict] + self.raw_data
        for field in self.fields.values():
            field_dict.append(field.get_field_dict())
        return field_dict

    def get_field(self, path, current_path=[]):
        current_path.append(self.name)
        if not path:
            #end of required path was reached
            return self
        for field_name in self.fields.keys():
            if field_name == path[0]:
                path = path[1:]
                return self.fields[field_name].get_field(path)
        
        #path does not exist
        return None

    def __repr__(self):
        return f"[Field]{self.name}"

class Sheet(Field):
    def __init__(self, sheet_list = None):
        if not sheet_list:
            sheet_list = ["Unknown",{}]
        Field.__init__(self, sheet_list)

    def get_sheet(self):
        sheet_dict = self.get_field_dict()
        return sheet_dict

    def format_path(self, path):
        return path.split("/") if path else []

    def get_display_info(self, path=""):
        #gets more or less user ready information from current path
        info_list = [path]
        path = self.format_path(path)
        field = self.get_field(path)

        if not field:
            return
        info_list.append(list(field.fields.keys()))
        info_list.append(field.raw_data)
        info_list.append([f"{key}: {value}" for key, value in field.sheet_dict.items()])
        return info_list

    def add_raw(self, data, path=""):
        path = self.format_path(path)
        field = self.get_field(path)
        if not field:
            return "no_path"
        field.raw_data.append(data)
        return "success"

    def add_dict_kv(self, key, value, path=""):
        path = self.format_path(path)
        field = self.get_field(path)
        if not field:
            return "no_path"
        field.sheet_dict[key] = value
        return "success"

    def add_field(self, name, path=""):
        path = self.format_path(path)
        field = self.get_field(path)
        if not field:
            return "no_path"
        field.fields[name] = Field([name,{}])
        return "success"

    def search(self, path=""):
        path = self.format_path(path)
        return Sheet.search(self, path=path)

