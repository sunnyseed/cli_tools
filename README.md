想实现一键将 obsidian 库中的 md 文档，转换为适合的英文名字，加入 front matter 后，在 hugo 博客目录中发布。
详细功能如下：
1. 使用 openfile 对话框（默认目录为：'/Users/XXX'），获取filepath，其中的 filename 可能为中文
2. 如果 filename 为中文，调用 azure 的 openai 接口，将文件名按中文含义翻译为英文（英文要简要，不超过 50 个字符）。
  比如：中文名为：'如何在 cloudflare 上部署 Hugo 构架的博客.md'
  翻译后为：'how_to_deploy_Hugo_blog_on_cloudflare.md'
3. 制作一个新的 md 格式文件，需要保留原 md 文件中的 front matter 和文件内容，在此基础上，在 front matter 中：
  - 将原始文件名（在上一个例子中是'如何在 cloudflare 上部署 Hugo 构架的博客'）作为 title
  - 如果 filepath 中包含子目录（比如：'XXX/hugo/cloudflare'），则将子目录（'hugo'和'cloudflare'）作为 categories

使用前需要设置环境变量：
```shell
AZURE_OPENAI_API_KEY = 'API KEY'
AZURE_OPENAI_API_BASE = 'BASE URL'
AZURE_OPENAI_MODEL_NAME = 'DEPLOYMENT NAME'
OB_VAULT_DIR = 'OBSIDIAN VAULT DIR'
HUGO_POST_DIR = 'HUGO POST DIR'
```