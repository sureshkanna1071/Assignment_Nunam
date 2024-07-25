
from flask import Flask, request, jsonify
import streamlit as st
import pandas as pd
from flask_cors import CORS
import plotly.express as px
import json
import plotly
import mysql.connector

app = Flask(__name__)
CORS(app)

db_config = {
    'user': 'root',
    'password': 'Kingmaker@701007',
    'host': '127.0.0.1',
    'database': 'nunamassignment'
}

def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

@app.route("/")
def route():
    conn = get_db_connection()
    query = 'SELECT * FROM batterycycles'
    query2 = 'SELECT * FROM batterycyclesdetails'
    df = pd.read_sql(query, conn)
    df2 = pd.read_sql(query2, conn)

    agg_df = df.groupby('Cell_id')["Capacity_of_discharge"].max().reset_index()

    nominal_capacity = 3000

    agg_df['SoH'] = (agg_df['Capacity_of_discharge'].round(2) / nominal_capacity) * 100

    fig = px.pie(agg_df, 
             names='Cell_id', 
             values='SoH', 
             title='State of Health (SoH) by Cell ID',
             )
    
    color_map = {
        5329: '#EF553B',
        5308: '#636EFA',
    }
    
    fig1 = px.line(df2, x='Absolute_Time', y='Energy_mWh', color='Cell_id', color_discrete_map=color_map, title='Energy Over Time by Cell', labels={'Energy_mWh': 'Energy (mWh)', 'Absolute_Time': 'Time'})
    fig2 = px.scatter(df2, x='Voltage_V', y='Auxiliary_channel_TU1_T_C', color='Cell_id', color_continuous_scale= ["#636EFA", "#EF553B"], title='Temperature vs Voltage', labels={'Voltage_V': 'Voltage (V)', 'Auxiliary_channel_TU1_T_C': 'Temperature (°C)'})
    fig3 = px.histogram(df2, x='Cur_mA', nbins=50, title='Distribution of Current Values',labels={'Cur_mA': 'Current (mA)'})
    
    fig.update_traces(marker=dict(colors=['#636EFA', '#EF553B', '#00CC96', '#AB63FA']))

    # Convert Plotly figure to JSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
   

    return jsonify({'chart1': graphJSON,
        'chart2': graphJSON1,
        'chart3': graphJSON2,
        'chart4': graphJSON3})

@app.route("/test", methods=["GET"])
def test():
    return jsonify({"Message": "No Issue In The Backend"}), 200

if __name__ == '__main__':
    app.run(debug=True)