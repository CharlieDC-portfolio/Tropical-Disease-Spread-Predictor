from flask import Flask, render_template
from flask import jsonify
from flask import request
import matplotlib
import matplotlib.pyplot as pyplot
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import pandas as pd
from statsmodels.iolib.smpickle import load_pickle
import pickle
from tensorflow import keras
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import threading
from queue import Queue
import seaborn as sns
import base64

app = Flask(__name__)

@app.route('/')
def defaultPage():
    return render_template('Home.html')
@app.route('/StatsPage')
def statsPage():
    return render_template('Stats.html')
@app.route('/PredictPage')
def predictPage():
    return render_template('Predict.html')
@app.route('/InfoPage')
def infoPage():
    return render_template('Info.html')

def generateDiseaseGraph(startDate, endDate, disease, province, stanDev, q):
    var = pd.read_excel('Final_full_cleaned_dataset.xlsx', engine='openpyxl')


    var = var.drop(var[var.province != province].index)

    x = list(var['year_month'])
    y = list(var[disease])

    standardDeviation = np.std(y)*int(stanDev)

    s=next(i for i in range(len(x)) if str(x[i])[:7]==startDate)
    del x[0:s]
    t = next(i for i in range(len(x)-1,-1,-1) if str(x[i])[:7]==endDate)
    del x[t:len(x)]

    del y[0:s]
    del y[t:len(y)]

    fig, ax = pyplot.subplots()
    ax.plot(x, y)
    ax.set_title(''+province+' '+disease)
    ax.set_xlabel('Year-Month')
    ax.set_ylabel(disease)
    ax.axhline(y=standardDeviation, color = 'g', linestyle='-')
    img = io.BytesIO()
    pyplot.savefig(img, format='png')
    img.seek(0)
    img = img.getvalue()
    q.put(img)

@app.route('/plotdisease', methods=['POST'])
def returnDiseaseGraph():

    startDate = request.form.get('start')
    endDate = request.form.get('end')
    disease = request.form['disease']
    province = request.form.get('province')
    stanDev = request.form.get('sd')

    if  startDate=="" or endDate=="" or disease=="" or province==" " or int(stanDev)<0: 
        r = {"Error": True,"msg": "Please Input all required fields"}
        return jsonify(r)
    if endDate<startDate:
        r = {"Error": True,"msg": "Ensure Start Date preceeds End Date"}
        return jsonify(r)
    if stanDev == None:
        stanDev = 0
    q = Queue()
    t1 = threading.Thread(target = generateDiseaseGraph, args = (startDate, endDate, disease, province, stanDev, q))
    t1.start()
    img = q.get()
    b64_string = base64.b64encode(img).decode('utf-8')
    return jsonify({"img": b64_string, "Error": False})


def generateFactorGraph(startDate, endDate, environmentalFactors, province, stanDev, q1):
    var = pd.read_excel('Final_full_cleaned_dataset.xlsx', engine='openpyxl')


    var = var.drop(var[var.province != province].index)
    fig = pyplot.figure()
    for i in range(len(environmentalFactors)):
        x = list(var['year_month'])
        y = list(var[environmentalFactors[i]])

        standardDeviation = np.std(y)*int(stanDev)

        s=next(i for i in range(len(x)) if str(x[i])[:7]==startDate)
        del x[0:s]
        t = next(i for i in range(len(x)-1,-1,-1) if str(x[i])[:7]==endDate)
        del x[t:len(x)]

        del y[0:s]
        del y[t:len(y)]

        d = {'year_month':x, environmentalFactors[i]: y}
        reducedData = pd.DataFrame(d)

        pyplot.subplot(len(environmentalFactors), 1, i+1)
        pyplot.title(''+province+' '+environmentalFactors[i])
        pyplot.xlabel('Year-Month')
        pyplot.ylabel(environmentalFactors[i])
        pyplot.axhline(y=standardDeviation, color = 'g', linestyle='-')
        sns.lineplot(data=reducedData, x="year_month", y=environmentalFactors[i])
        
    img = io.BytesIO()
    pyplot.savefig(img, format='png')
    img.seek(0)
    img = img.getvalue()
    q1.put(img)

