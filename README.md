



<div align="center">
  <img src="./浙江大学-logo.svg" alt="浙江大学 Logo" width="200"/>
</div>

### 作业要求：

- 使用Java/Python 制作Web应用

- 可选RESTful api。用api形式则需要有一个客户端程序，语言自选(java, js, python, shell)

- 使用数据库存储数据

- 有增、删、改、查的操作 

### 项目思路

  RESTful API中，API服务器（Flask应用）负责处理客户端发来的HTTP请求，并返回JSON数据。选择了来自开源天气预报平台openweather提供的免费api接口。用户由前端输入查询天气的查询数据，后端调用api并反馈给前端，数据库存储查询数据。

### 技术栈

-	**后端**：使用Flask框架来构建RESTful API，提供天气查询和CRUD功能。

- **前端**：使用JavaScript编写一个网页客户端（HTML+CSS+JavaScript），通过AJAX或fetch请求来与Flask API交互。

-	**数据库**：使用SQLite或其他数据库（如PostgreSQL、MySQL）来存储天气数据。

### 部署

  最后使用docker对代码和依赖项打包，确保在其他环境中能够运行。
