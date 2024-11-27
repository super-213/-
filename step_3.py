'''
第三步 添加了电梯节点
寻路算法设计为先寻找从电梯到最近的空闲车位
再从最近的空闲车位到入口
显示从入口到最近的空闲车位的路径
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

# 查询节点数据，包括电梯标识
cursor.execute("SELECT slot_id, position_x, position_y, position_z, state, is_elevator FROM parking_slots")
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
    slot_id, position_x, position_y, position_z, state, is_elevator = node
    G.add_node(slot_id, position_x=position_x, position_y=position_y, position_z=position_z, state=state, is_elevator=is_elevator)

# 添加边到图中
for edge in edges_data:
    source_id, target_id, weight = edge
    G.add_edge(source_id, target_id, weight=weight)

# 查找电梯节点
elevator_node = None
for node, data in G.nodes(data=True):
    if data['is_elevator']:  # 判断是否为电梯
        elevator_node = node
        break

# 确保电梯节点在图中
print(f"电梯节点是否在图中：{elevator_node is not None}")

# 最短路径函数（从电梯到最近空闲车位）
def find_nearest_free_slot_from_elevator(graph, elevator):
    # 筛选空闲车位
    free_slots = [node for node, data in graph.nodes(data=True) if data['state'] == 0]
    print(f"空闲车位: {free_slots}")
    
    if not free_slots:
        return None, None, None
    
    # 使用 Dijkstra 算法寻找最近的空闲车位
    shortest_path = None
    min_distance = float('inf')
    nearest_slot = None
    
    for slot in free_slots:
        try:
            path = nx.shortest_path(graph, source=elevator, target=slot, weight='weight')
            distance = nx.shortest_path_length(graph, source=elevator, target=slot, weight='weight')
            if distance < min_distance:
                min_distance = distance
                shortest_path = path
                nearest_slot = slot
        except nx.NetworkXNoPath:
            continue
    
    return shortest_path, min_distance, nearest_slot


# 入口到车位的路径函数
def find_path_to_entry(graph, slot, entry):
    try:
        path = nx.shortest_path(graph, source=slot, target=entry, weight='weight')
        distance = nx.shortest_path_length(graph, source=slot, target=entry, weight='weight')
        return path, distance
    except nx.NetworkXNoPath:
        return None, None

# 测试：指定入口节点（将入口节点设为整数类型）
entry_node = 1  # 假设车辆从入口1进入停车场，使用整数类型

# 从电梯到最近空闲车位
path_to_slot, distance_to_slot, nearest_slot = find_nearest_free_slot_from_elevator(G, elevator_node)

if path_to_slot:
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
    
    print(f"从电梯到最近空闲车位的路径: {path_to_slot}")
    print(f"路径长度: {distance_to_slot}")
    print(f"空闲车位: {nearest_slot}")
    print(f"车位坐标: X={x}, Y={y}, Z={z}")
    

# 确保入口和车位节点都在图中
if nearest_slot in G.nodes and entry_node in G.nodes:
    path_to_entry, distance_to_entry = find_path_to_entry(G, nearest_slot, entry_node)
    if path_to_entry:
        print(f"从车位到入口的路径: {path_to_entry}")
        print(f"路径长度: {distance_to_entry}")
    else:
        print("无法找到从车位到入口的路径")
else:
    print("车位或入口节点未在图中")

