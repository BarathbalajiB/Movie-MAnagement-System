from flask import Flask, render_template, request, url_for, redirect, session, jsonify
#from flask_session import Session
#import flask_login
from flask_login import LoginManager, login_manager,login_required,  UserMixin, login_user, current_user, logout_user
import bcrypt
import pymongo
from bson.objectid import ObjectId


app = Flask(__name__)
app.secret_key = 'secretkey'
client = pymongo.MongoClient("mongodb+srv://moo1-student:m001-mongodb-basics@sandbox.pmgteep.mongodb.net/?retryWrites=true&w=majority")
db = client.Movie_Management_System # database name = login_users


user_db = db.user_cerdentials
movies_db = db.movies


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader      
def load_user(name):
    
    users = db.user_cerdentials
    data = users.find_one({'name':name})
    if data:
        return User(name=data['name'],password=data['password'], userid = str(data['_id']))
    else:
        return None

class User(UserMixin):
    def __init__(self, userid = None, name= None, password = None):
        self.name = name
        self.userid = userid
        

    def get_id(self):
        return self.userid

        

'''def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if 'name' in session:
            return func(*args,**kwargs)
        else:
            return "This is protucted  page You need to login again !"
            #return redirect(url_for('login'))
    return wrap'''    


@app.route('/', methods=['POST','GET'])
def Home():
    return render_template('login.html')


@app.route('/login', methods = ['POST', 'GET'])
def login():
    #pdb.set_trace()
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        
        data = user_db.find_one({'name': name})
    
        if data:
            if bcrypt.hashpw(password.encode('utf-8'), data['password']) == data['password']:
                logged_user = User( str(data['_id']), data['password'])
                login_user(logged_user)
                
                session['name'] = data['name']

                print(session)
                return redirect(url_for('dashboard')) 
            
        return {'message':'Invaild username or password'}
    return render_template('login.html')


@app.route('/dashboard', methods=['POST','GET'])
def dashboard():

    print(session)
    if 'name' in session:

        name = session["name"]  
        Genre = db.user_cerdentials.find_one({"name":name})
        movie_type = Genre["recommendation"]
        data = movies_db.find({"gener": movie_type})
        return render_template('dashboard.html', data = data)
    
    return redirect(url_for('login'))





@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        hashpass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        email = request.form['email']
        favs = request.form['gener']
        userid = session['_user_id']
        #user = db.user_cerdentials
        movie = movies_db.find()
        data = user_db.find_one({'email': email})

        if data is None :
            user_db.insert_one({'name': name, 'password': hashpass, 'email': email, 'recommendation': favs})
            
            session['name'] = name
            user_db.update_one({'_id': ObjectId(userid)}, {'$set':{name: 0}})
            return redirect(url_for('Home'))
        else:
            return {'meaasge': 'The user Email_Id already exist, kindly user another!', 'status': 'Registration failed'}

    return render_template("register.html")




@app.route('/add', methods = ['POST', 'GET']) 
def add():
    #pdb.set_trace()
    if request.method == 'POST':
        name = request.form['name']
        gener = request.form['gener']
        date = request.form['date']
        mov_var = movies_db.insert_one({"movie_name": name, "gener": gener, "release_date": date, "up": 0, "down": 0}).inserted_id
        mov_id = str(mov_var)
        user_db.update_many({ }, {"$set": {mov_id: 0}})
        return render_template('dashboard.html')
            
    return render_template('add.html')




@app.route('/update_name', methods = ['POST', 'GET'])
def update_name():
    if request.method == 'POST':
        name = request.form['movie_name']
        c_name = request.form['c_name']
        data = movies_db.find_one({"movie_name": name})


        if data :
            movies_db.update_one({"movie_name": name},{'$set':{"movie_name": c_name}})
            user_db.update_many({}, {'$rename':{name: c_name}})
            return {"message": "name successfully updated!", "status": "success!"}

    return render_template("update_name.html")



@app.route('/update_genre', methods = ['POST', 'GET'])
def update_genre():
    if request.method == 'POST':
        name = request.form['movie_name']

        data = movies_db.find_one({"movie_name": name})
        if data :
            return {"message": "name successfully updated!", "status": "success!"}

    return render_template("update_genre.html")


