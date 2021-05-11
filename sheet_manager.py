#Provides a class to deal with the sheets stored in the data base and its format
#information explaining sheet's format in readme
import json
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
    def __init__(self, sheet_json_string):
        sheet_list = json.loads(sheet_json_string)
        Field.__init__(self, sheet_list)

    def get_sheet_json(self):
        sheet_dict = self.get_field_dict()
        sheet_json = json.dumps(sheet_dict)
        return sheet_json

    def get_display_info(self, path_string):
        #gets more or less user ready information from current path
        info_list = [path_string]
        path = path_string.split("/") if path_string else []
        field = self.get_field(path)

        if not field:
            return
        info_list.append(list(field.fields.keys()))
        info_list.append(field.raw_data)
        info_list.append([f"{key}: {value}" for key, value in field.sheet_dict.items()])
        return info_list

    def add_raw(self, data, path=[]):
        field = self.get_field(path)
        if not field:
            return
        field.raw_data.append(data)
        return "success"

    def add_dict_kv(self, key, value, path=[]):
        field = self.get_field(path)
        if not field:
            return
        field.sheet_dict[key] = value
        return "success"

    def add_field(self, name, path=[]):
        field = self.get_field(path)
        if not field:
            return
        field.fields[name] = Field([name,{}])
        return "success"

