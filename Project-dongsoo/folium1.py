# 모듈 임포트
import cx_Oracle as cx
import folium

# 오라클 연결 및 커서생성
host_name = 'localhost'
oracle_port = 1521
service_name = 'xe'
connect_info = cx.makedsn(host_name, oracle_port, service_name)
conn = cx.connect('education', '1234', connect_info)
cursor = conn.cursor()

# 폴리엄으로 지도 생성
edu_map = folium.Map(location=[37.47, 126.88], zoom_start=15)
edu_map.save('./saveFiles/edu_map.html')

# 지도 데이터를 오름차순 정렬해서 인출
sql = "select * from plant_edu_spot order by idx asc"
cursor.execute(sql)
for rs in cursor:
    idx = rs[0]
    faclt = rs[1]
    addr = rs[2]
    latitude = rs[3]
    longitude = rs[4]
    # 교육기관 정보를 통해 마커 생성
    folium.Marker(
        location=[latitude, longitude],
        popup=folium.Popup(f"<b>{faclt}</b>", max_width=250),
        icon=folium.Icon(color='blue', icon='star')  # 'home', 'star', 'leaf', 'info-sign' 등
    ).add_to(edu_map)
    print(faclt, latitude, longitude)

# 마커가 포함된 지도 생성 및 저장
edu_map.save('./saveFiles/edu_map_marker.html')
print("맵이 생성되었습니다.")