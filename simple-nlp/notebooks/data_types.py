import re
import pickle
import pandas as pd

class Author():
    def __init__(self, mn_id = -1):
        self.cols = ["year","nrf"]
        
        self.mn_id = mn_id
        self.papers = {}
        
        # self.mn_id = mn_id
        # self.article_links = links
        # self.article_years = years
        # self.coauthors = authors
        # self.nones_count = nrf
    
    def update_author_info(self, pub_info, page_info):        
        if page_info["yr"] is None:
            year = re.findall(r"19[0-9]{2}|20[0-9]{2}",pub_info["name"])[0]
        else:
            year = page_info["yr"]        
        
        self.papers.update({
            pub_info["mn_link"]:
                {"year":year,
                 "nrf":page_info['nrf']}})
    
    def read_from_pubdb(self, mnlink, audb):
        for author,pubs in audb.db.items():            
            if mnlink in pubs:                
                self.papers.update({mnlink:pubs[mnlink]})
                return
        print(f'We cant find this {mnlink} in {type(self).__name__}')
        
            
        
        
        
        

    def show(self):
        print(self.mn_id)  
        
        for paper in self.papers:
            print(paper)    
        print(self.convert2dict())
    
    def convert2dict(self):
        return {self.mn_id:
            self.papers}
        
# https://www.reddit.com/r/learnpython/comments/774kjr/multiple_values_in_one_cell_in_pandas/        
class AuthorsDB():
    
    def __init__(self, adb={}):
        self.db = adb
        self.filename = "../data/dbase/authorsDB.pkl"
    
    def update_data(self, adb:Author):        
        for id, info in adb.items():            
            if id not in self.db:                                  
                self.db.update({id:info})                
            else:
                print(f"id {id} in self.db")                
                if self.db[id] != info:                                    
                    # self.db[id]["coathors"].update(info["coathors"]-self.db[id]["coathors"])
                    self.db[id].update(info)
                    # # print(f"Two info data are not equal \n{self.db[id]}\n{info}")
                    # # print(list({self.db[id]["links"]}-{info["links"]}))
                    # temp = list(set(info["links"])-set(self.db[id]["links"]))                    
                    # indexes = [info["links"].index(temp[i]) for i in range(len(temp))]
                    # for ind in indexes:
                    #     self.db[id]["links"].append(info["links"][ind])
                    #     self.db[id]["years"].append(info["years"][ind])
                    #     self.db[id]["nones_count"].append(info["nones_count"][ind])
                                    
    
    def check_key(self,key):        
        return key in self.db
    
    def pop_key(self,key):
        if self.check_key(key):        
            self.db.pop(key)
        else:
            print(f"There is no such element in {type(self).__name__} as {key}")
                    
    def show(self):
        print("printing AuthorsDB:")        
        for ind, item in self.db.items():
            print(f"ind = {ind}")
            print(f"item = {item}")
            
    def save(self,status='write',text=''):
        if text != '':
            print(text)
        if status == 'write':    
            with open(self.filename,'wb') as outp:
                pickle.dump(self.db, outp, pickle.HIGHEST_PROTOCOL)
        
    def load(self):
        try:
            with open(self.filename,'rb') as inp:
                self.db = pickle.load(inp)
        except:
            print(f"We have problems in {type(self).__name__} while reading file:{self.filename}")
                    

class Publication():
    
    def __init__(self,mn_id=0):        
        self.cols = ["mn_link","author_id","doi","udk","send","type","reference","by","paper","jour","yr","vol","issue","pages"]
        self.info_dict={keys:None for keys in self.cols}
        self.pub_info_cols =["mn_link"]
        self.page_info_cols =["author_id","doi","udk","send","type","reference","by","paper","jour","yr","vol","issue","pages"]
        self.info_dict["mn_link"] = mn_id
        # self.mn_link = mnlink
        # self.author_id = aus_id
        # self.doi = doi
        # self.udk = udk
        # self.send = send
        # self.type = type
        # self.reference = reference       
    
    def update_publication_info(self, pub_info, page_info):
        for item in self.pub_info_cols:
            if item in pub_info:
                self.info_dict[item] = pub_info[item]
                
        for item in self.page_info_cols:
            if item in page_info:
                self.info_dict[item] = page_info[item]
            
                
        # self.mn_link = pub_info["mn_link"]
        # self.author_id = page_info["author_id"]
        # self.doi = page_info["doi"]
        # self.udk = page_info["udk"]
        # self.send = page_info["send"]
        # self.type = page_info["type"]
        # self.reference = page_info["reference"]
        
    def show(self):
        for k,v in self.info_dict.items():
            print(k)
            print(v)      
        # print(self.mn_link)
        # print(self.author_id)
        # print(self.doi)
        # print(self.udk)
        # print(self.send)
        # print(self.type)
        # print(self.reference)
        print(self.convert2dict())
    
    def convert2dict(self):        
        mndic = {key:self.info_dict[key]  for key in self.info_dict.keys() if key!="mn_link"}
        return {self.info_dict["mn_link"]:mndic}
        # return {"mn_link":
        #     {"author_id":self.author_id,
        #      "doi": self.doi,
        #      "udk":self.udk,
        #      "send":self.send,
        #      "type":self.type,
        #      "reference":self.reference}}


