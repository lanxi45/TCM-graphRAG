import json
from openai import OpenAI
from neo4j import GraphDatabase

DEEPSEEK_API_KEY = "你的DeepSeek_API密钥"
NEO4J_URI = "bolt://192.168.176.128:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "你的Neo4j密码"
FILE_PATH = "xiaoer.txt"

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def extract_kg(chunk):
    prompt = f"""任务：从中医古籍文本中提取知识图谱实体与关系。
输入文本：{chunk}
约束：严格输出JSON格式，包含nodes和edges两个数组。
节点label限制：Disease, Symptom, Herb, Prescription
关系type限制：HAS_SYMPTOM, TREATS_DISEASE, CONTAINS_HERB"""
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

def write_to_neo4j(kg_data):
    with driver.session() as session:
        for node in kg_data.get("nodes", []):
            query = f"MERGE (n:{node['label']} {{name: $id}})"
            session.run(query, id=node["id"])
            
        for edge in kg_data.get("edges", []):
            query = f"""
            MATCH (a {{name: $source}})
            MATCH (b {{name: $target}})
            MERGE (a)-[r:{edge['type']}]->(b)
            """
            session.run(query, source=edge["source"], target=edge["target"])

with open(FILE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

chunks = [content[i:i+500] for i in range(0, len(content), 500)]

for chunk in chunks:
    data = extract_kg(chunk)
    write_to_neo4j(data)

driver.close()