function generateQrCode(text, qr_id) {
    let qrModal = new bootstrap.Modal(document.getElementById("qrModal"));
    let placeholder = document.getElementById("qr_code");
    removeAllChildNodes(placeholder);
    new QRCode("qr_code", text);
    qrModal.show();

    setTimeout(() => {
        let downloadButton = document.getElementById("download_qr");
        let qrCode = document.getElementById("qr_code");
        let qrImage = qrCode.getElementsByTagName("img")[0];
        let imgSrc = qrImage.getAttribute("src");
        downloadButton.setAttribute("href", imgSrc);
        downloadButton.setAttribute("download", "qr_code_" + qr_id + ".png")
        downloadButton.enabled = true;
    }, 1000);
}

function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}

function getShareUrl(url) {
    let shareModal = new bootstrap.Modal(document.getElementById("share_link_modal"));
    let shareNoDirect = document.getElementById("share_url");
    shareNoDirect.value = url;
    shareModal.show();
}

function copyShareToClipboard() {
    let shareUrl = document.getElementById("share_url").value;
    navigator.clipboard.writeText(shareUrl)
}