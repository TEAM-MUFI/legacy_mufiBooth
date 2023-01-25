const qrious = require("qrious");

function generateQR(pin, element) {
    if (!/^\d{4}/.test(pin)) {
        return;
    }
    const qr = new qrious({
        element: element,
        value: pin,
        size: 200
    })
}