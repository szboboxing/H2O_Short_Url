## 介绍
一款部署在Vercel,基于Python-Flask框架,开发的短网址程序.
## 演示站
[https://s.henhao.icu/](https://s.henhao.icu/)
## 需求
1. 平台: Vercel.
2. 数据库: MySql.
## 部署
[![部署](https://camo.githubusercontent.com/f209ca5cc3af7dd930b6bfc55b3d7b6a5fde1aff/68747470733a2f2f76657263656c2e636f6d2f627574746f6e)](https://vercel.com/import/project?template=https://github.com/H2Oa/H2O_Short_Url)
1. 点击上方按钮,跳转至Vercel(如果未登录,请使用GitHub账户进行快捷登录).
2. 输入名称,点击Create.  
   ![图片1](https://i.postimg.cc/hGd9D4vt/4-C22687635-EDC5-A3-F18522-F29-FDC79-FD.jpg)
3. Vercel会建立仓库并部署.  
   ![图片2](https://i.postimg.cc/6q54FnmF/1-D8-E8828-F5-CCBB2-BC495-C51293-DC5547.jpg)
4. 部署完成后,点击Go to Dashboard.  
   ![图片3](https://i.postimg.cc/28yBwdvZ/BCC07-D74-D959797-F394-CD27-E866-E1-E42.jpg)
5. 点击上方的Settings,然后在左侧选择Environment Variables,依次将HOST(数据库地址),PORT(数据库端口),USERNAME(数据库用户名),PASSWORD(数据库密码),DATABASE_NAME(数据库名称),PREFIX(表前缀,推荐填h2o_short_url_).  
   ![图片4](https://i.postimg.cc/sX3MZ5s1/16-B780016-E3541366662-A68-A368-A232-C.png)
6. 点击上方Deployments,然后选右侧Redeploy.  
   ![图片5](https://i.postimg.cc/qMgxR6Jp/C921-A6-CB-9773-4998-87-E2-CC4-A62008-D92.jpg)
7. 跳转至Overview页面等待部署完成,DOMAINS下方为网址.  
   ![图片6](https://i.postimg.cc/SNPYtX7t/7-DC0066-A53-ED67-E60-EF768-D9-F3-A04291.jpg)
## 域名
1. 点击上方的Settings,然后在左侧选择Domains,添加域名,根据提示完成解析(如果你暂时还没有域名,可忽略这一步骤,Vercel已赠送一个域名).  
   ![图片7](https://i.postimg.cc/vmFgbpKr/97-A2948-DC906-CFFDFDB00-C92-A021-CC01.jpg)
2. 在MySql管理页面中,选择core表,填写domain的值(用,分割),为你在Vercel上的域名.  
   ![图片8](https://i.postimg.cc/tJSnb70J/91-BDFA1064-DA1-BFE135797-C3-CD3-E20-C1.jpg)
## 配置
在MySql管理页面中,选择core表,title(标题),keyword(关键词),description(描述).  
![图片9](https://i.postimg.cc/52JLhf9M/B98804-F7-A072-4-C3-D-89-DA-292-E489-D7293.jpg)
## 问题
1. 问: 怎样修改数据库信息.  
   答: 参考部署中的第5步,在下方每个项的右侧选择Edit.
2. 问: Vercel赠送的域名无法访问.  
   答: 目前Vercel赠送的域名被DNS污染,暂时无法访问,需要添加自己的域名.