import pandas as pd  
from neo4j import GraphDatabase  
import time  

NEO4J_URI="bolt://localhost:7687"  
NEO4J_USERNAME="neo4j"  
NEO4J_PASSWORD="YH1223725"  
NEO4J_DATABASE="neo4j"  
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))  

def batched_import(statement, df, batch_size=1000):  
    total = len(df)  
    start_s = time.time()  
    for start in range(0,total, batch_size):  
        batch = df.iloc[start: min(start+batch_size,total)]  
        result = driver.execute_query("UNWIND $rows AS value " + statement,  
                                      rows=batch.to_dict('records'),  
                                      database_=NEO4J_DATABASE)  
        print(result.summary.counters)  
    print(f'{total} rows in { time.time() - start_s} s.')  
    return total  

statements = """  
create constraint chunk_id if not exists for (c:__Chunk__) require c.id is unique;  
create constraint document_id if not exists for (d:__Document__) require d.id is unique;  
create constraint entity_id if not exists for (c:__Community__) require c.community is unique;  
create constraint entity_id if not exists for (e:__Entity__) require e.id is unique;  
create constraint entity_title if not exists for (e:__Entity__) require e.name is unique;  
create constraint entity_title if not exists for (e:__Covariate__) require e.title is unique;  
create constraint related_id if not exists for ()-[rel:RELATED]->() require rel.id is unique;  
""".split(";")  
for statement in statements:  
    if len((statement or "").strip()) > 0:  
        print(statement)  
        driver.execute_query(statement)  

doc_df = pd.read_parquet(f'D:/GISERR/graduate_study/pytorch/graphrag/ragtest/output/create_final_documents.parquet', columns=["id", "title"])  
print(doc_df.head(2)  )


# import documents  
statement = """  
MERGE (d:__Document__ {id:value.id})  
SET d += value {.title}
"""  
batched_import(statement, doc_df)  


text_df = pd.read_parquet(f'D:/GISERR/graduate_study/pytorch/graphrag/ragtest/output/create_final_text_units.parquet',  
                          columns=["id","text","n_tokens","document_ids"])  
text_df.head(2)  

