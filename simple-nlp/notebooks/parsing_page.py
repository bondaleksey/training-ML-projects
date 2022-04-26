import re

def parsing_author_page(soup):
    papers={}
    pubs= soup.find_all('td', attrs={'align':'left', 'valign':"top"})
    for indx, pub in enumerate(pubs[1:]):         
        papers[indx+1] = get_paper_info(pub)  
    return papers



def get_paper_info(pub):
    result = {}
    name = re.sub('[\n\t\xa0]','',pub.text)
    name = re.sub(' +',' ',name)
    name = name.rstrip(' ')
    name = name.lstrip(' ')    
    result['name'] = name      
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
    # print("Однажды, в студеную зимнюю пору\n\
    #     Я из лесу вышел; был сильный мороз.\n\
    #         Гляжу, поднимается медленно в гору\n\
    #             Лошадка, везущая хворосту воз.\n\
    #                 И шествуя важно, в спокойствии чинном,\n\
    #                     Лошадку ведет под уздцы мужичок\n\
    #                         В больших сапогах, в полушубке овчинном,\n\
    #                             В больших рукавицах… а сам с ноготок! ")        
    doi = None
    for item in soup.find_all("a",  attrs={"class":"SLink"}):
        href = item.get("href")
        if "//doi.org" in href:
            doi = href.replace("https://doi.org/","")
                
    for line in soup.find_all('td',  attrs={'valign':"top"}):    
        if "Аннотация:" in line.text or "Abstract:" in line.text:
            mystr = line.text    
            # reference = line.i.text 
              
    abstract = get_next_paragraph(mystr, "Аннотация:")
    if abstract is None:
        abstract = get_next_paragraph(mystr, "Abstract:")
    keywords = get_next_paragraph(mystr, "Ключевые"+"\xa0"+"слова:")    
    if keywords is None:
        keywords = get_next_paragraph(mystr, "Keywords:")
    if doi is None:
        doi = get_next_paragraph(mystr, "DOI:").replace("https://doi.org/","")
    udk = get_next_paragraph(mystr, "УДК:")                
    reference = get_next_paragraph(mystr,"Образец"+"\xa0"+"цитирования:")
    if reference is None:
        reference = get_next_paragraph(mystr,"Образец цитирования:")
    res = {"Abstract":abstract,
            "Keywords":keywords,
            "DOI":doi,
            "UDK":udk,
            "Reference":reference}
    # print(res)
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
    
    