function tossPay(name) {
	const date = new Date; 
    tossPayments.requestPayment('카드', {
        amount: purchase.totalPrice,
        orderId: date.getFullYear()+""+(date.getMonth()+1)+""+date.getDate()+""+date.getHours()+""+date.getMinutes()+""+date.getSeconds()+"MFB"+date.getMilliseconds(),
        orderName: purchase.size + "컷 포토 " + purchase.amount + "장",
        customerName: name,
        successUrl: 'http://www.muinfilm.shop/webserver/payment/success',
        failUrl: 'http://www.muinfilm.shop/webserver/payment/fail',
    })
}
