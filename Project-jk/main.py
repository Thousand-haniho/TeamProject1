from flask import Flask, render_template, request, jsonify
from weather import weather_data
from solar import solar_data
from compare import compare_data
import pandas as pd

app = Flask(__name__)


@app.route('/')
def home():
    return "<h1>Welcome to Smart Farm Dashboard</h1>"

@app.route('/dashboard')
def dashboard():
    weather_dict = weather_data()
    compare_dict = compare_data()

    return render_template(
        'dashboard.html',
        weather_dict=weather_dict,
        compare_dict=compare_dict,
    )

@app.route('/education')
def education():
    return render_template('education.html')


@app.route('/flowershop')
def flowershop():
    return render_template('flowershop.html')

@app.route('/growplant')
def growplant():
    return render_template('growplant.html')

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


df = pd.read_csv("./resData/가격_데이터.csv")
@app.route('/api/get_ranking_data', methods=["POST"])
def get_ranking_data():
    req_data = request.get_json()
    category_code = int(req_data["category_code"])
    itemname = req_data.get("itemname")  # itemname이 안 올 수도 있으니 get()

    # 1차 필터링 (부류코드)
    filtered = df[df["부류코드"] == category_code]

    # 2차 필터링 (itemname이 있으면)
    if itemname:
        filtered = filtered[filtered["itemname"] == itemname]

    # NaN → None으로 변환
    filtered = filtered.where(pd.notna(filtered), None)
    data = filtered.to_dict(orient="records")

    return jsonify(data)



@app.errorhandler(404) 
def page_not_found(error):
    print('오류 로그:', error) # 서버 콘솔에 출력
    return "페이지가 없습니다. URL를 확인하세요.", 404


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
    





