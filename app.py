from flask import Flask, render_template, request, redirect,url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

import os
from dotenv import load_dotenv
from urllib import parse



#connect to MongoDb collection.

load_dotenv()
uri = os.getenv('MONGO_URI')

client = MongoClient(uri)
db = client[os.getenv('MONGO_DBNAME')]
collection = db['coursesCollection']  
commentsColl = db['comments'] 


#Start Flask server and have routes for each endpoint. 
app = Flask(__name__, static_url_path='/static')

@app.route("/")
def home():

    return render_template("index.html")

@app.route("/course_search", methods=['GET'])
def courseSearch():
     
    search = request.args.get('q')

    if(not search):
      data = collection.find()
      return render_template("CourseSearch.html",data = data)
    else:
      collection.create_index([('classTitle', 'text'), ('classNumber',  'text'),('schedule', 'text'),('notes', 'text')])
      data = collection.find({"$text": {"$search": parse.unquote(search)}})
      return render_template("CourseSearch.html",data = data)



@app.route("/view_comments", methods=['GET','PUT'])
def viewComments():
     data = commentsColl.find()
     newData= []
     for doc in data:

       objInstance = ObjectId(doc['forID'])
       classCurrent = collection.find_one({"_id": objInstance})
       doc["articleTitle"] = classCurrent['classTitle']
       doc["classNumber"] = classCurrent['classNumber']
       doc["schedule"] = classCurrent['schedule']
       newData.append(doc)
     return render_template("ViewComments.html",data=newData)

@app.route("/delete_comments/<commentID>", methods=['GET','DELETE'])
def deleteComments(commentID):
     
     if request.method == 'DELETE':
          objDelete = ObjectId(commentID)
          commentsColl.delete_one({"_id": objDelete})
          return redirect("/view_comments", code=302)

             
 
     objInstance = ObjectId(commentID)
     data = commentsColl.find_one({"_id": objInstance})

     objInstance2 = ObjectId(data['forID'])
     articleTitle = collection.find_one({"_id": objInstance2})
     data["articleTitle"] = articleTitle['classTitle']
     data["classNumber"] = articleTitle['classNumber']
     data["schedule"] = articleTitle['schedule']



     return render_template("DeleteComments.html",data=data)

@app.route("/edit_comments/<commentID>", methods=['GET','PUT'])
def editComments(commentID):
     if request.method == 'PUT':
          print(request.json)
          objEdit = ObjectId(commentID)

          commentsColl.update_one({"_id": objEdit}, { "$set": { "name": request.json['newName'],"text": request.json['newCom'] } })

          return redirect("/view_comments", code=302)
 
     objInstance = ObjectId(commentID)
     data = commentsColl.find_one({"_id": objInstance})

     objInstance2 = ObjectId(data['forID'])
     articleTitle = collection.find_one({"_id": objInstance2})
     data["articleTitle"] = articleTitle['classTitle']
     data["classNumber"] = articleTitle['classNumber']
     data["schedule"] = articleTitle['schedule']



     return render_template("EditComments.html",data=data)




@app.route("/class/<classId>", methods=['GET', 'POST'])
def showClass(classId):
     if request.method == 'POST':
        username = request.values.get('name') # Your form's
        comment = request.values.get('comment') # input names
        commentsColl.insert_one({

             "name":username,
             "text": comment,
             "forID": classId,

        })

        
     objInstance = ObjectId(classId)
     data = collection.find_one({"_id": objInstance})
     comments = commentsColl.find({"forID": classId})
     return render_template("showClass.html", data=data, comments=comments)



if __name__ == "__main__":
    app.run(debug=True)
