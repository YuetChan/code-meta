import json
import jsonschema

class config_reader:

    def __init__(
            self, 
            fpath
            ):
        self.fpath = fpath

        with open(self.fpath, 'r') as f:
            try:
                self.data = json.load(f)
                self.is_valid = self.validate_schema()

            except json.JSONDecodeError:
                self.is_valid = False


    def validate_schema(self):
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "user": {"type": "string"},
                "file_paths":  {"type": "object"},
            },
            "required": ["name", "user", "file_paths"]
        }

        try:
            jsonschema.validate(self.data, schema)
            return True

        except jsonschema.ValidationError as e:
            print("JSON data is invalid:", e)
            return False


    def get_project_name(self):
        return self.data['name']


    def get_user(self):
        return self.data['user']


    def get_note(self, fpath):
        return self.data[fpath]['note']
    

    def get_plain_text_note(self, fpath):
        return self.data[fpath]['plain_text_note']


    def get_data_source(self):
        return self.data


    def update_data_soruce(self, data):
        with open(self.fpath, 'w') as outfile:
            json.dump(data, outfile)


    def create_new_config(dir):
        return ''
    


    
