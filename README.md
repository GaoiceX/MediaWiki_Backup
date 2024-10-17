# MediaWiki 导出脚本

这个脚本用于导出指定MediaWiki命名空间中的所有页面，并将其保存为XML文件。

1. **导出所有页面**：使用MediaWiki API获取指定命名空间中的所有页面。
2. **处理文件名**：替换文件名中的非法字符（如 `\\/*?:"<>|` 等）为 `-`，可以根据需要修改-为其他内容（仅因为Windows的文件名限制我才这么改的）
3. **处理XML内容**：将XML内容中的 `&lt;` 转换为 `<`，将 `&gt;` 转换为 `>`。（因为抓取的XML文件内容的元素<>都会被转义，转义回来就更易读了）
4. **自动生成保存文件夹**：因为目前还是每次得从头抓取而不是自己就能增量更新，就根据wiki的域名和当前时间自动生成保存文件夹。

## 参数设置

### MediaWiki API URL

请设置脚本中的 `API_URL` 为你MediaWiki站点的API地址。例如：
```python
API_URL = "https://your-mediawiki-site/api.php"
```
### 命名空间设置

在脚本中，你可以通过 namespaces 变量指定需要导出的命名空间。默认设置为 0，1，2，你可以根据需要添加更多命名空间，具体可以参见：使用 [MediaWiki Namespaces](https://www.mediawiki.org/wiki/Help:Namespaces)

### 注意事项

记得给Python装requests模块，不然跑不动
