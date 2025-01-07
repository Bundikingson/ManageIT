class Task:
    def __init__(self, title, description):
        self.id = len(tasks)
        self.title = title
        self.description = description

    def to_dict(self):
        return {'id': self.id, 'title': self.title, 'description': self.description}

    def update(self, title, description):
        self.title = title
        self.description = description
