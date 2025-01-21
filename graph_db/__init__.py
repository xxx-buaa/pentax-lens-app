from pathlib import Path
import pandas as pd
from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, uri, user, pwd):
        self.uri = uri
        self.user = user
        self.pwd = pwd
        self.driver = None
        self.session = None

    def open(self):
        """打开数据库连接"""
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.pwd))
        self.session = self.driver.session()

    def close(self):
        """打开数据库连接"""
        if self.session:
            self.driver.close()

    def clear_existing_data(self):
        """清除现有节点和关系（初始化图数据库）"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("Graph database initialized (existing nodes and relationships cleared).")

    def load_data_from_csv(self):
        """从 CSV 文件加载数据"""
        # 获取当前脚本目录路径
        script_dir = Path(__file__).parent

        # 拼接文件路径
        lenses_data_path = script_dir  / "raw_data" / "Lens.csv"
        mounts_data_path = script_dir  / "raw_data" / "Mount.csv"
        focal_lengths_data_path = script_dir / "raw_data" / "FocalLengths.csv"

        # 读取CSV文件
        lenses_data = pd.read_csv(lenses_data_path)
        mounts_data = pd.read_csv(mounts_data_path)
        focal_lengths_data = pd.read_csv(focal_lengths_data_path)

        return lenses_data, mounts_data, focal_lengths_data

    def create_nodes_and_relationships(self, lenses_data, mounts_data, focal_lengths_data):
        with self.driver.session() as session:
            # 创建卡口和焦段节点
            for _, mount in mounts_data.iterrows():
                session.run(
                    "CREATE (m:Mount {id: $id, name: $name, description: $description})",
                    id=mount['mount_id'], name=mount['name'], description=mount['description']
                )

            for _, focal_length in focal_lengths_data.iterrows():
                session.run(
                    "CREATE (f:FocalLength {id: $id, name: $name, description: $description})",
                    id=focal_length['focal_length_id'], name=focal_length['name'], description=focal_length['description']
                )
            
            # 创建镜头节点和关系
            for _, lens in lenses_data.iterrows():
                # 创建镜头节点
                session.run(
                    "CREATE (l:Lens {id: $id, name: $name, price: $price, rating: $rating, description:$description, image_link: $image_link, lens_link: $lens_link, sharpness: $sharpness, aberration: $aberration, bokeh: $bokeh, autofocus: $autofocus, handling: $handling, value: $value})",
                    id=lens['lens_id'], name=lens['lens_name'], price=lens['price'], rating=lens['rating'], description=lens['description'], image_link=lens['image_link'], lens_link=lens['lens_link'], sharpness=lens['sharpness'], aberration=lens['aberration'], bokeh=lens['bokeh'], autofocus=lens['autofocus'], handling=lens['handling'], value=lens['value']
                )
                # 创建与卡口的关系
                session.run(
                    "MATCH (l:Lens {id: $lens_id}), (m:Mount {id: $mount_id}) "
                    "CREATE (l)-[:HAS_MOUNT]->(m)",
                    lens_id=lens['lens_id'], mount_id=lens['mount']
                )
                # 创建与焦段的关系
                session.run(
                    "MATCH (l:Lens {id: $lens_id}), (f:FocalLength {id: $focal_length_id}) "
                    "CREATE (l)-[:HAS_FOCAL_LENGTH]->(f)",
                    lens_id=lens['lens_id'], focal_length_id=lens['focal_length']
                )

    def query_lenses_with_mount_and_focal_length(self):
        """查询所有镜头及其卡口和焦段"""
        with self.driver.session() as session:
            result = session.run(
            "MATCH (l:Lens)-[:HAS_MOUNT]->(m:Mount), (l)-[:HAS_FOCAL_LENGTH]->(f:FocalLength)"
            "RETURN l.name AS lens_name, m.name AS mount_name, f.name AS focal_length"
            )
            for record in result:
                print(f"Lens: {record['lens_name']}, Mount: {record['mount_name']}, Focal Length: {record['focal_length']}")

    def query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record.data() for record in result]

# 初始化驱动程序
uri = "bolt://localhost:7687"  # 默认 URI，适用于本地数据库
username = "neo4j"  # 数据库用户名
password = "20020728"  # 数据库密码
# driver = GraphDatabase.driver(uri, auth=(username, password))

# 创建 Neo4jGraph 实例
connection = Neo4jConnection(uri, username, password)
