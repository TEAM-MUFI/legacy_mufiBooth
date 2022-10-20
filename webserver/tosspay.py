import http.client

class TossPay:
    def __init__(self):
        self.__conn = http.client.HTTPSConnection("api.tosspayments.com")

    def signIn(self,paymentkey,amount,orderid):
        payload = "{\"paymentKey\":\""+paymentkey+"\",\"amount\":"+amount+",\"orderId\":\""+orderid+"\"}"

        headers = {
            'Authorization': "Basic secreat key to base64 ver",
            'Content-Type': "application/json"
            }
        self.__conn.request("POST", "/v1/payments/confirm", payload,headers)
        res = self.__conn.getresponse()
        data = res.read()
        return data.decode("utf-8")
