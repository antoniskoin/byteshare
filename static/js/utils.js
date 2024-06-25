function setFooter() {
    let currentYear = new Date().getFullYear();
    let footer = document.getElementById("footer");
    footer.textContent = `ByteShare © ${currentYear}`;
}
