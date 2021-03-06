import sys
sys.path.insert(1, '/mnt/c/Users/danie/OneDrive/Documents/Insight/')

from flask import Flask, render_template, request
from  Git.scripts.LSA_model import LemmaTokenizer
import Git.nba_smart_database.search_engine as backend


# Create the application object
app = Flask(__name__)


@app.route('/',methods=["GET","POST"]) #we are now using these methods to get user input
# @app.route('/')
def home_page():
    return render_template('index.html')  # render a template

@app.route('/output')
def recommendation_output():
#       
       # Pull input
       query =request.args.get('user_input')            
       
       # Case if empty
       if query =='':
           return render_template("index.html",
                                  my_input = query,
                                  my_form_result="Empty")
       else:
           # if query is non-empty, return the results of the search
           # TODO dates = ...
           results = backend.search(query)

           headlines = ['','','']
           for i in range(0,len(results)):
               headlines[i] = results[i][0]
           summaries = ['','','']
           for i in range(0,len(results)):
               summaries[i] = results[i][1] 

  



           return render_template("index.html",
                              my_input=query,
                              headline_1 = headlines[0],
                              headline_2 = headlines[1],
                              headline_3 = headlines[2],
                              summary_1 = summaries[0],
                              summary_2 = summaries[1],
                              summary_3 = summaries[2],   

                              my_form_result="NotEmpty")


# start the server with the 'run()' method
if __name__ == "__main__":
    app.run(debug=True) #will run locally http://127.0.0.1:5000/

