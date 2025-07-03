from flask import Flask, render_template, request, jsonify
from pie import pie_data

app = Flask(__name__)


# 예시로 메인 페이지 추가
@app.route('/')
def root():
    return 'Hello Flask Apps'

@app.route('/api/pie')
def api_pie():
    pie_plant1=pie_data("farm")
    pie_plant2=pie_data("foliage")
    return render_template('chart_result.html',
                           pie_plant1=pie_plant1,
                           pie_plant2=pie_plant2)



# 플라스크 애플리케이션 작성시 모든 함수를 정의한 후 app.run()을 실행.
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
# 만약 이 아래쪽에 함수가 정의되어 있으면 오류가 발생된다.

# 실행
# python Main.py