@app.route('/plotfactor', methods=['POST'])
def returnFactorGraph():

    environmentalFactors = request.form.getlist('env_factor')
    startDate = request.form.get('start')
    endDate = request.form.get('end')
    province = request.form.get('province')
    stanDev = request.form.get('sd')


    if  startDate=="" or endDate=="" or environmentalFactors==[] or province==" " or int(stanDev)<0: 
        r = {"Error": True,"msg": "Please Input all required fields"}
        return jsonify(r)
    if endDate<startDate:
        r = {"Error": True,"msg": "Ensure Start Date preceeds End Date"}
        return jsonify(r)
    if stanDev == None:
        stanDev = 0 
    q1 = Queue()
    t2 = threading.Thread(target = generateFactorGraph, args = (startDate, endDate, environmentalFactors, province, stanDev, q1))
    t2.start()
    img = q1.get()
    b64_string = base64.b64encode(img).decode('utf-8')
    return jsonify({"img": b64_string, "Error": False})

def processData(data):
   data = np.asarray(data).astype('float32')
   Scaler = MinMaxScaler()
   data = Scaler.fit_transform(data)
   return data

def classification_weighting(pred, b_acc, f1):
    weighted_pred = []
    for i in pred:
        if i == 0:
            weighted_pred.append(-(b_acc*f1))
        else:
            weighted_pred.append(b_acc*f1)
    return weighted_pred

@app.route('/predictReg', methods = ['POST'])
def forecastRegular():

    predStartDate = request.form.get('predStartDate')
    predEndDate = request.form.get('predEndDate')
    disease = request.form['diseases']
    province = request.form.get('province')

    if predStartDate == "" or predEndDate == "" or disease == "" or province == " ":
        r = {"Error": True,"msg": "Please Input all required fields"}
    elif predEndDate<predStartDate:
        r = {"Error": True,"msg": "Ensure Start Date preceeds End Date"}
    else:
        model_Sarima = load_pickle("Saved_Models/"+province+"_"+disease+"_SARIMA_Model.pickle")

        prediction = model_Sarima.get_prediction(start=pd.to_datetime(predStartDate), end=pd.to_datetime(predEndDate), dynamic=False)

        dates = prediction.predicted_mean.index.tolist()
        formatted_dates = [d.strftime('%Y-%m') for d in dates]

        predictions = prediction.predicted_mean.values.tolist()
        formatted_predictions = ["{:.0f}".format(max(0,p)) for p in predictions]

        r = {"Error": False,"dates": formatted_dates, "predictions": formatted_predictions}
    

    return jsonify(r)