@app.route('/update_release', methods = ['POST', 'GET'])
def update_release():
    if request.method == 'POST':
        name = request.form['movie_name']
        
        
        data = db.movies.find_one({"movie_name": name})


        if data :
            '''db.movies.update_one({"movie_name": name},{'$set':{"movie_name": c_name}})
            db.user_cerdentials.update_many({}, {'$rename':{name: c_name}})'''
            return {"message": "name successfully updated!", "status": "success!"}

    return render_template("update_release.html")




@app.route('/delete', methods = ['POST', 'GET'])

def delete():
    if request.method == 'POST':
        m_name = request.form['name']
        
        data = movies_db.find_one({"movie_name": m_name})
        mov_id = str(data['_id'])

        if data:
            movies_db.delete_one({"movie_name": m_name})
            user_db.update_many({ }, {'$unset': {mov_id:{'$lte': 2}}})
            return {"Message": "Movie deleted successfully", "Status": "Success"}
        else:
            return {"Message": "Unable to find the movie", "Status": "Failure"}


    return render_template('delete.html')




@app.route('/details', methods = ['POST', 'GET'])
def details():
    if request.method == 'GET':
        data = movies_db.find()
        return render_template('details.html', data = data)
    

    

@app.route('/details/upvote/<mov_id>', methods = ['POST', 'GET'])
def upvote(mov_id):
    #pdb.set_trace()
    userid = session['_user_id'] 
    print(userid)
    movie = movies_db.find_one({'_id': ObjectId(mov_id)})
    up_vote = movie['up']
    down_vote = movie['down']
    data = user_db.find_one({'_id': ObjectId(userid)})
    
    print(data)
    if data is None or data.get(mov_id, None) == 0 or data.get(mov_id, None) is None :
        up_inc = up_vote + 1
        print(up_inc)
        movies_db.update_one({'_id': ObjectId(mov_id)}, {"$set": {'up': up_inc}})
        user_db.update_one({'_id': ObjectId(userid)}, {'$set': {str(mov_id): 1}}, upsert= True)
        return {'message': 'upvoted successfully', 'status': 'success'}
    if data.get(mov_id, None) == -1:
        up_inc = up_vote + 1
        print(up_inc)
        down_dec = down_vote -1
        print(down_dec)
        movies_db.update_one({'_id': ObjectId(mov_id)}, {"$set": {'up': up_inc}}) #use the $inc operator
        #print(movies_db.update_one({'_id': mov_id}, {"$set": {'up': up_inc}}))

        movies_db.update_one({'_id': ObjectId(mov_id)}, {"$set": {'down': down_dec}})
        
        user_db.update_one({'_id': ObjectId(userid)}, {'$set': {str(mov_id): 1}}, upsert= True)
        return {'message': 'upvoted successfully', 'status': 'success'}
    else : 
        return {'message': 'Same vote has been given already', 'status': 'Failed'}
    
    
    



@app.route('/details/downvote/<mov_id>', methods = ['POST', 'GET']) 
def downvote(mov_id):
    #pdb.set_trace()
    userid = session['_user_id']
    movie = movies_db.find_one({'_id': ObjectId(mov_id)})
    mov_id = str(movie['_id'])
    up_vote = movie['up']
    down_vote = movie['down']
    data = user_db.find_one({'_id': ObjectId(userid)})
    if data is None or data.get(mov_id, None) == 0 or data.get(mov_id, None) is None:
        down_inc = down_vote + 1
        print(down_inc)
        movies_db.update_one({'_id': ObjectId(mov_id)}, {"$set": {'down': down_inc}})
        user_db.update_one({'_id': ObjectId(userid)}, {'$set': {mov_id: -1}}, upsert= True)
        return {'message': 'downvoted successfully', 'status': 'success'}
    if data.get(mov_id, None) == 1:
        up_dec = up_vote - 1
        print(up_dec)
        down_inc = down_vote + 1
        print(down_inc)
        movies_db.update_one({'_id': ObjectId(mov_id)}, {"$set": {'up': up_dec}})
        movies_db.update_one({'_id': ObjectId(mov_id)}, {"$set": {'down': down_inc}})
        user_db.update_one({'_id': ObjectId(userid)}, {'$set': {mov_id: -1}}, upsert= True)
        return {'message': 'downvoted successfully', 'status': 'success'}
    
    else : 
        return {'message': 'Same vote has been given already', 'status': 'Failed'}
    
    
    




