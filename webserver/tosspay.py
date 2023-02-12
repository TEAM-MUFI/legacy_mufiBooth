import http.client
from keyLoad import KeyLoad

class TossPay:
    def __init__(self):
        self.__conn = http.client.HTTPSConnection("api.tosspayments.com")
        key = KeyLoad()
        self.__liveSK = "Basic " + key.getPeymentKey()

    def signIn(self,paymentkey,amount,orderid):
        payload = "{\"paymentKey\":\""+paymentkey+"\",\"amount\":"+amount+",\"orderId\":\""+orderid+"\"}"

        headers = {
                'Authorization': self.__liveSK,
                'Content-Type': "application/json"
            }
        self.__conn.request("POST", "/v1/payments/confirm", payload,headers)
        res = self.__conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

    def cancelOrder(self, paymentKey, reason):
        payload = "{\"cancelReason\":\""+ reason +"\"}"

        headers = {
                'Authorization': self.__liveSK,
                'Content-Type': "application/json"
            }

        self.__conn.request("POST", "/v1/payments/" + paymentKey + "/cancel", payload, headers)

        res = self.__conn.getresponse()
        data = res.read()

        return data.decode("utf-8")
