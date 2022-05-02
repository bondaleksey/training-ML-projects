import re
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
        print(set(page_info["author_id"]))
        print(set(self.mn_id))
        print(set(page_info["author_id"]).difference({self.mn_id}))
        self.coathors.update(set(page_info["author_id"]).difference({self.mn_id}))

    def show(self):
        print(self.mn_id)
        print(self.article_links)
        print(self.article_years)
        print(self.coathors)
    
    def convert2dict(self):
        return {self.mn_id:
            [self.article_links,self.article_years,self.coathors]}
        
# https://www.reddit.com/r/learnpython/comments/774kjr/multiple_values_in_one_cell_in_pandas/        
class AuthorsDB():
    def __init__(self):
        cols = ['mn_id', ]
        self.df = pd.DataFrame(columns = [])
        #maybe just dict?