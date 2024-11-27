'''
第一步 将数据库中的数据导入到networkx中
能够实现生成停车场的图
'''
import mysql.connector
import networkx as nx
import matplotlib.pyplot as plt

# 连接到 MySQL 数据库
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='12345678',
    database='car_park_system'
)

cursor = conn.cursor()

# 查询节点数据
cursor.execute("SELECT slot_id, position_x, position_y, position_z FROM parking_slots")
nodes_data = cursor.fetchall()

# 查询边数据
cursor.execute("SELECT source_id, target_id, weight FROM edge_information")
edges_data = cursor.fetchall()

# 关闭连接
conn.close()

# 创建 NetworkX 图
G = nx.Graph()

# 添加节点及属性
for node in nodes_data:
    slot_id, position_x, position_y, position_z = node
    G.add_node(slot_id, position_x=position_x, position_y=position_y, position_z=position_z, name = slot_id)


# 添加边及权重
for edge in edges_data:
    source_id, target_id, weight = edge
    G.add_edge(source_id, target_id, weight=weight)

# 可视化图
# 创建二维位置字典 (投影到 XY 平面)
pos = {node[0]: (node[1], node[2]) for node in nodes_data}  # 使用 (position_x, position_y)

# 绘制节点
nx.draw(G, pos, with_labels=True, node_size=500)

edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.show()

