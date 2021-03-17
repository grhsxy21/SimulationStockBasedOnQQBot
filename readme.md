# 基于QQBot的模拟炒股方案
----
## 设计
- 流程设计：
	- 玩家在QQ群中，以一定的语法，选择购入、卖出股票，查看股票，账户信息，增设自选股等。
	- 在开盘时间，股票价格每隔5Min刷新一次，玩家买入卖出的操作，也仅在刷新时结算。
	- 若在下一次价格刷新时，玩家选择购入股票的价格高于实际价格，则购入成功，否则持续等待。
	- 若在下一次价格刷新时，玩家选择卖出股票的价格低于实际价格，则卖出成功，否则持续等待。
	- 无论是买入或是卖出，玩家都可以在订单未达成时查看，取消订单。取消订单的操作立即结算。
	- 买入或卖出需要按照当下市场规则，收取一定的手续费。被取消的订单不收取手续费。
- 交互设计
	- 注册：通过!#register 命令授权注册，以玩家QQ号作为uid，进行各项操作，向user_information表中插入新项即可。
	- 添加自选股:通过!#stock + #股票编号，添加自选股。此后，系统开始获取该股票信息。（玩家只能购买或卖出自选股表中的股票）
	- 买入：通过!#buy+股票编号+数量 创建购买订单
	- 卖出：通过!#sell+股票编号+数量 创建卖出订单
	- 查看: 通过!#+search+表名+属性名，查看自选股，个人账户，活跃订单等信息。
	- 取消订单：通过!#+delete+订单编号，删除订单
	- 其他
- 数据设计（表）：
	- 玩家信息(user_information)
		- qq号(user_id)
		- 昵称(user_name)
		- 账户可支配金额(free\_money_amount)
		- 账户总金额(total\_money_amount)
		- 历史总金额(history\_money_amount)
	- 股票信息(stock_information)
		- 股票编号(stock_id)
		- 最后一次刷新价格(now_price)
		- 最后一次刷新时间(flush_time)
		- 历史价格(history_price)
	- 玩家持仓(user_holdings)
		- qq号(user_id)
		- 股票编号(stock_index)
		- 持有数量(stock_amount)
		- 买入时价格(bought_price)
		- 买入订单总价格(bought\_total_price)
	- 活跃订单（alive_order）
		- qq号(user_id)
		- 活跃订单编号(alive\_order_index)
		- 订单时间(alive\_order_time)
		- 购买股票的编号(buying\_stock_index)
		- 购买股票的名称(buying\_stock_name)
		- 购买股票的数量(buying\_stock_amount)
		- 购买股票的单价(buying\_stock_price)
		- 订单总金额(order\_money_amount)
	- 全局变量(global_vars)
		- 买入手续费用(buy\_service_charge)
		- 卖出手续费用(sell\_service_charge)
		- 其他
	- 其他
- 模块设计
	- dao:与数据库交互，不考虑前端逻辑
	- domain:与dao交互，只存储信息的基本类，只有属性。
	- service：处理业务逻辑
	- controller：与前端交互，即QQBot的调用部分。

## 实现
 
- dao
	- DataBaseOperator.py
		- 类的属性
			- __connect: 与数据库的连接
			- __cursor: 游标，进行数据库操作
		- 类的方法
			- openConnect(self): 打开数据库连接，创建游标
			- getConnect(self): 获取数据库连接
			- getCursor(self): 获取游标
			- closeConnect(self): 关闭数据库连接，关闭游标
			- addRecord(self, table, record):向表table(str)中插入记录record(str)
			- deleteRecord(self, table, primary_key):从表table(str)中删除主键(id)为primary_key(str)的记录
			- changeRecord(self, table, primary_key, record):将表table(str)中主键（id)为primary_key(str)的记录，修改为record
			- searchRecord(self, table, primary_key, record):返回表table(str)中主键(id)为primary_key的记录
	- dataBaseConfig.ini
		- 数据库的配置文件
- domain
	- 包含的文件
		- 包含的类
			- 类的方法
			- 类的属性
- service
	- 包含的文件
		- 包含的类
			- 类的方法
			- 类的属性
- controller
	- 包含的文件
		- 包含的类
			- 类的方法
			- 类的属性
## TODO
- ./dao/DataBaseOperator.py，请帮助完成增删改查函数，实现后务必进行测试，保证与mysql数据库的正常交互，请不要删掉测试用例。
- ./domain/，请参考UserInformation.py定义，及readme.md的数据设计部分，完成其余4个类的代码
- ./service/Server.py，请在完成前两个需求后，设计定义在server类中的方法，包括需要的参数，功能的实现，返回值等。
## 使用框架
- python==3.7
- PyMySQL==1.0.2
