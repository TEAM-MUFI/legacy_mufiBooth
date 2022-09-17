function tossPay() {
    tossPayments.requestPayment('카드', {
        amount: purchase.totalPrice,
        orderId: 'gss_1tIvCXayv-LBXP0R4',
        orderName: purchase.size + "컷 포토 " + purchase.amount + "장",
        customerName: '이름Test',
        successUrl: 'http://localhost:3000/new3',
        failUrl: 'http://localhost:3000/new2',
    })
}