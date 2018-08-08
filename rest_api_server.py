
from flask import Flask,request 
from flask_restful import Resource,Api
from json import dumps
from flask_jsonpify import jsonify

app=Flask(__name__)
api=Api(app)
fname="linked_to-count.tsv"
data=None

def load_data():
    global data
    print("Loading data...")
    f=open(fname,'r')
    data={}
    for line in f:
        items=line.split("\t")
        if len(items)==2:
            data[items[0]]=items[1].strip()
    return data 

def get_results(query):
    if query in data: 
        return data[query]
    if query+'/' in data:
        return data[query+'/']
    return "NULL"


class Test(Resource):
    def get(self):
        return {'test':'test'}

class LinkCt(Resource):
    def get(self,url): 
        true_url=url.replace("&slash;","/")
        linked_to_ct=get_results(true_url)
        return {'count':linked_to_ct}


api.add_resource(Test,'/test')  
api.add_resource(LinkCt,'/count/<url>')

if __name__=='__main__':
    load_data()
    app.run(port='5002')