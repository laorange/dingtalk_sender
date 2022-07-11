# 钉钉批量通知程序

## 开发背景

现有一份Excel：待通知的人员名单，类似于：

| **张三** |
| -------- |
| **李四** |
| **王五** |

拟通过这份名单，在钉钉上，根据账号的实名信息找到他们，并以**公告**的形式批量通知他们。

## 初次使用

1. 您可以通过[**克隆代码**](https://github.com/laorange/dingtalk_sender/archive/refs/heads/master.zip)或[**下载发行版**](https://github.com/laorange/dingtalk_sender/releases)来获取程序。

2. 您需要在您的钉钉组织申请开发者权限，可参考这篇[文档](https://open.dingtalk.com/document/dashboard/become-a-dingtalk-developer)。

3. 然后，您需要创建及发布**企业内部应用-H5微应用**，可参考这篇[文档](https://open.dingtalk.com/document/org/microapplication-creation-and-release-process)。

4. 此时，您会来到如下图所示的页面，您会得到在后续步骤中需要用到的三个参数（在图中以红笔遮盖的地方）：

   1. `AgentId`

   1. `AppKey`

   1. `AppSecret`

5. 然后您需要在下图中以绿色框住的**权限管理**中，为您的应用添加下列权限：

   + 通讯录管理：
     + 通讯录部门信息读权限
     + 成员信息读权限
     + 通讯录部门成员读权限
   + 公告
     + 钉钉公告管理权限

6. 然后您可以开始运行程序了，需要以此填写**步骤4**中获取到的三个参数、您想发送的消息、以及您要发送的对象姓名。

   > 注：在输入发送的对象时，可直接选中Excel的一列，在程序中直接粘贴。

![demo.jpeg](assets\demo.jpeg)



## 使用第一次后

每一次完成配置信息后（那三个参数），程序都会在其**所在文件夹**下生成一个名为`settings.json`的文件，您可以使用**记事本**、**Sublime**等文本编辑器来打开它。

在这个配置文件中，会记录您上一次录入的信息，以方便快速使用。

如果您的钉钉部门信息有变，请删除这个文件，这样程序就会在下一次运行时重新加载部门信息。

## 继续开发

在 `utils\dingTalkOperator.py` 中封装了一系列对钉钉接口的操作方法，可为后来的项目提供参考。