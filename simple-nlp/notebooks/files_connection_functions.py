from os.path import exists
from os import makedirs
import pickle

def save_html(data, mnid, name, status='write'):
    newpath = r'../data/'+mnid+'/'
    if not exists(newpath):
        makedirs(newpath)
    filename = "../data/"+mnid+"/"+name+".pkl"
    if status == 'write':        
        with open(filename,'wb') as outp:
            pickle.dump(data, outp, pickle.HIGHEST_PROTOCOL)