class PublicationsDB():
    
    def __init__(self, pdb={}):
        self.db = pdb
        # self.cols = ["mn_link","author_id","doi","udk","type","references"]
        self.filename = "../data/dbase/publicationsDB.pkl"
    
    def update_data(self,pub):
        for id, info in pub.items():
            if id not in self.db:
                print(f"id {id} not in self.db")
                self.db.update({id:info})
            else:
                print(f"id {id} in self.db")
                if self.db[id] != info:
                    for key, val in info:
                        if (val != "") and (val is not None):
                            self.db[id][key]=val
     
    def check_key(self,key):
        return key in self.db

    def pop_key(self,key):
        if self.check_key(key):        
            self.db.pop(key)
        else:
            print(f"There is no such element in {type(self).__name__} as {key}")
       
    def show(self):
        print("printing PublicationsDB:")        
        for ind, item in self.db.items():
            print(f"ind = {ind}")
            print(f"item = {item}")
            
    # def save(self,text=''):
    #     if text != '':
    #         print(text)
    #     with open(self.filename,'wb') as outp:
    #         pickle.dump(self.db, outp, pickle.HIGHEST_PROTOCOL)
        
    def save(self,status='write',text=''):
        if text != '':
            print(text)
        if status == 'write':    
            with open(self.filename,'wb') as outp:
                pickle.dump(self.db, outp, pickle.HIGHEST_PROTOCOL)
        
    def load(self):
        try:
            with open(self.filename,'rb') as inp:
                self.db = pickle.load(inp)
        except:
            print(f"We have problems in {type(self).__name__} while reading file:{self.filename}")

class Abstract():
    
    def __init__(self, mn_link="", abstract="", keywords=""):
        # self.cols = ["mn_link","author_id","doi","udk","type","references"]
        self.mn_link = mn_link
        self.abstract = abstract
        self.keywords = keywords            
    
    def update_abstract_info(self, pub_info, page_info):
        self.mn_link = pub_info["mn_link"]
        self.abstract = page_info["abstract"]
        self.keywords = page_info["keywords"]       
        
    def show(self):        
        print(self.mn_link)
        print(self.abstract)
        print(self.keywords)        
        print(self.convert2dict())
    
    def convert2dict(self):
        return {self.mn_link:
            {"abstract": self.abstract,
             "keywords": self.keywords}}


class AbstractsDB():
    
    def __init__(self):        
        # cols = ["mn_link","abstract","keywords"]
        cols = ["abstract","keywords"]        
        self.db = pd.DataFrame(columns = cols)
        self.db.index.name = "mn_link"
        # self.cols = cols[1:]
        self.filename = "../data/dbase/abstractsDB.pkl"
    
    def update_data(self,datadict):        
        # https://stackoverflow.com/questions/42632470/how-to-add-dictionaries-to-a-dataframe-as-a-row        
        for id, info in datadict.items():
            print("id = ", id)
            if id not in self.db.index:                
                self.db.loc[id] = info                
            else:
                for col, val in info.items():
                    if (val is not None) and (val !=""):
                        self.db.loc[id,col] = val                                
                
    
    def check_key(self,key):
        return key in self.db.index
    
    def pop_key(self,key):
        if self.check_key(key):        
            self.db.drop([key], axis=0, inplace=True)
        else:
            print(f"There is no such element in {type(self).__name__} as {key}")
                
    
    def show(self):
        print("printing AbstractsDB:") 
        # print("columns:\n",self.db.columns)       
        # print("indexes:\n",self.db.index)
        for ind, row in self.db.iterrows():
            print(f"ind =")
            print(ind)
            print(f"row =")
            print(row)
            
    # def save(self,text=''):
    #     if text != '':
    #         print(text)
    #     with open(self.filename,'wb') as outp:
    #         pickle.dump(self.db, outp, pickle.HIGHEST_PROTOCOL)
            
    def save(self,status='write',text=''):
        if text != '':
            print(text)
        if status == 'write':    
            with open(self.filename,'wb') as outp:
                pickle.dump(self.db, outp, pickle.HIGHEST_PROTOCOL)
        
    def load(self):
        try:
            with open(self.filename,'rb') as inp:
                self.db = pickle.load(inp)
        except:
            print(f"We have problems in {type(self).__name__} while reading file:{self.filename}")