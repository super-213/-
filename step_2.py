'''
第二步 在第一步的基础上
使用networkx中的算法 找到最短路径
然后将数据库中的车位信息进行相应修改
'''
import mysql.connector
import networkx as nx

# 创建数据库连接函数
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host='localhost',      # 数据库主机地址
            user='root',  # 数据库用户名
            password='12345678',  # 数据库密码
            database='car_park_system'   # 数据库名称
        )
        print("数据库连接成功")
        return conn
    except mysql.connector.Error as err:
        print(f"连接错误: {err}")
        return None

# 连接到数据库
conn = connect_to_database()

cursor = conn.cursor()

# 查询节点数据
cursor.execute("SELECT slot_id, position_x, position_y, position_z, state FROM parking_slots")
nodes_data = cursor.fetchall()

# 查询边数据
cursor.execute("SELECT source_id, target_id, weight FROM edge_information")
edges_data = cursor.fetchall()

# 关闭数据库连接
conn.close()

# 创建 NetworkX 图
G = nx.Graph()

# 添加节点及属性
for node in nodes_data:
    slot_id, position_x, position_y, position_z, state = node
    G.add_node(slot_id, position_x=position_x, position_y=position_y, position_z=position_z, state=state)

# 添加边及权重
for edge in edges_data:
    source_id, target_id, weight = edge
    G.add_edge(source_id, target_id, weight=weight)

# 最短路径函数
def find_nearest_free_slot(graph, start):
    # 筛选空闲车位
    free_slots = [node for node, data in graph.nodes(data=True) if data['state'] == 0]
    
    # 检查是否有空闲车位
    if not free_slots:
        return None, None, None
    
    # 使用 Dijkstra 算法寻找最近的空闲车位
    shortest_path = None
    min_distance = float('inf')
    nearest_slot = None
    
    for slot in free_slots:
        try:
            path = nx.shortest_path(graph, source=start, target=slot, weight='weight')
            distance = nx.shortest_path_length(graph, source=start, target=slot, weight='weight')
            if distance < min_distance:
                min_distance = distance
                shortest_path = path
                nearest_slot = slot  # 记录最近空闲车位的ID
        except nx.NetworkXNoPath:
            continue
    
    return shortest_path, min_distance, nearest_slot

# 测试：从入口（假设入口为节点 1）寻找最近的空闲车位
start_node = 1
path, distance, nearest_slot = find_nearest_free_slot(G, start_node)

if path:
    # 获取车位坐标
    slot_data = G.nodes[nearest_slot]
    x, y, z = slot_data['position_x'], slot_data['position_y'], slot_data['position_z']

    # 更新车位状态为已占用
    conn = connect_to_database()
    cursor = conn.cursor()

    update_query = "UPDATE parking_slots SET state = 1 WHERE slot_id = %s"
    cursor.execute(update_query, (nearest_slot,))
    conn.commit()
    cursor.close()
    conn.close()
    # 输出结果
    
    print(f"最短路径: {path}")
    print(f"最短距离: {distance}")
    print(f"最近空闲车位: {nearest_slot}")
    print(f"车位坐标: X={x}, Y={y}, Z={z}")
else:
    print("没有可用的空闲车位")