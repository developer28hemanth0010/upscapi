from flask import Flask,jsonify, render_template, request
import sqlite3

app = Flask(__name__)


@app.route("/")
def main_page():
    return render_template("index.html")

@app.route("/play")
def getvalues():

        exam= request.args.get('exam') 
        gender= request.args.get('gender') 
        preference= request.args.get('pref') 
        input_dob= request.args.get('dob') 


        def calc(table,dob):

            conn= sqlite3.connect('dates.db',check_same_thread=False)
            c= conn.cursor()
            results_list= c.execute(f"""SELECT course from {table} WHERE starting_date <= '{dob}'
                                        and ending_date >= '{dob}'
                                    """)
            results_list= list(c.fetchall())
            conn.commit()
            results_list= [i for ele in results_list for i in ele]
    
            if table=="cse" and len(results_list) :
                results_list = ', '.join(str(v) for v in results_list)
                dataset= {'Calculated attempts':results_list,'dob':input_dob,'exam':exam,'gender':gender,'preference':preference}
                return jsonify(dataset)     

            elif len(results_list):
                results_list = ', '.join(str(v) for v in results_list)
                dataset= {'Calculated attempts':results_list,'dob':input_dob,'exam':exam,'gender':gender,'preference':preference}
                return jsonify(dataset)
                
            else:
                ageover_error='Your entered age is out of attempts.'
                dataset= {'Calculated attempts':ageover_error}
                return jsonify(dataset) 
            

        if exam=="nda" and (gender=="male" or gender=="female"):
            main_return= calc('nda',input_dob)
            return(main_return)

        elif exam=="cds" and gender=="male" and (preference=="ima" or preference=="ina"):
            main_return= calc('cds_ima_ina',input_dob)
            return(main_return)

        elif exam=="cds" and preference=="ota":
            main_return= calc('cds_ota_men_women',input_dob)
            return(main_return)

        elif exam=="afcat" and preference=="afa_flying":
            main_return= calc('afcat_fb',input_dob)
            return(main_return)

        elif exam=="afcat" and preference=="afa_gd":
            main_return= calc('afcat_gd',input_dob)
            return(main_return)
        
        elif exam=="cds" and gender=="male" and preference=="afa":
            main_return= calc('cds_afa',input_dob)
            return(main_return)

        elif exam=="cse":
            main_return= calc('cse',input_dob)
            return ((main_return))

        #ERRORS

        elif exam=="cds" and gender=="female" and (preference=="ima" or preference=="ina" or preference=="afa"):
            dataset={"calculated attempts":"Women are only eligibile to apply for OTA through CDS entry"}
            return dataset

        else:
            return "An Error has occured, try back again after some time"    


if __name__=="__main__":
    app.run(port=8080)