@app.route('/findone',methods=['POST','GET'])
def find():
    if request.method == 'POST':
        name = request.form['name']
        #date = request.form['r_date']
        data = movies_db.find_one({"movie_name":name})
        movie_name = data["movie_name"]
        gener = data["gener"]
        relese_date = data["release_date"]
        up_vote = data["up"]
        down_vote = data["down"]
        comment = movies_db.find_one({"comments": {'$exists': True}})
        keyNotExist = movies_db.find_one({"comments": {'$exists': False}})

        if data and keyNotExist:
            return jsonify({"movie_name":movie_name,"gener":gener,"release_date":relese_date,"up":up_vote,"down":down_vote})
        elif data and comment:
            return jsonify({"movie_name":movie_name,"gener":gener,"release_date":relese_date,"up":up_vote,"down":down_vote, "comments": comment})
            #return render_template("detial.html",name=movie_name,type=movie_type,date=relese_date,upvote=up_vote,downvote=down_vote)
        elif data is None:
            return {'Messgae': 'Movie unavailable', 'Status': 'Failed'}
    return render_template("dashboard.html")



    


@app.route('/review', methods = ['POST','GET'])
def review():
    if request.method == 'POST':
        m_name = request.form['mov_name']
        review = request.form['review']
        
        movie_exist = movies_db.find_one({"movie_name": m_name})
        
        
        print(session)

        if movie_exist:
            name = session["name"]
            movies_db.update_one({"movie_name": m_name}, {"$push": {"comments": [session['name'], review]}})
            return {'message': 'review added successfully', 'status': 'Successful'}
        else:
            return "This movie is not available!"
    return render_template('reviews.html')






@app.route('/genre', methods = ['POST', 'GET'])
def gener():
    if request.method == 'POST':
        gener = request.form['gener']
        name = session['name']
        data = movies_db.find({'gener': gener})
        user_db.update_one({'name': name}, {'$set': {'recommendation': gener}})
        user = user_db.find({'name': name} )
        
        return render_template('details.html', data = data)
    
    return render_template('dashboard.html')


'''@app.route('/recommendation', methods = ['POST', 'GET'])
def recommendation():
    if request.method == 'GET':
        name = session["name"]
        Genre = db.user_cerdentials.find_one({"name":name})
        movie_type = Genre["recommendation"]
        data = db.movies.find({"gener": movie_type})
        return render_template("dashboard.html", data=data)
'''
    

@app.route('/userprof', methods = ['POST', 'GET'])
def userprof():
    name = session["name"]
    users = user_db.find_one({'name': name})
    name = users['name']
    email = users['email']
    recommendations = users['recommendation']       
    return render_template("profile.html", name= name, email= email, recommendation= recommendations)
    #if users :
    #return render_template('profile.html', users = users)




@app.route('/search',methods=['POST','GET'])
def sort():
    if request.method == 'POST':
        vote = request.form['vote']
        compare = request.form['type']
        
        if vote == 'up' and compare == 'ascending':
            data = movies_db.find().sort(vote, 1)
            return render_template("details.html", data=data)
        elif vote == 'up' and  compare == 'descending':
            data = movies_db.find().sort(vote, -1)    
            return render_template("details.html", data=data)
        
        elif vote == 'down' and compare == 'ascending':
            data = movies_db.find().sort(vote, 1)
            return render_template("details.html", data=data)
        else:
            data = movies_db.find().sort(vote, -1)
            return render_template("details.html", data=data)
    return render_template("sort.html")



@app.route('/logout', methods = ['POST', 'GET'])
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug = True, port= 2000)
