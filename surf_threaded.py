
from urllib.request import urlopen
from threading import Thread
from time import time
import signal

mapping=open("surf_report-concurrent.tsv","w")
log=open("errors-concurrent.log","w")
visited=0
debug=False
seen={}
errors=0
stop_threads=False

def load_page(url):
    global log
    try:
        return urlopen(url,timeout=2).read().decode('utf-8')
    except Exception as e:
        try: log.write("%s\n"%e)
        except: log.write("Couldn't write out error!")
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

def surf(url):
    global mapping
    global visited
    global seen
    global errors
    links=get_links(url)
    while len(links)>0:
        if stop_threads: return
        link,links=links[0],links[1:]
        if debug: print("surf: %s"%link)
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
    
def lifeguard(sig,frame):
    global stop_threads
    stop_threads=True

def concurrent_surf(urls):
    threads=[]
    for url in urls:
        threads.append(Thread(target=surf,args=(url,)))
    for thread in threads:
        thread.start()
    start_time=time()
    while True:
        threads_alive=0
        for thread in threads:
            if thread.is_alive(): threads_alive+=1
        if threads_alive==0 or stop_threads: break
        print("\rVisited: %d  |  Errors: %d  |  Workers: %d  |  Time: %d"%(visited,errors,threads_alive,time()-start_time),end="\r")
    print("\n")
    print("Process complete in %d seconds"%(time()-start_time))
    
signal.signal(signal.SIGINT,lifeguard)
surfs_up_at=["https://wikipedia.org","https://github.com","https://youtube.com","https://reddit.com",
    "https://cnn.com","https://yahoo.com","https://apple.com","https://nytimes.com",
    "https://liveleak.com","https://imdb.com","https://msnbc.com","https://weather.com",
    "https://amazon.com","https://facebook.com","https://microsoft.com","https://ibm.com"]
print("Surfing starting with %d threads, press Ctrl+C to exit."%len(surfs_up_at))
concurrent_surf(surfs_up_at)

