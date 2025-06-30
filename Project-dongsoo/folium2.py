import cx_Oracle as cx
import folium
from folium import FeatureGroup
from folium.plugins import MarkerCluster

# 오라클 연결
host_name = 'localhost'
oracle_port = 1521
service_name = 'xe'
connect_info = cx.makedsn(host_name, oracle_port, service_name)
conn = cx.connect('education', '1234', connect_info)
cursor = conn.cursor()

# 시군명 목록 조회
cursor.execute("SELECT DISTINCT sigun FROM flowershop_spot ORDER BY sigun ASC")
sigun_list = [r[0] for r in cursor]

# 지도 초기화
flowershop_map = folium.Map(location=[37.40, 127.38], zoom_start=10, tiles=None)
# 사용자 정의 이름으로 타일 추가
folium.TileLayer('OpenStreetMap', name='지역선택').add_to(flowershop_map)

# 시군별 그룹 + 클러스터 마커 생성
for sigun in sigun_list:
    # FeatureGroup: 시군별로 분리
    group = FeatureGroup(name=sigun, show=False)  # 기본은 off, 사용자 선택

    # MarkerCluster: 시군 내 클러스터링
    marker_cluster = MarkerCluster().add_to(group)

    # 데이터 조회
    sql = "SELECT faclt, latitude, longitude FROM flowershop_spot WHERE sigun = :sigun"
    cursor.execute(sql, sigun=sigun)

    for faclt, lat, lon in cursor:
        if lat and lon:
            try:
                lat = float(lat)
                lon = float(lon)
                folium.Marker(
                    [lat, lon],
                    popup=folium.Popup(f"<b>{faclt}</b>", max_width=250),
                    icon=folium.Icon(color="green", icon="leaf")
                ).add_to(marker_cluster)
            except ValueError:
                print(f"[오류] 좌표 변환 실패 - {faclt}")

    # FeatureGroup을 지도에 추가
    group.add_to(flowershop_map)

# 레이어 컨트롤
folium.LayerControl(collapsed=False).add_to(flowershop_map)

# 지도 저장
flowershop_map.save('./saveFiles/flowershop_map.html')
print("맵이 생성되었습니다: flowershop_map.html")
