from flask import Flask, render_template
from fetch_kamis_items_data import fetch_kamis_items_data
from weather import weather_data
from compare import compare_data


app = Flask(__name__)




@app.route('/')
def home():
    return "<h1>Welcome to Smart Farm Dashboard</h1>"


@app.route('/dashboard')
def dashboard():

    kamis_data = fetch_kamis_items_data()
    weather_dict = weather_data()
    compare_dict = compare_data()

    return render_template(
        'dashboard.html',
        weather_dict=weather_dict,
        ranking_data=kamis_data,
        compare_dict=compare_dict,
    )


@app.route('/map')
def map():
    return render_template('map.html')


@app.route('/flowershop')
def flowershop():
    return render_template('flowershop.html')

@app.route('/ui_test')
def ui_test():
    return render_template('ui_test2.html')



@app.errorhandler(404) 
def page_not_found(error):
    print('오류 로그:', error) # 서버 콘솔에 출력
    return "페이지가 없습니다. URL를 확인하세요.", 404


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)