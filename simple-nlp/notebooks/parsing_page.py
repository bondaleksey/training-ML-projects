import re
def parsing_author_page(soup):
    pass

def parsing_article_page(soup):
    
    doi = None
    for item in soup.find_all("a",  attrs={"class":"SLink"}):
        href = item.get("href")
        if "//doi.org" in href:
            doi = href.replace("https://doi.org/","")
                
    for line in soup.find_all('td',  attrs={'valign':"top"}):    
        if "Аннотация:" in line.text or "Abstract:" in line.text:
            mystr = line.text    
            base_info = line.i.text 
              
    abstract = get_next_paragraph(mystr, "Аннотация:")
    kwords = get_next_paragraph(mystr, "Ключевые"+"\xa0"+"слова:")
    udk = get_next_paragraph(mystr, "УДК:")
    doi = get_next_paragraph(mystr, "DOI:")
    bib = get_next_paragraph(mystr,"Образец"+"\xa0"+"цитирования:")
    
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
    
    