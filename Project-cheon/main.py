from flask import Flask, render_template, request, jsonify
from price import fetch_price_all
from weather import weather_data
from solar import solar_data
from compare import compare_data


app = Flask(__name__)


@app.route('/')
def home():
    return "<h1>Welcome to Smart Farm Dashboard</h1>"

@app.route('/map')
def map():
    return render_template('map.html')


@app.route('/flowershop')
def flowershop():
    return render_template('flowershop.html')


@app.route('/ui_jk')
def ui_jk():
    weather_dict = weather_data()
    compare_dict = compare_data()

    return render_template(
        'ui_jk.html',
        weather_dict=weather_dict,
        compare_dict=compare_dict,
    )
    
@app.route('/api/weather')
def api_weather():
    region = request.args.get("region", "서울")
    weather_dict = weather_data(region)
    return jsonify(weather_dict)



@app.route('/api/solar')
def api_solar():
    region = request.args.get("region", "서울")
    solar_dict = solar_data(region)
    return jsonify(solar_dict)


@app.route('/api/get_ranking_data', methods=["POST"])
def get_ranking_data():
    req_data = request.get_json()
    category_code = req_data["category_code"]  # 바로 이게 리스트
    data = fetch_price_all(category_code)
    return jsonify(data)




@app.errorhandler(404) 
def page_not_found(error):
    print('오류 로그:', error) # 서버 콘솔에 출력
    return "페이지가 없습니다. URL를 확인하세요.", 404


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
    

from flask import jsonify
import requests
from datetime import datetime
from dotenv import load_dotenv
import os



