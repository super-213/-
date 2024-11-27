import networkx as nx
import matplotlib.pyplot as plt

# 创建带权图
G = nx.Graph()

# 添加节点（表示城市或位置）
cities = ['A', 'B', 'C', 'D']
G.add_nodes_from(cities)

# 添加带权边（表示道路及距离）
G.add_edge('A', 'B', weight=10)
G.add_edge('B', 'C', weight=15)
G.add_edge('C', 'D', weight=5)
G.add_edge('A', 'D', weight=20)

# 绘制地图图形
pos = nx.spring_layout(G)  # 布局算法
nx.draw(G, pos, with_labels=True, node_size=700, node_color='skyblue')

# 添加权重标签
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.show()