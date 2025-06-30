import pandas as pd
import cx_Oracle as cx

# 오라클 접속을 위한 정보를 변수로 정의
host_name = 'localhost'
oracle_port = 1521
service_name = 'xe'
# 연결정보를 객체로 정의
connect_info = cx.makedsn(host_name, oracle_port, service_name)
# 커넥션 객체 생성
conn = cx.connect('education', '1234', connect_info)
# 쿼리문 실행을 위한 커서 생성
cursor = conn.cursor()

file_path = './resData/전국_꽃집_주소/충북 꽃집.csv'

df = pd.read_csv(file_path)
# print(df)


# 인파라미터가 있는 insert 쿼리문. ':변수명'과 같이 기술한다.
sql="""insert into flowershop_spot (idx, sigun, faclt, addr, latitude, longitude)
    values (seq_board_num.nextval, :sigun, :faclt, :addr, :latitude, :longitude) """

for i, row in df.iterrows():
    try:
        cursor.execute(sql, {
            "sigun": row['시도명'],
            "faclt": row['상호명'],
            "addr": row['지번주소'],
            "latitude": float(row['위도']),
            "longitude": float(row['경도'])
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