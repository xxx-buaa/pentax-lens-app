import pandas as pd
import os

# 定义文件路径
input_folder = os.path.join(os.getcwd(), "raw_data")
input_file = os.path.join(input_folder, "Lens.csv")
output_file = os.path.join(os.getcwd(), "Lens-Triples.csv")

# 读取数据
lens_data = pd.read_csv(input_file)

# 构建三元组
triples = []
for _, row in lens_data.iterrows():
    lens_id = row['lens_id']
    for col in lens_data.columns:
        if col != 'lens_id':  # 排除 lens_id 列
            triples.append((lens_id, col, row[col]))

# 转换为DataFrame
triples_df = pd.DataFrame(triples, columns=['lens_id', 'relation', 'entity'])

# 保存为 CSV 文件
triples_df.to_csv(output_file, index=False)

print(f"三元组数据已保存到: {output_file}")
