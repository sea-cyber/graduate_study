from neo4j import GraphDatabase
from googletrans import Translator
 
# 配置Neo4j连接
uri = "bolt://localhost:7687"  # 替换为你的Neo4j实例的URI
user = "neo4j"                 # 替换为你的Neo4j用户名
password = "YH1223725"          # 替换为你的Neo4j密码
 
# 创建Neo4j驱动程序实例
driver = GraphDatabase.driver(uri, auth=(user, password))
 
# 创建翻译器实例
translator = Translator()
 
# 定义查询函数
def translate_and_update_entities(tx):
    # 获取所有entity标签的节点及其英文name属性
    for record in tx.run("MATCH (e:__Entity__) RETURN e.id AS id, e.name AS name"):
        entity_id = record["id"]
        english_name = record["name"].lower()
        
        # 使用翻译器将英文name翻译成中文
        translation = translator.translate(english_name, src='en', dest='zh-cn')
        chinese_name = translation.text
 
        # 更新节点的name属性为中文
        tx.run("MATCH (e:__Entity__ {id: $id}) SET e.name_zh = $chinese_name", id=entity_id, chinese_name=chinese_name)
        print("Chinese entity_name: ",english_name,"                        English entity_name:    ",chinese_name)
# 使用with语句管理驱动程序的生命周期
with driver.session() as session:
    # 执行查询并更新节点
    session.write_transaction(translate_and_update_entities)
 
# 关闭驱动程序
driver.close()



