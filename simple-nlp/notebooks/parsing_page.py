import re

def clean_text(text):
    if text is None:
        return None
    text = re.sub('[\n\t]','',text)
    text = re.sub('\xa0\xa0',' ',text)
    text = re.sub('\xa0',' ',text)
    text = text.rstrip(' ')
    text = text.lstrip(' ')
    text = re.sub('  ',' ',text)        
    text = re.sub('<i>','',text)
    text = re.sub('</b>','',text)
    text = re.sub('<b>','',text)    
    return text


def parsing_author_page(soup):
    papers={}
    pubs= soup.find_all('td', attrs={'align':'left', 'valign':"top"})
    for indx, pub in enumerate(pubs[1:]):         
        papers[indx+1] = get_paper_info_for_author(pub)  
    return papers


def get_paper_info_for_author(pub):
    result = {}    
    name = re.sub(' +',' ',pub.text)
    result['name'] = clean_text(name)             
    for a in pub.find_all('a'):               
        link = a.get('href')
        if 'elibrary.ru' in link:
            # result['elib_link'] = link
            result['elib_id'] = link.replace("https://elibrary.ru/item.asp?id=","")
            # re.findall('\d+',link)[0]
        if 'mathnet.ru' in link:
            result['mn_link'] = link.replace("http://mi.mathnet.ru/","")
    return result


def parsing_article_page(soup):   
    doi = None
    au_id = []
    au_name = []
    for item in soup.find_all("a",  attrs={"class":"SLink"}):
        href = item.get("href")
        if "//doi.org" in href:
            doi = href.replace("https://doi.org/","")
        if "personid=" in href:                
        # au_name = re.findall(r"\d\"\>(.+)\<",item)
            au_id.append(clean_text(re.findall(r"(?<=personid=)\d+",str(item))[0]))
            au_name.append(clean_text(item.text))
    
    values = {"abstract":"Аннотация:",
              "abstract_en":"Abstract:",
            "keywords":"слова:",
            "doi":"DOI",
            "udk":"УДК",
            "send":'редакцию:',
            "type":'публикации:',
            "reference":'цитирования:'
    }
    res = {}                        
    for line in soup.find_all('td',  attrs={'valign':"top"}):    
        if "публикации:" in line.text or "Аннотация:" in line.text:
            # mystr = line.text    
            # reference = line.i.text
            collection = line.find_all('div',  attrs={'class':"around-button"})
            if len(collection)>1:
                res = get_text_from_collection(collection, values) 
            else:                
                res = get_text_from_tag(line, values)
            if len(res)<2:
                print("Something goes wrong")
            res['author_names'] = au_name
            res['author_id'] = au_id
            if doi is not None:                
                res['doi'] = doi            
    ams = soup.find_all('div', attrs={'class':'showamsbib'})
    if len(ams)>0:
        bibitem = parsing_showamsbib(ams)
        res.update(bibitem)

    nc = 0
    for val in res.values():
        if (val=="") or (val is None):
            nc += 1
    res['nones_count']=nc
    return res

def parsing_showamsbib(ams):
    values = ["by","paper","jour","yr","vol","issue","pages"]      
    text =ams[0].code.__str__()    
    return {key:get_between_words(text,"\\"+key,'<br>') for key in values}
        
     

def get_text_from_collection(collection, values):    
    result = {}
    for k,_ in values.items():
        result[k] = None
        
    for tag in collection:
        for key, val in values.items():
            if val in tag.text:
                result[key]=get_paragraph(tag.text,val)
    return result

def get_paragraph(text,phrase):
    start = text.index(phrase)
    return clean_text(text[start+len(phrase):])
                
def get_text_from_tag(tag, values):    
    result = {}
    for k,_ in values.items():
        result[k] = None            
    for key, val in values.items():
        if val == 'цитирования:':
            result[key]=get_next_paragraph(tag.text,val)
        else:
            if val in tag.text:
                result[key]=get_between_angle_brackets(tag,val)
    return result

def get_between_angle_brackets(text,phrase):
    if type(text) != 'str':
        text = str(text)
    start = text.index(phrase)
    indx = [m.start() for m in re.finditer(r"\<",text[start+len(phrase):])]  
    end = 6
    nstart = 0
    for ind in indx:
        if ind>end:
            end = ind
            break
        nstart = ind    
    return clean_text(text[start+len(phrase)+nstart:start+len(phrase)+end])
    
def get_next_paragraph(text, phrase):
    result = None
    if phrase in text: 
        start = text.index(phrase)
        indx = [m.start() for m in re.finditer(r"\n\n",text[start:])]
        result = clean_text(text[start+len(phrase)+1:start+indx[0]])        
    return result

def get_regex_between_words(text,word1,word2,regex):
    result = None
    if (word1 in text) and (word2 in text):
        start = text.index(word1)
        end = text.index(word2)
        result = re.findall(regex,text[start:end])[0] 
    return result

def get_between_words(text,word1,word2):
    result = None    
    if (word1 in text) and (word2 in text):        
        start = text.index(word1)+len(word1)
        # print("start",start)
        end = text[start:].index(word2)        
        # print('end',end)
        result = text[start+1:start+end]        
    return result
