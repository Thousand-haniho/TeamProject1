import pandas as pd
import cx_Oracle as cx
import os

os.environ["NLS_LANG"] = ".AL32UTF8"  # 한글 깨짐 방지

# 오라클 접속을 위한 정보를 변수로 정의
host_name = '192.168.0.29'
oracle_port = 1521
service_name = 'XEPDB1'
# 연결정보를 객체로 정의
connect_info = cx.makedsn(host_name, oracle_port, service_name)
# 커넥션 객체 생성
conn = cx.connect('dongsoo', '1234', '192.168.0.29:1521/XEPDB1')

# 쿼리문 실행을 위한 커서 생성
cursor = conn.cursor()

file_path = '../backupData/plants_kor.csv'

df = pd.read_csv(file_path)
# print(df)


# 인파라미터가 있는 insert 쿼리문. ':변수명'과 같이 기술한다.
sql="""insert into plant_dict (idx, pname, height, width, breeding_season, manager_level, growth_speed, growth_temperature,
humidity)
    values (seq_board_num.nextval, :pname, :height, :width, :breeding_season, :manager_level, :growth_speed, :growth_temperature,
:humidity) """

for i, row in df.iterrows():
    try:
        cursor.execute(sql, {
            "pname" : row['식물 명'],
            "height" : float(row['성장 높이 정보']),
            "width" : float(row['성장 넓이 정보']),
            "breeding_season" : row['번식 시기 정보'],
            "manager_level" : row['관리수준 코드명'],
            "growth_speed" : row['생장속도 코드명'],
            "growth_temperature" : row['생육 온도 코드명'],
            "humidity" : row['습도 코드명']
        })
        print("1행입력.")
        # 실행에 문제가 없다면 커밋해서 실제 테이블에 적용
        conn.commit()
    except Exception as e:
        # 예외가 발생했다면 롤백 처리
        conn.rollback()
        print("insert 실행시 오류발생", e)

# DB 연결 해제
conn.close()