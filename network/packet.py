FIELD_LEN = 16
MAX_FIELD_VALUE = (2 ** FIELD_LEN) - 1


class Packet:

    def __init__(self, data=None):
        self.data = dict()
        if isinstance(data, dict):
            for field, value in data.items():
                self.set_field(field, value)

    def set_field(self, field, value):
        if not isinstance(field, str):
            raise Exception('The field name must be a string')
        if not isinstance(value, int):
            raise Exception('The value must be an integer')
        if not 0 <= value <= MAX_FIELD_VALUE:
            raise Exception(f'The value {value} does not fit in {FIELD_LEN} bit, must be between [0-{MAX_FIELD_VALUE}]')

        self.data[field] = value

    def get_field(self, field):
        if field not in self.data:
            raise Exception("The given field have not been set in this packet")
        return self.data[field]

    def get_available_fields(self):
        return sorted(self.data.keys())

    def get_available_field_values(self):
        return [self.get_field(field) for field in self.get_available_fields()]

    def __str__(self):
        return str(self.data)

    def __len__(self):
        return len(self.data)
