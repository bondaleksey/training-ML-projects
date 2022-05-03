import re
import pickle
class Author():
    def __init__(self, mn_id=0, links=[],years=[], authors=set()):
        self.mn_id = mn_id
        self.article_links = links
        self.article_years = years
        self.coathors = authors
    
    def update_author_info(self, pub_info, page_info):
        self.article_links.append(pub_info["mn_link"])
        year = re.findall(r"19|20[0-9]{2}",pub_info["name"])[0]
        self.article_years.append(year)
        # print(set(page_info["author_id"]))
        # print(set(self.mn_id))
        # print(set(page_info["author_id"]).difference(set([self.mn_id])))
        self.coathors.update(set(page_info["author_id"]).difference(set([self.mn_id])))

    def show(self):
        print(self.mn_id)
        print(self.article_links)
        print(self.article_years)
        print(self.coathors)
        print(self.convert2dict())
    
    def convert2dict(self):
        return {self.mn_id:
            {"links":self.article_links,
             "years": self.article_years,
             "coathors":self.coathors}}
        
# https://www.reddit.com/r/learnpython/comments/774kjr/multiple_values_in_one_cell_in_pandas/        
class AuthorsDB():
    
    def __init__(self, adb={}):
        self.db = adb
        self.filename = "../data/authorsDB.pkl"
    
    def update_data(self, adb):
        for id, info in adb.items():
            if id not in self.db.keys():
                print(f"id {id} not in self.db.keys()")
                self.db.update(adb)
            else:
                print(f"id {id} in self.db.keys()")
                if self.db[id] != info:                                    
                    # print(f"Two info data are not equal \n{self.db[id]}\n{info}")
                    # print(list({self.db[id]["links"]}-{info["links"]}))
                    temp = list(set(info["links"])-set(self.db[id]["links"]))                    
                    indexes = [info["links"].index(temp[i]) for i in range(len(temp))]
                    for ind in indexes:
                        self.db[id]["links"].append(info["links"][ind])
                        self.db[id]["years"].append(info["years"][ind])
                    self.db[id]["coathors"].update(info["coathors"]-self.db[id]["coathors"])
                    
    def show(self):
        print("printing AuthorsDB:")        
        for ind, item in self.db.items():
            print(f"ind = {ind}")
            print(f"item = {item}")
            
    def save(self):
        with open(self.filename,'wb') as outp:
            pickle.dump(self.db, outp, pickle.HIGHEST_PROTOCOL)
        
    def load(self):
        with open(self.filename,'rb') as inp:
            self.db = pickle.load(inp)
                    
                