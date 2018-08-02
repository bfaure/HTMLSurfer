
from urllib.request import urlopen
mapping=open("surf_report.tsv","w")
log=open("errors.log","w")
visited=0
debug=False
seen={}

def load_page(url):
    global log
    try:
        return urlopen(url,timeout=2).read().decode('utf-8')
    except Exception as e:
        log.write("%s\n"%e)
        log.flush()
        return ''

def get_links(url):
    html=load_page(url)
    links=html.split("<a")
    cleaned_links=[]
    for link in links:
        start_idx=link.find("href=")+6
        end_idx=min([link.find(" ",start_idx),link.find(">",start_idx)])
        cleaned_link=link[start_idx:end_idx-1]
        if debug: print("get_links: %s"%cleaned_link)
        if cleaned_link[:4]=="http": cleaned_links.append(link[start_idx:end_idx-1]) 
    return cleaned_links

def recursive_surf(url):
    global mapping
    global visited
    global seen
    print("\rVisited: %d"%visited,end="\r")
    links=get_links(url)
    for link in links:
        if debug: print("recursive_surf: %s"%link)
        mapping.write("%s\t%s\n"%(url,link))
        if link not in seen:
            seen[link]=True
            visited+=1
            recursive_surf(link)

def iterative_surf(url):
    global mapping
    global visited
    global seen
    errors=0
    links=get_links(url)
    while len(links)>0:
        link,links=links[0],links[1:]
        print("\rVisited: %d  |  Links: %s  |  Errors: %d"%(visited,len(links),errors),end="\r")
        if debug: print("iterative_surf: %s"%link)
        new_links=get_links(link)
        for new_link in new_links:
            try:mapping.write("%s\t%s\n"%(link,new_link))
            except: 
                errors+=1
                continue
            if new_link not in seen:
                seen[new_link]=True
                visited+=1
                links.append(new_link)
    
from random import choice
surfs_up_at=["https://wikipedia.org/","https://github.com","https://youtube.com"]
surf_spot=choice(surfs_up_at)
print("Surfing starting at %s"%surf_spot)
iterative_surf(surf_spot)

