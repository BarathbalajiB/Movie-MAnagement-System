#<<--- Hello barry this page consist of the excess code that we write


#---------------------------This code is for sort the page based on the vote values--------------------------------
'''
def sort():
    if request.method == 'POST':
        vote = request.form['vote']
        compare = request.form['type']
        count = int(request.form['num'])
        if vote == 'up':
            if compare == 'lessthan':
                data = db.movies.find({vote:{"$lte":count}})
                return render_template("details.html", data=data)
            else:
                data = db.movies.find({vote: {"$gte": count}})
                return render_template("details.html", data=data)
        if vote == 'down':
            if compare == 'lessthan':
                data = db.movies.find({vote:{"$lte":count}})
                return render_template("details.html", data=data)
            else:
                data = db.movies.find({vote: {"$gte": count}})
                return render_template("details.html", data=data)
    return render_template("sort.html")
'''


#----------------------------------This is previous update code------------------------------------------------------------------#
'''def update_name():
    if request.method == 'POST':
        name = request.form['name']
        gener = request.form['gener']
        date = request.form['date']
        movies = db.movies
        data = movies.find_one({"movie_name": name})

        if data:
            movies.update_one({"movie_name":name},{"$set":{"release_date":date,"gener":gener}})
            return redirect(url_for("details"))

    return render_template("update_name.html")
'''

'''
<div class="col-lg-8">
        <div class="card mb-4">
          <div class="card-body">
            <div class="row">
              <div class="col-sm-3">
                <p class="mb-0">Full Name</p>
              </div>
              <div class="col-sm-9">
                <p class="text-muted mb-0">{{ name }}</p>
              </div>
            </div>
            <hr>
            <div class="row">
              <div class="col-sm-3">
                <p class="mb-0">Email</p>
              </div>
              <div class="col-sm-9">
                <p class="text-muted mb-0">{{ email }}</p>
              </div>
            </div>
            <hr>
            <div class="row">
              <div class="col-sm-3">
                <p class="mb-0">Recommendation</p>
              </div>
              <div class="col-sm-9">
                <p class="text-muted mb-0">{{ recommendation }}</p>
              </div>
            </div>
            <hr>
          </div>
        </div> 
    </div>
'''

'''
@app.route('/details/downvote/<name>', methods = ['POST', 'GET']) 
def downvote(name):
    #pdb.set_trace()
    userid = session['_user_id']
    movie = movies_db.find_one({"movie_name": name})
    mov_id = str(movie['_id'])
    up_vote = movie['up']
    down_vote = movie['down']
    data = user_db.find_one({'_id': ObjectId(userid)})
    if data is None or data.get(mov_id, None) == 0 or data.get(mov_id, None) is None:
        down_vote = down_vote + 1
        movies_db.update_one({'_id': mov_id}, {"$set": {'down': down_vote}})
        user_db.update_one({'_id': ObjectId(userid)}, {'$set': {mov_id: -1}}, upsert= True)
        return {'message': 'downvoted successfully', 'status': 'success'}
    if data.get(mov_id, None) == 1:
        up_vote = up_vote - 1
        down_vote = down_vote + 1
        movies_db.update_one({'_id': mov_id}, {"$set": {'up': up_vote}})
        movies_db.update_one({'_id': mov_id}, {"$set": {'down': down_vote}})
        user_db.update_one({'_id': ObjectId(userid)}, {'$set': {mov_id: -1}}, upsert= True)
        return {'message': 'downvoted successfully', 'status': 'success'}
    
    else : 
        return {'message': 'Same vote has been given already', 'status': 'Failed'}

'''