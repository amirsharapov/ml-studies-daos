import json
from typing import Dict

from daos.abstracts.files.base import File


class JsonFile(File):
    suffix = '.json'

    def dict(self):
        return json.loads(self.contents)

    def set_contents(self, contents: str | Dict):
        if isinstance(contents, dict):
            contents = json.dumps(contents)
        self.contents = contents
        return self
