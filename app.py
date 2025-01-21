from flask import Flask, render_template, jsonify, request
from graph_db import connection
from graph_db.queries import query_lenses_with_mount_and_focal_length, get_all_lenses, get_random_lens, get_graph_data

app = Flask(__name__)

# 首页路由
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# 备份路由
@app.route('/index')
def index():
    return render_template('index.html')

# 每日推荐页路由
@app.route('/recommend')
def recommend():
    return render_template('recommend.html')

# 推荐功能路由
@app.route('/recommend_data', methods=['POST'])
def recommend_data():
    """随机推荐功能的API"""
    recommend_lens = get_random_lens()
    # print('data: ', recommend_lens[0])
    return recommend_lens[0]
    
# 镜头查询页路由
@app.route('/search')
def search():
    return render_template('search.html')
    
# 问答页路由
@app.route('/qa')
def qa():
    return render_template('qa.html')
    
# 空白页路由
@app.route('/debug')
def debug():
    return render_template('debug.html')

@app.route('/dev')
def dev():
    return render_template('dev.html')
    
@app.route('/devSend', methods=['POST'])
def devSend():
    # json = request.json
    data = get_random_lens()
    # print('recv:', json)
    # print('data: ', data)
    return data

@app.route('/graph_data', methods=['POST'])
def graph_data():
    # 获取请求体中的数据
    data = request.get_json()
    selected_mounts = data.get('mounts', [])
    selected_focal_lengths = data.get('focalLengths', [])

    data = get_graph_data(selected_mounts, selected_focal_lengths)
    return jsonify(data)

if __name__ == '__main__':
    connection.open()
    connection.clear_existing_data()
    # 从 CSV 文件加载数据
    lenses_data, mounts_data, focal_lengths_data = connection.load_data_from_csv()
    # 创建节点和关系
    connection.create_nodes_and_relationships(lenses_data, mounts_data, focal_lengths_data)

    app.run(debug=True)