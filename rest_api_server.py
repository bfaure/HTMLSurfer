
from flask import Flask,request 
from flask_restful import Resource,Api
from json import dumps
from flask_jsonpify import jsonify
from time import time

app=Flask(__name__)
api=Api(app)
fname="linked_to-count.tsv"
data=None

def load_data():
    global data
    print("Loading data...")
    f=open(fname,'r')
    data={}
    t0=time()
    for line in f:
        items=line.split("\t")
        if len(items)==2:
            data[items[0]]=items[1].strip()
    print("Loaded data in %d seconds."%int(time()-t0))
    return data 

def get_results(query):
    ct=0
    if query in data:     ct+=int(data[query])
    if query+'/' in data: ct+=int(data[query+'/'])
    return ct

class LinkCt(Resource):
    def get(self,url): 
        true_url=url.replace("&slash;","/")
        linked_to_ct=get_results(true_url)
        return {'count':str(linked_to_ct)}

api.add_resource(LinkCt,'/count/<url>')

if __name__=='__main__':
    load_data()
    app.run(port='5002')