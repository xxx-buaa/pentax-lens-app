## 知识工程及应用课程大作业
项目结构
```plaintext
/pentax-lens-app/                         # 项目根目录
    /static/                          # 静态文件（CSS, JS, 图片等）
        /css/                         # CSS 样式文件
            style.css                 # 主样式文件
        /js/                          # JavaScript 文件
            script.js                 # 前端脚本
        /images/                      # 镜头图片等
            lens_image.jpg            # 镜头图片
    /templates/                       # HTML 模板
        index.html                    # 首页模板
        lens_detail.html              # 镜头详情页
        search_results.html           # 搜索结果页面
        base.html                     # 基础模板（包含导航、页脚等）
    /graph_db/                           # Neo4j 交互代码
        __init__.py                   # Neo4j 初始化
        lens_query.py                 # 查询 Neo4j 数据库的代码
    /scrapers/                        # 爬虫程序目录
        __init__.py                   # 爬虫模块初始化
        pentax_scraper.py             # 爬取镜头数据的爬虫程序
    requirements.txt                      # 项目依赖
    run.py                                # 启动脚本
```

1. /static/
这个文件夹存放所有静态资源（例如 CSS、JS 文件、镜头图片等），Flask 会自动提供对这些文件的访问。

2. /templates/
Flask 的模板文件夹，用于存放 HTML 页面。Flask 会使用 Jinja2 模板引擎来渲染这些页面。

index.html：主页，用于展示镜头的概览。
lens_detail.html：单个镜头的详细信息页面。
search_results.html：显示搜索结果。
base.html：基础模板，包含公共的布局（如导航栏、页脚等），其他页面将继承这个模板。

3. /app/scrapers/
爬虫模块，用于从外部网站获取镜头的数据。

pentax_scraper.py：这是爬虫代码，负责从特定的网站抓取宾得镜头的信息（例如，产品名称、焦距、光圈等）。

4. requirements.txt
项目的依赖文件，列出 Flask、Neo4j 驱动、爬虫库等所有需要安装的依赖。

5. app.py
启动 Flask 应用的入口文件。
