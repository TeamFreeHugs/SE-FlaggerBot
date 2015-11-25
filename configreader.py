import json as JSON


class ConfigReader:
    def __init__(self, file_path):
        self.file = file_path
        try:
            self.json = JSON.load(open(file_path, 'r'))
        except:
            with open(file_path, 'w') as f:
                f.write('{}')
                f.close()
            self.json = JSON.load(open(file_path, 'r'))

    def has_value(self, name):
        return name in self.json

    def ensure_value(self, name, value):
        if not self.has_value(name):
            self.set_value(name, value)

    def set_value(self, name, value):
        self.json[name] = value

    def get_value(self, name):
        if name in self.json:
            return self.json[name]
        else:
            return None

    def save(self):
        with open(self.file, 'w') as file_var:
            file_var.write(JSON.dumps(self.json))
