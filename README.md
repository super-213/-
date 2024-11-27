智能停车场管理系统

本项目是一个基于 Python、MySQL 和 NetworkX 的智能停车场管理系统。系统支持车辆的入库、出库管理，并利用推荐算法为不同类型的车辆（尤其是电动车）分配合适的车位。系统还提供图形可视化功能，帮助直观查看停车场的车位分布及寻路路径。

功能概述

 • 车辆管理
 • 录入新车辆
 • 更新现有车辆的车位信息
 • 车辆出库管理
 • 车位推荐算法
 • 根据车辆尺寸推荐合适的车位（小型、中型、大型）
 • 电动车或混合动力车优先推荐带充电桩的车位
 • 路径规划
 • 通过 NetworkX 图算法，从电梯节点到空闲车位计算最短路径
 • 从车位到停车场入口计算路径
 • 数据库管理
 • 使用 MySQL 存储车辆和车位信息
 • 支持 增、删、改、查 操作
 • 可视化
 • 使用 Matplotlib 显示停车场节点图及推荐路径

环境配置与依赖

安装依赖包

请确保你的环境中已安装以下依赖包：

pip install mysql-connector-python
pip install networkx
pip install matplotlib

数据库配置

 1. 确保 MySQL 数据库已安装并运行。
 2. 创建名为 car_park_system 的数据库，并设置以下表结构：

CREATE TABLE parking_slots (
    slot_id INT PRIMARY KEY,
    position_x FLOAT,
    position_y FLOAT,
    position_z FLOAT,
    state INT DEFAULT 0,      -- 0 表示空闲，1 表示已占用
    is_elevator BOOLEAN,
    is_charger BOOLEAN,
    type VARCHAR(10)           -- 小、中、大型车位
);

CREATE TABLE vehicles (
    license_plate VARCHAR(20) PRIMARY KEY,
    car_length FLOAT,
    car_width FLOAT,
    car_type VARCHAR(10),       -- 油、混合、电
    slot_id INT,
    FOREIGN KEY (slot_id) REFERENCES parking_slots(slot_id)
);

CREATE TABLE edge_information (
    source_id INT,
    target_id INT,
    weight FLOAT,
    PRIMARY KEY (source_id, target_id),
    FOREIGN KEY (source_id) REFERENCES parking_slots(slot_id),
    FOREIGN KEY (target_id) REFERENCES parking_slots(slot_id)
);


 3. 根据实际需求填充 parking_slots 和 edge_information 表。

使用说明

启动项目

 1. 运行主程序：
在终端中运行：

python main.py


 2. 操作选择：
程序启动后，会提示选择操作：
 • 1 录入车辆信息
 • 2 车辆离开
 • q 退出程序
 3. 录入车辆信息：
系统会要求输入车辆的详细信息（车牌号、尺寸、类型等），然后根据推荐算法为车辆分配车位。
 4. 车辆出库：
输入车牌号，系统会释放相应的车位并更新数据库。

推荐算法说明

 • 车位类型匹配：
根据车辆尺寸自动推荐小、中、大型车位。
 • 电动车优先充电桩：
如果车辆类型为 电动车 或 混合动力车，系统优先推荐带充电桩的空闲车位。

贡献指南

欢迎大家参与项目贡献：
 1. 提交 Pull Request
 2. 报告 Bug
 3. 提出新功能需求

许可证

本项目采用 MIT许可证。

联系方式

如有任何问题，请通过 [你的联系方式] 与我联系。

感谢你的使用和贡献！
