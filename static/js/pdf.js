function previewPdf(fileId) {
    const pdfUrl = "https://byteshare.vercel.app/download/" + fileId;
    let pdfViewer = document.getElementById("pdf_view")
    fetch(pdfUrl)
        .then(response => response.blob())
        .then(blob => {
            // Read the PDF data as a binary string
            const reader = new FileReader();
            reader.onload = () => {
                // Encode the PDF data to base64
                const base64EncodedData = btoa(reader.result);
                pdfViewer.setAttribute("data", "data:application/pdf;base64," + base64EncodedData);
            };
            reader.readAsBinaryString(blob);
        })
        .catch(error => {
            console.error('Error fetching and encoding PDF:', error);
        });
}