@app.route('/predictXtreme', methods = ['POST'])
def forecastXtreme():

    error = False
    thresholds = [0.1537093,0.15678541,0.15174027,0.1472154,0.14336675,0.14448333]
    mlp_Acc = [67.56756756756756, 48.91891891891892, 49.45945945945946, 54.32432432432432, 51.486486486486484, 54.054054054054056]
    mlp_f1 = [0.363395225464191, 0.20253164556962028, 0.2076271186440678, 0.21939953810623555, 0.2178649237472767, 0.205607476635514]
    rf_Acc = [75.27027027027027, 84.18918918918918, 84.39189189189189, 85.4054054054054, 85.06756756756756, 85.74324324324324]
    rf_f1 = [0.14485981308411214, 0.040983606557377046, 0.03347280334728033, 0.009174311926605505, 0.008968609865470852, 0.009389671361502348]
    svm_Acc = [77.63513513513513, 76.8918918918919, 77.97297297297298, 79.5945945945946, 79.32432432432432, 80.06756756756756]
    svm_f1 = [0.29424307036247327, 0.12307692307692307, 0.0994475138121547, 0.11695906432748539, 0.11046511627906976, 0.10876132930513595]
    file = request.files['file']
    within = request.form.get('within', False)
    timeframe = request.form['timeframe']
    

    if file.filename == "" or '.csv' not in file.filename:
        r = {"Error": True, "msg": "Please Input all required fields"}
        return jsonify(r)
    else:
        data = pd.read_csv(file)
        if data.shape[0]!=1:
            r = {"Error": True, "msg": "Please Ensure file only contains a single record with all required features"}
            return jsonify(r)
    if timeframe == "":
        r = {"Error": True, "msg": "Please Input all required fields"}
        return jsonify(r)

    processed_data = processData(data.values)
    if error == False:
        if within == "on":
            for i in range(int(timeframe)):
                monthsAhead = i+1
                model_mlp = keras.models.load_model("Saved_Models/MLP_"+str(monthsAhead)+"_month/")
                model_rf = pickle.load(open("Saved_Models/rf_"+str(monthsAhead)+".sav", 'rb'))
                model_svm = pickle.load(open('Saved_Models/svm_'+str(monthsAhead)+'.sav', 'rb'))

                MLP_predictions = model_mlp.predict(processed_data)
                MLP_predictions_binary = []
                for j in MLP_predictions:
                    if j > thresholds[i]:
                        MLP_predictions_binary.append(1)
                    else:
                        MLP_predictions_binary.append(0)

                rf_predictions = model_rf.predict(processed_data)
                rf_predictions_binary = []
                for j in rf_predictions:
                    if j > 0.5:
                        rf_predictions_binary.append(1)
                    else:
                        rf_predictions_binary.append(0)

                svm_predictions = model_svm.predict(processed_data)

                svm_wegihted_pred = classification_weighting(svm_predictions, svm_Acc[i], svm_f1[i])
                rf_weighted_pred = classification_weighting(rf_predictions_binary, rf_Acc[i], rf_f1[i])
                mlp_weighted_pred = classification_weighting(MLP_predictions_binary, mlp_Acc[i], mlp_f1[i])


                if len(svm_wegihted_pred)==len(rf_weighted_pred) and len(svm_wegihted_pred)==len(mlp_weighted_pred):
                    weighted_prediction=rf_weighted_pred[0]+svm_wegihted_pred[0]+mlp_weighted_pred[0]
                    if weighted_prediction>0:
                        r = {"Error": False,"msg": "The Ensemble model predicts there will be a Dengue Fever outbreak within "+timeframe+" months"}
                        return jsonify(r)

            r = {"Error": False,"msg": "The Ensemble model predicts there will not be a Dengue Fever outbreak within "+timeframe+" months"}
            return jsonify(r)
        
        else:
            model_mlp = keras.models.load_model("Saved_Models/MLP_"+timeframe+"_month/")
            model_rf = pickle.load(open("Saved_Models/rf_"+timeframe+".sav", 'rb'))
            model_svm = pickle.load(open('Saved_Models/svm_'+timeframe+'.sav', 'rb'))

            MLP_predictions = model_mlp.predict(processed_data)
            MLP_predictions_binary = []
            for i in MLP_predictions:
                if i > thresholds[int(timeframe)-1]:
                    MLP_predictions_binary.append(1)
                else:
                    MLP_predictions_binary.append(0)

            rf_predictions = model_rf.predict(processed_data)
            rf_predictions_binary = []
            for i in rf_predictions:
                if i > 0.5:
                    rf_predictions_binary.append(1)
                else:
                    rf_predictions_binary.append(0)

            svm_predictions = model_svm.predict(processed_data)

            svm_wegihted_pred = classification_weighting(svm_predictions, svm_Acc[int(timeframe)-1], svm_f1[int(timeframe)-1])
            rf_weighted_pred = classification_weighting(rf_predictions_binary, rf_Acc[int(timeframe)-1], rf_f1[int(timeframe)-1])
            mlp_weighted_pred = classification_weighting(MLP_predictions_binary, mlp_Acc[int(timeframe)-1], mlp_f1[int(timeframe)-1])

            if len(svm_wegihted_pred)==len(rf_weighted_pred) and len(svm_wegihted_pred)==len(mlp_weighted_pred):
                weighted_prediction=rf_weighted_pred[0]+svm_wegihted_pred[0]+mlp_weighted_pred[0]
                if weighted_prediction>0:
                        r = {"Error": False,"msg": "The Ensemble model predicts there will be a Dengue Fever outbreak in "+timeframe+" months"}
                        return jsonify(r)
                else:
                        r = {"Error": False,"msg": "The Ensemble model predicts there will not be a Dengue Fever outbreak in "+timeframe+" months"}
                        return jsonify(r)



if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=5000)