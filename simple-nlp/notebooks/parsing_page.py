import re

def clean_text(text):
    if text is None:
        return None
    text = re.sub('[\n\t\xa0]','',text)
    text = text.rstrip(' ')
    text = text.lstrip(' ')
    return text

def parsing_author_page(soup):
    papers={}
    pubs= soup.find_all('td', attrs={'align':'left', 'valign':"top"})
    for indx, pub in enumerate(pubs[1:]):         
        papers[indx+1] = get_paper_info(pub)  
    return papers



def get_paper_info(pub):
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
            au_id.append(re.findall(r"(?<=personid=)\d+",str(item))[0])
            au_name.append(item.text)
                            
    for line in soup.find_all('td',  attrs={'valign':"top"}):    
        if "Аннотация:" in line.text or "Abstract:" in line.text:
            mystr = line.text    
            # reference = line.i.text 
              
    abstract = get_next_paragraph(mystr, "Аннотация:")
    if abstract is None:
        abstract = get_next_paragraph(mystr, "Abstract:")
    if abstract is None:
        print("We have some problems!!!\nabstract is None")
    else:
        abstract = clean_text(abstract)
    keywords = get_next_paragraph(mystr, "Ключевые"+"\xa0"+"слова:")    
    if keywords is None:
        keywords = get_next_paragraph(mystr, "Keywords:")
    if doi is None:
        doi = get_next_paragraph(mystr, "DOI:")
        if doi is not None:
            doi = doi.replace("https://doi.org/","")
    udk = clean_text(get_next_paragraph(mystr, "УДК:"))
    send = None
    if udk is not None:
        if "редакцию:" in udk:
            send = re.findall(r"(?<=редакцию:\s)\S+",udk)
            udk = re.findall(r"\S+(?=Поступила)",udk)
    pubtype = clean_text(get_next_paragraph(mystr, "публикации:"))
    reference = clean_text(get_next_paragraph(mystr,"Образец"+"\xa0"+"цитирования:"))
    if reference is None:
        reference = clean_text(get_next_paragraph(mystr,"Образец цитирования:"))
    res = { "author_names": au_name,
            "author_id": au_id,
            "abstract":abstract,
            "keywords":keywords,
            "doi":doi,
            "udk":udk,
            "send":send,
            "type":pubtype,
            "reference":reference}    
    nc = 0
    for val in res.values():
        if (val=="") or (val is None):
            nc += 1
    res['nones_count']=nc
    return res
    
def get_next_paragraph(text, phrase):
    result = None
    # print(f" in get_next_paragraph phrase = {phrase}")
    if phrase in text: 
        # print("phrase in text")       
        start = text.index(phrase)
        # print(start)    
        indx = [m.start() for m in re.finditer(r"\n",text[start:])]
        # print(indx)
        result = text[start+indx[0]+1:start+indx[1]]
    return result
    
