# CSDN博客导出工具
## 功能
将个人CSDN账号的所有文章导出为Markdown文件，并将文章信息（标题、发表时间、分类、标签等）导出为JSON文件。

## 用法
```shell
python csdn_blog_export.py [options]
```

选项：
* `--username`：字符串，CSDN用户名
* `--cookie-file`：字符串，存储登录cookie的文件
* `--interval`：整数，文章爬取间隔，单位：秒，默认为2
* `--output-dir`：字符串，输出目录
