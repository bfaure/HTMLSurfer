
from urllib.request import urlopen
from threading import Thread
from time import time,sleep
import signal

mapping=open("surf_report-concurrent.tsv","w")
log=open("errors-concurrent.log","w")
visited=0
debug=False
seen={}
errors=0
stop_threads=False
buffer=[]

def buffer_manager():
    global buffer 
    global errors
    while True:
        while len(buffer)>0:
            src,dest=buffer.pop()
            try:    mapping.write("%s\t%s\n"%(src,dest))
            except: errors+=1
        if stop_threads: return 
        sleep(1)

def lifeguard(sig,frame):
    global stop_threads
    stop_threads=True

def load_page(url):
    global log
    global errors
    try:
        return urlopen(url,timeout=2).read().decode('utf-8')
    except Exception as e:
        errors+=1
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
        end_idx=None 
        for end_tag in [' ','>','\"']:
            cur_end_idx=link.find(end_tag,start_idx)
            if end_idx==None or (cur_end_idx!=-1 and cur_end_idx<end_idx): end_idx=cur_end_idx
        if end_idx==-1: continue
        cleaned_link=link[start_idx:end_idx-1]
        if len(cleaned_link)<6: continue
        if debug: print("get_links: %s"%cleaned_link)
        if cleaned_link[:4]=="http": cleaned_links.append(cleaned_link) 
    return cleaned_links

def surf(url):
    global mapping
    global visited
    global seen
    global buffer
    links=get_links(url)
    while len(links)>0:
        if stop_threads: return        
        link,links=links[0],links[1:]
        if debug: print("surf: %s"%link)
        new_links=get_links(link)
        for new_link in new_links:
            buffer.append([link,new_link])
            if new_link not in seen:
                seen[new_link]=True
                visited+=1
                links.append(new_link)
    #print("\nThread that started with %s has died.\n"%url)

def concurrent_surf(urls):
    threads=[]
    for url in urls:
        threads.append(Thread(target=surf,args=(url,)))
    for thread in threads:
        if stop_threads: return
        thread.start()
    print("All threads online.\n")
    start_time=time()
    while True:
        threads_alive=0
        for thread in threads:
            if thread.is_alive(): threads_alive+=1
        if threads_alive==0 or stop_threads: break
        print("\rVisited: %d  |  Errors: %d  |  Workers: %d  |  Time: %d"%(visited,errors,threads_alive,time()-start_time),end="\r")
    print("\n")
    print("Process complete in %d seconds"%(time()-start_time))

print("\nStarting buffer manager...")    
buf_man=Thread(target=buffer_manager)
buf_man.start()
signal.signal(signal.SIGINT,lifeguard)
surfs_up_at=["https://www.wikipedia.org","https://www.github.com","https://www.youtube.com",
    "https://www.cnn.com","https://www.yahoo.com","https://www.apple.com","https://www.nytimes.com",
    "https://www.liveleak.com","https://www.imdb.com","https://www.msnbc.com","https://www.weather.com",
    "https://www.amazon.com","https://www.facebook.com","https://www.ibm.com","https://www.steemit.com"]
print("Surfing starting with %d threads, press Ctrl+C to exit."%len(surfs_up_at))
concurrent_surf(surfs_up_at)

