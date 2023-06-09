

import pickle


class RSSource:
    def __init__(self) -> None:
        self.filename = "rss_db.pickle"

    def load(self):
        with open(self.filename, "rb") as f:
            self._db = pickle.load(f)
        return self._db

    def dump(self, data: any):
       with open(self.filename, "wb") as f:
           pickle.dump(data, f) 

    def add_rss(self,name: str, link: str):
        load_data = self.load()
        load_data.append(dict(name=name, link=link))
        self.dump(load_data)

    def delete_rss(self,name: str):
        load_data = self.load()
        for index in range(len(load_data)):
            if load_data[index]["name"] == name:
                del load_data[index]
        self.dump(load_data)



