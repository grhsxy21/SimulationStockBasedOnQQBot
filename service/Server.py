from dao.DataBaseOperator import DataBaseOperator
from domain.AliveOrder import AliveOrder
from domain.GlobalVars import GlobalVars
from domain.StockInformation import StockInformation
from domain.UserInformation import UserInformation
from domain.UserHoldings import UserHoldings
from datetime import datetime

begin_money = 500000


# TODO
# 返回值要改掉，应该改成str.format()方法

class Server:
    async def register(self, user_id: str, user_name: str) -> str:
        dbo = DataBaseOperator()
        if dbo.searchOne(UserInformation, UserInformation.user_id, user_id):
            return "您已注册\n" + user_id + "\n" + user_name
        else:
            user = UserInformation(user_id=user_id, user_name=user_name,
                                   free_money_amount=begin_money, total_money_amount=begin_money)
            dbo.add(user)
            return "注册成功\n" + user_id + "\n" + user_name

    async def addSelfStock(self, stock_id: str) -> str:
        dbo = DataBaseOperator()
        obj = dbo.searchOne(StockInformation, StockInformation.stock_id, stock_id)
        if obj:
            return "自选股已经被添加过\n" + obj.stock_id + "\n" + obj.stock_name
        else:
            new_obj = StockInformation(stock_id=stock_id, stock_name="暂未查询", now_price=-1, flush_time=datetime.now())
            dbo.add(new_obj)
            return "自选股添加成功" + stock_id

    async def buyStock(self, user_id: str, stock_name: str, stock_amount: int, stock_price: float) -> str:
        dbo = DataBaseOperator()
        if not dbo.searchOne(StockInformation, StockInformation.stock_name, stock_name):
            return "订单失败，请先添加自选股"
        else:
            aoi = dbo.searchAll(AliveOrder)
            if aoi:
                alive_order_index = aoi[-1].alive_order_index + 1
            else:
                alive_order_index = 1
            obj = dbo.searchOne(StockInformation, StockInformation.stock_name, stock_name)
            stock_id = obj.stock_id
            order_money_amount = stock_amount * stock_price
            free_money_amount = dbo.searchOne(UserInformation, UserInformation.user_id, user_id).free_money_amount
            if free_money_amount < order_money_amount:
                return "购买订单创建失败，可支配金额不足"
            else:
                alive_order = AliveOrder(user_id=user_id, alive_order_index=alive_order_index,
                                         alive_order_time=datetime.now(),
                                         buy_or_sell=True, stock_id=stock_id,
                                         stock_name=stock_name, stock_price=stock_price,
                                         stock_amount=stock_amount,
                                         order_money_amount=order_money_amount)
                dbo.add(alive_order)
                return "购买订单创建成功\n股票：{}\n股数：{}\n预定价格：{}\n总价格：{}\n".format(stock_name, str(stock_amount),
                                                                          str(stock_price),
                                                                          str(order_money_amount))

    # 卖出：参数alive_order是类AliveOrder的实例，在service_main中实例化;
    # 请先根据alive_order的stock_index和user_id字段，调用双字段查询方法，查询表user_holdings的stock_amount
    # 如果查询不到，返回"卖出订单创建失败，您没有购买该支股票"
    # 如果查询到，比较查询到的stock_amount和alive_order的stock_amount
    # 如果查询到的较小，返回"卖出订单创建失败，您没有足够的持仓，当前持仓为："+str(查询到玩家持仓的stock_amount)
    # 如果玩家持仓较大，调用add_record方法，将str(alive_order)插入表alive_order中，返回"卖出订单创建成功"+str(订单id)
    async def sellStock(self, user_id: str, stock_name: str, stock_amount: int, stock_price: float) -> str:
        dbo = DataBaseOperator()
        stock_amount_obj = dbo.searchOneWithTwoFields(UserHoldings, UserHoldings.stock_name, stock_name,
                                                      UserHoldings.user_id, user_id)
        if not stock_amount_obj:
            return "卖出订单创建失败，您没有购买该支股票"
        else:
            if stock_amount > stock_amount_obj.stock_amount:
                return "卖出订单创建失败，您没有足够的持仓，当前持仓为：" + str(stock_amount_obj.stock_amount)
            else:
                aoi = dbo.searchAll(AliveOrder)
                if aoi:
                    alive_order_index = aoi[-1].alive_order_index + 1
                else:
                    alive_order_index = 1
                stock_id = dbo.searchOne(StockInformation, StockInformation.stock_name, stock_name).stock_id
                alive_order = AliveOrder(user_id=user_id, alive_order_index=alive_order_index,
                                         alive_order_time=datetime.now(),
                                         buy_or_sell=False, stock_id=stock_id,
                                         stock_name=stock_name, stock_price=stock_price,
                                         stock_amount=stock_amount,
                                         order_money_amount=stock_amount * stock_price)

                dbo.add(alive_order)
                return "卖出订单创建成功\n股票：{}\n股数：{}\n预定价格：{}\n总价格：{}\n".format(stock_name, str(stock_amount),
                                                                          str(stock_price),
                                                                          str(stock_amount * stock_price))

    async def searchUserHoldings(self, user_id: str) -> str:
        dbo = DataBaseOperator()
        userHoldings = dbo.searchAllWithField(UserHoldings, UserHoldings.user_id, user_id)
        if not userHoldings:
            return "您当前没有持仓"
        else:
            rst = "您好，{},您当前的持仓情况是：\n".format(user_id)
            if type(userHoldings) == list:
                for item in userHoldings:
                    rst += str(item) + "\n"
                    rst += "-------------\n"
            else:
                rst += str(userHoldings)

            return rst

    async def searchAliveOrders(self, user_id: str) -> str:
        dbo = DataBaseOperator()
        aliveorders = dbo.searchAllWithField(AliveOrder, AliveOrder.user_id, user_id)
        if not aliveorders:
            return "您当前没有有效订单"
        else:
            rst = "您好，{},您当前的订单情况是：\n".format(user_id)
            if type(aliveorders) == list:
                for item in aliveorders:
                    rst += str(item) + "\n"
                    rst += "-------------\n"
            else:
                rst += str(aliveorders)

            return rst

    async def searchUserInformation(self, user_id: str) -> str:
        dbo = DataBaseOperator()
        user = dbo.searchAllWithField(UserInformation, UserInformation.user_id, user_id)
        if not user:
            return "您尚未注册"
        else:
            rst = "您好，{},您当前的账户信息如下：\n".format(user_id)
            if type(user) == list:
                for item in user:
                    rst += str(item) + "\n"
                    rst += "-------------\n"
            else:
                rst += str(user)
            return rst

    async def searchStock(self):
        dbo = DataBaseOperator()
        objs = dbo.searchAll(StockInformation)
        rst = "当前的股票信息为：\n"
        for obj in objs:
            rst += str(obj) + "-------------\n"
        return rst

    async def cancelOrder(self, user_id: str, alive_order_index: int) -> str:
        dbo = DataBaseOperator()
        obj = dbo.searchOneWithTwoFields(AliveOrder, AliveOrder.user_id, user_id, AliveOrder.alive_order_index,
                                         alive_order_index)
        if not obj:
            return "您要删除的订单不存在"
        else:
            dbo.deleteWithTwoFields(AliveOrder, AliveOrder.user_id, user_id, AliveOrder.alive_order_index,
                                    alive_order_index)
            return "订单{}删除成功".format(obj.alive_order_index)

    async def help(self):
        s = "使用命令:\n！注册：注册您的账户\n！添加自选股 股票编码\n！" \
            + "购买股票 股票编号 购买价格 购买数量\n" + \
            "！卖出股票 股票编号 卖出价格 卖出数量\n！查询持仓\n！查询订单\n！我的信息\n！取消订单 订单id\n！股票 " \
            + "\n感谢您的使用"
        return s


if __name__ == "__main__":
    server = Server()
    # print(server.register('906618000', 'xiaozeyu'))
    # print(server.buyStock('906618000', '114512', 500, 25))
    # print(server.sellStock('906618000', '海豚证券', 50, 10.5))
    # print(server.searchUserHoldings('906618000'))
    # print(server.searchAliveOrders('326490366'))
    # print(server.searchUserInformation('326490366'))
    print(server.cancelOrder('22', 1))
