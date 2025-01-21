from . import connection

def query_lenses_with_mount_and_focal_length():
  """查询所有镜头及其卡口和焦段"""
  query = """
  MATCH (l:Lens)-[:HAS_MOUNT]->(m:Mount), (l)-[:HAS_FOCAL_LENGTH]->(f:FocalLength)
  RETURN l.name AS lens_name, m.name AS mount_name, f.name AS focal_length
  """
  result = connection.query(query)
  lenses_info = []
  for record in result:
      lens_info = {
          "lens_name": record["lens_name"],
          "mount_name": record["mount_name"],
          "focal_length": record["focal_length"]
      }
      lenses_info.append(lens_info)
  return lenses_info

def get_all_lenses():
  """查询所有镜头"""
  query = "MATCH (l:Lens) RETURN l.name AS name, l.model AS model LIMIT 25"
  result = connection.query(query)
  return result

def get_random_lens():
  """随机推荐一个镜头"""
  query = """
  MATCH (l:Lens) 
  RETURN l.name AS name, l.description AS description, l.image_link AS image_link, l.lens_link AS lens_link
  ORDER BY rand()
  LIMIT 1
  """
  result = connection.query(query)
  return result

def get_graph_data(selected_mounts, selected_focal_lengths):
  # 将字符串列表转换为整数列表
  selected_mounts = [int(mount) for mount in selected_mounts]
  selected_focal_lengths = [int(focal_length) for focal_length in selected_focal_lengths]
  print(f'mounts: ', selected_mounts)
  print(f'focal lengths: ', selected_focal_lengths)

  # 基于选择的卡口和焦段构建查询
  query = """
  MATCH (l:Lens)-[:HAS_MOUNT]->(m:Mount), (l)-[:HAS_FOCAL_LENGTH]->(f:FocalLength)
  WHERE m.id IN $selected_mounts AND f.id IN $selected_focal_lengths
  RETURN l.name AS lens_name, m.id AS mount_id, f.id AS focal_length_id, 
  l.description AS lens_description, l.sharpness AS lens_sharpness, l.aberration AS lens_aberration, 
  l.bokeh AS lens_bokeh, l.autofocus AS lens_autofocus, l.handling AS lens_handling, l.value AS lens_value, 
  l.price AS lens_price, l.rating AS lens_rating
  """

  with connection.driver.session() as session:
    result = session.run(query, selected_mounts=selected_mounts, selected_focal_lengths=selected_focal_lengths)
    nodes = []
    edges = []
    # 用于跟踪节点ID
    node_ids = {}
    node_counter = 0

    # 从 Neo4j 获取对应的卡口和焦段名字
    mount_query = """
    UNWIND $selected_mounts AS mount_id
    MATCH (m:Mount)
    WHERE m.id = mount_id
    RETURN m.id AS mount_id, m.name AS mount_name, m.description AS mount_description
    """
    focal_length_query = """
    UNWIND $selected_focal_lengths AS focal_length_id
    MATCH (f:FocalLength)
    WHERE f.id = focal_length_id
    RETURN f.id AS focal_length_id, f.name AS focal_length_name, f.description AS focal_length_description
    """

    # 获取卡口
    mount_infos = {record['mount_id']: {
      'name': record['mount_name'],
      'description': record['mount_description'],
    } for record in session.run(mount_query, selected_mounts=selected_mounts)}
    # 获取焦段名字
    focal_length_infos = {record['focal_length_id']: {
      'name': record['focal_length_name'],
      'description': record['focal_length_description'],
    }
    for record in session.run(focal_length_query, selected_focal_lengths=selected_focal_lengths)}
    
    for record in result:
      lens_name = record['lens_name']
      lens_description = record['lens_description']
      lens_sharpness = record['lens_sharpness']
      lens_aberration = record['lens_aberration']
      lens_bokeh = record['lens_bokeh']
      lens_autofocus = record['lens_autofocus']
      lens_handling = record['lens_handling']
      lens_value = record['lens_value']
      lens_price = record['lens_price']
      lens_rating = record['lens_rating']

      mount_id = record['mount_id']
      focal_length_id = record['focal_length_id']

      # 获取对应的信息
      mount_info = mount_infos.get(mount_id, {})
      focal_length_info = focal_length_infos.get(focal_length_id, {})
      
      # 添加 Lens 节点
      if lens_name not in node_ids:
          node_ids[lens_name] = node_counter
          nodes.append({
            'id': node_counter, 
            'label': lens_name,
            'type': 'lens', # 设置类型为 'lens'
            'description': lens_description,
            'sharpness': lens_sharpness,
            'aberration': lens_aberration,
            'bokeh': lens_bokeh,
            'autofocus': lens_autofocus,
            'handling': lens_handling,
            'value': lens_value,
            'price': lens_price,
            'rating': lens_rating,
            })
          node_counter += 1
      
      # 添加 Mount 节点
      if mount_info['name'] not in node_ids:
          node_ids[mount_info['name']] = node_counter
          nodes.append({
            'id': node_counter, 
            'label': mount_info['name'],
            'type': 'mount',  # 设置类型为 'mount'
            'description': mount_info['description'],
            })
          node_counter += 1
      
      # 添加 FocalLength 节点
      if focal_length_info['name'] not in node_ids:
          node_ids[focal_length_info['name']] = node_counter
          nodes.append({
            'id': node_counter,
            'label': focal_length_info['name'],
            'type': 'focalLength',  # 设置类型为 'focalLength'
            'description': focal_length_info['description']
            })
          node_counter += 1
      
      # 添加关系
      lens_id = node_ids[lens_name]
      mount_id = node_ids[mount_info['name']]
      focal_length_id = node_ids[focal_length_info['name']]
      
      edges.append({'source': lens_id, 'target': mount_id, 'label': 'HAS_MOUNT'})
      edges.append({'source': lens_id, 'target': focal_length_id, 'label': 'HAS_FOCAL_LENGTH'})

  return {'nodes': nodes, 'edges': edges}

