from flask import Flask, render_template
from flask import request
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

# Getting a file 
def get_file(file_name):
    file = request.files[file_name]                    
    if file:
        df = pd.read_excel(file)
        dictionary = df.to_dict()
        names = list(dictionary['Retailer_Account_Title'].values())
        return names

@app.route('/handle_data', methods=['POST'])
def handle_data():
        first_file = get_file('file1')
        second_file = get_file('file2')
        if first_file and second_file:
            all_names = get_file('file1') + get_file('file2')
            duplicates = []
            # Comparing the names of both files + finding duplicates
            for first_name in first_file:
                for second_name in second_file:
                    if first_name.lower() in second_name.lower(): 
                        duplicates.append(first_name.lower())
            # Getting the non duplicated data
            final_result = []
            for name in all_names:
                if name.lower() not in duplicates:
                    final_result.append(name)
            data_frame = pd.DataFrame({"NAMES": final_result})
            data_frame.to_excel('output.xlsx', index=False)
            return '<h3 style="background-color: darkgreen;color: #fff;font-family: Verdana; text-align:center; padding:1rem;">File Uploaded Successfully!</h3><br><br> <p style="text-align:center; font-family: Verdana;">👉 The output file has been generated Check it in your computer to see the result 😊</p>'
        else:
            return '<h3 style="background-color: red;color: #fff;font-family: Verdana; text-align:center; padding:1rem;">File Uploaded Failed!</h3><br><p style="text-align:center; font-family: Verdana;">👉 You did not choosed a file 😒</p><br><a href="/" style="margin-left: 45%;">Go Back</a>'
        

if __name__ == '__main__':
    app.run()

