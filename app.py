from flask import Flask, render_template
from pymongo import MongoClient

#connect to MongoDb collection.

#TODO Add uri to env file later

uri = "mongodb+srv://user-snbn:vE5Wuy014rIzjQrL@project-2-cluster.iijlv1n.mongodb.net/"

client = MongoClient(uri);
db = client['project-2-db']  
collection = db['coursesCollection']  # Replace "collection_name" with your collection name


#Start Flask server and have routes for each endpoint. 
app = Flask(__name__)

@app.route("/")
def home():
    data = collection.find();
    return render_template("index.html",data = data);

@app.route("/course_search", methods=['GET'])
def courseSearch():
     return render_template("CourseSearch.html")

@app.route("/view_comments", methods=['GET'])
def viewComments():
     return render_template("ViewComments.html")

@app.route("/delete_comments", methods=['GET'])
def deleteComments():
     return render_template("DeleteComments.html")


if __name__ == "__main__":
    app.run(debug=True)
