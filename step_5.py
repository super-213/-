'''
第五步 添加可视化模块
增加了可视化模块
展示了从入口到最近空闲车位的路径
'''
import mysql.connector
import networkx as nx
import matplotlib.pyplot as plt

# ===================== 数据库操作模块 =====================

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host, user=self.user, password=self.password, database=self.database
            )
            self.cursor = self.conn.cursor()
            print("数据库连接成功")
        except mysql.connector.Error as err:
            print(f"连接错误: {err}")
            return None

    def close(self):
        if self.conn:
            self.conn.close()

    def execute_query(self, query, params=None):
        if self.cursor:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        return None

    def execute_update(self, query, params):
        if self.cursor:
            self.cursor.execute(query, params)
            self.conn.commit()

# ===================== 图操作模块 =====================

class GraphManager:
    def __init__(self, nodes_data, edges_data):
        self.graph = nx.Graph()
        self.add_nodes(nodes_data)
        self.add_edges(edges_data)

    def add_nodes(self, nodes_data):
        for node in nodes_data:
            slot_id, position_x, position_y, position_z, state, is_elevator = node
            self.graph.add_node(
                slot_id, position_x=position_x, position_y=position_y, position_z=position_z, 
                state=state, is_elevator=is_elevator
            )

    def add_edges(self, edges_data):
        for edge in edges_data:
            source_id, target_id, weight = edge
            self.graph.add_edge(source_id, target_id, weight=weight)

    def find_elevator_node(self):
        for node, data in self.graph.nodes(data=True):
            if data['is_elevator']:
                return node
        return None

    def find_shortest_path(self, source, target):
        try:
            path = nx.shortest_path(self.graph, source=source, target=target, weight='weight')
            distance = nx.shortest_path_length(self.graph, source=source, target=target, weight='weight')
            return path, distance
        except nx.NetworkXNoPath:
            return None, None

# ===================== 寻路逻辑模块 =====================

class PathFinder:
    def __init__(self, graph_manager):
        self.graph_manager = graph_manager

    def find_nearest_free_slot_from_elevator(self, elevator_node):
        # 筛选空闲车位
        free_slots = [node for node, data in self.graph_manager.graph.nodes(data=True) if data['state'] == 0]
        print(f"空闲车位: {free_slots}")
        
        if not free_slots:
            return None, None, None

        shortest_path = None
        min_distance = float('inf')
        nearest_slot = None

        for slot in free_slots:
            path, distance = self.graph_manager.find_shortest_path(elevator_node, slot)
            if path and distance < min_distance:
                min_distance = distance
                shortest_path = path
                nearest_slot = slot

        return shortest_path, min_distance, nearest_slot

    def find_path_to_entry(self, slot, entry_node):
        return self.graph_manager.find_shortest_path(slot, entry_node)

# ===================== 可视化模块 =====================

class VisualizeGraph:
    def __init__(self, graph, path=None):
        self.graph = graph
        self.path = path  # 从入口到车位的路径

    def draw(self):
        # 创建二维位置字典 (投影到 XY 平面)
        pos = {node[0]: (node[1]['position_x'], node[1]['position_y']) for node in self.graph.nodes(data=True)}

        # 绘制节点
        nx.draw(self.graph, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=10, font_weight='bold')

        # 绘制边权重
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)

        # 如果路径不为空，加粗路径上的边
        if self.path:
            edge_widths = [1 if (self.path[i], self.path[i+1]) in self.graph.edges else 1 for i in range(len(self.path)-1)]
            nx.draw_networkx_edges(self.graph, pos, width=edge_widths, alpha=0.7, edge_color='r')

        plt.title("停车场路径图")
        plt.show()

# ===================== 车辆管理模块 =====================

class VehicleManager:
    def __init__(self, db):
        self.db = db

    def add_vehicle(self, license_plate, car_length, car_width, car_type, slot_id):
        # 将车辆信息插入到 vehicles 表中
        query = """INSERT INTO vehicles (license_plate, car_length, car_width, car_type, slot_id) 
                   VALUES (%s, %s, %s, %s, %s)"""
        self.db.execute_update(query, (license_plate, car_length, car_width, car_type, slot_id))
        print(f"车辆 {license_plate} 已成功登记在车位 {slot_id}")

# ===================== 主控制模块 =====================

def main():
    # 数据库连接
    db = Database(host='localhost', user='root', password='12345678', database='car_park_system')
    db.connect()

    # 用户输入车辆信息
    license_plate = input("请输入车牌号：")
    car_length = float(input("请输入车长（米）："))
    car_width = float(input("请输入车宽（米）："))
    car_type = input("请输入车型（油/电/混合）：")

    # 查询节点数据和边数据
    nodes_data = db.execute_query("SELECT slot_id, position_x, position_y, position_z, state, is_elevator FROM parking_slots")
    edges_data = db.execute_query("SELECT source_id, target_id, weight FROM edge_information")

    # 创建 NetworkX 图
    G = nx.Graph()

    # 添加节点及属性
    for node in nodes_data:
        slot_id, position_x, position_y, position_z, state, is_elevator = node  # 更新解包
        G.add_node(
            slot_id, position_x=position_x, position_y=position_y, position_z=position_z, 
            state=state, is_elevator=is_elevator
        )

    # 添加边及权重
    for edge in edges_data:
        source_id, target_id, weight = edge
        G.add_edge(source_id, target_id, weight=weight)
    
    # 创建图管理对象
    graph_manager = GraphManager(nodes_data, edges_data)

    # 查找电梯节点
    elevator_node = graph_manager.find_elevator_node()
    print(f"电梯节点是否在图中：{elevator_node is not None}")

    # 寻路逻辑
    path_finder = PathFinder(graph_manager)

    # 从电梯到最近空闲车位
    path_to_slot, distance_to_slot, nearest_slot = path_finder.find_nearest_free_slot_from_elevator(elevator_node)

    if path_to_slot:
        # 获取车位坐标
        slot_data = graph_manager.graph.nodes[nearest_slot]
        x, y, z = slot_data['position_x'], slot_data['position_y'], slot_data['position_z']

        # 更新车位状态为已占用
        db.execute_update("UPDATE parking_slots SET state = 1 WHERE slot_id = %s", (nearest_slot,))

        # 添加车辆信息
        vehicle_manager = VehicleManager(db)
        vehicle_manager.add_vehicle(license_plate, car_length, car_width, car_type, nearest_slot)

        # 可视化图
        visualize = VisualizeGraph(G, path=path_to_slot)
        visualize.draw()

        print(f"从电梯到最近空闲车位的路径: {path_to_slot}")
        print(f"路径长度: {distance_to_slot}")
        print(f"空闲车位: {nearest_slot}")
        print(f"车位坐标: X={x}, Y={y}, Z={z}")

    # 从车位到入口的路径
    entry_node = 1  # 假设入口节点为 1
    path_to_entry, distance_to_entry = path_finder.find_path_to_entry(nearest_slot, entry_node)
    if path_to_entry:
        print(f"从车位到入口的路径: {path_to_entry}")
        print(f"路径长度: {distance_to_entry}")
    else:
        print("无法找到从车位到入口的路径")

    # 关闭数据库连接
    db.close()

if __name__ == "__main__":
    main()