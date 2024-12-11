# rag+llm+graph
## 1,zaure无法继续安装
伊马祖尔打开 2020年4月3日·annatisch编辑
編輯从版本 5.0.0 开始，此 azure 元包已弃用，无法再安装。您仍然可以根据需要使用以下方式安装此包的特定旧版本:
```
    pip install azure=-4.0.8
```
这一决定背后的理由是:，Azure 世界中的 SDK 被分成每个服务一个包。这导致 PyP! 上发布了 200 多个包。每个包都有自己的版本(即使它们都遵循 semver)。
使用一个独特的 azure 元包有很多挑战:
。在进行常规发布时，元包的版本控制不能遵循semver，否则它会很快达到疯狂的数字。
。对该包进行松散的版本控制(即不遵循semver)并允许在没有主要版本更新的情况下进行重大更改无济于事，并且会造成比任何事情
都更多的混乱。
超过 200 个软件包的安装时间是个问题，尤其是因为在同一环境中不太可能没有人需要一次性安装所有可能的服务。这种情况在低带
宽连接或物联网设备上甚至是不可能的

## 2 graphrag无文件夹
1、最新版本存在一些问题

        pip insrall graphrag==0.4
2、初始化仓库，构建ragtest/intput/book.txt 

3、初始化仓库生成配置文件

      python -m graphrag.index --init --root ./graphtest
        
4、设置api，llm
```
    llm:
      api_key: ${GRAPHRAG_API_KEY}
      type: openai_chat
      model: glm-4-air    # 修改LLM
      api_base: https://open.bigmodel.cn/api/paas/v4    # 修改请求URL

    embeddings:
      async_mode: threaded
      llm:
        api_key: ${GRAPHRAG_API_KEY}
        type: openai_embedding
        model: embedding-3    # 修改向量模型
        api_base: https://open.bigmodel.cn/api/paas/v4    # 修改请求URL
```
5、构建索引
```
      graphrag index --root ./ragtest
```
6、构建查询
```
      graphrag query --root ./ragtest --method global --query "这场暴雨和城市建筑有什么关系"     
```
## 3 googletrans翻译库使，直接安装会出错，需要安装下列版本
```
      pip install googletrans==4.0.0-rc1
```

## 4 neo4j apoc安装
```
      NEO4J_HIOME/labs/apoc-5.25.1-core.jar # 已经存在apoc核心库
```
拷贝到

      NEO4J_HIOME/plugins  # 修改config文件

```
      dbms.security.procedures.unrestricted=apoc.*,algo.*

      dbms.security.procedures.allowlist=apoc.coll.*,apoc.load.*,gds.*
```