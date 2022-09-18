import http.client

class TossPay:
    def __init__(self):
        __conn = http.client.HTTPSConnection("api.tosspayments.com")

    def signIn(self,paymentkey,amount,orderid):
        payload = "{\"paymentKey\":\""+paymentkey+"\",\"amount\":"+amount+",\"orderId\":\""+orderid+"\"}"

        headers = {
            'Authorization': "Basic dGVzdF9za196WExrS0V5cE5BcldtbzUwblgzbG1lYXhZRzVSOg==",
            'Content-Type': "application/json"
            }
        conn.request("POST", "/v1/payments/confirm", payload, headers)
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")
