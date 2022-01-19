import json


class JsonDump:

    def __init__(self, help, success, result):
        self.result = result
        self.success = success
        self.help = help
        self.records = json.dumps(result['records'])


    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        return cls(**json_dict)

    def __repr__(self):
        return f'<JsonDump {self.records}>'

    def return_records(self):
        return json.loads(self.records)
