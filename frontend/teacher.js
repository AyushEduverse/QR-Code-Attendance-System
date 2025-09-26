document.addEventListener('DOMContentLoaded', () => {
    const sessionDataInput = document.getElementById('session-data');
    const startSessionBtn = document.getElementById('start-session-btn');
    const qrImage = document.getElementById('qr-image');
    const qrLink = document.getElementById('qr-link');
    const qrLinkText = document.getElementById('qr-link-text');
    const messageElement = document.getElementById('message');
    const twoColumnLayout = document.querySelector('.two-column-layout'); // Get the two-column layout container

    // Base URL for the student attendance page
    const studentAttendanceBaseUrl = window.location.origin + '/frontend/index.html';

    startSessionBtn.addEventListener('click', async () => {
        const sessionData = sessionDataInput.value.trim();
        if (!sessionData) {
            messageElement.textContent = 'Please enter session data.';
            messageElement.style.color = 'red';
            qrImage.style.display = 'none';
            qrLink.style.display = 'none';
            qrLinkText.style.display = 'none';
            twoColumnLayout.classList.remove('show-two-columns'); // Ensure single column if validation fails
            return;
        }

        messageElement.textContent = 'Starting session and generating QR code...';
        messageElement.style.color = 'blue';
        qrImage.style.display = 'none';
        qrLink.style.display = 'none';
        qrLinkText.style.display = 'none';
        twoColumnLayout.classList.remove('show-two-columns'); // Ensure single column during processing

        try {
            // First, call the backend to create the session sheet
            const createSheetResponse = await fetch('http://127.0.0.1:5000/create_session_sheet', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ session_name: sessionData }),
            });

            const createSheetResult = await createSheetResponse.json();

            if (!createSheetResponse.ok) {
                messageElement.textContent = createSheetResult.error || 'Failed to create session sheet.';
                messageElement.style.color = 'red';
                return;
            }

            // If sheet creation is successful, then generate the QR code
            const qrContentUrl = `${studentAttendanceBaseUrl}?qr_data=${encodeURIComponent(sessionData)}`;

            const generateQrResponse = await fetch(`http://127.0.0.1:5000/generate_qr?data=${encodeURIComponent(qrContentUrl)}`);
            const generateQrResult = await generateQrResponse.json();

            if (generateQrResponse.ok && generateQrResult.qr_code) {
                qrImage.src = `data:image/png;base64,${generateQrResult.qr_code}`;
                qrImage.style.display = 'block';
                qrLink.href = qrContentUrl;
                qrLink.textContent = qrContentUrl;
                qrLink.style.display = 'block';
                qrLinkText.style.display = 'block';
                messageElement.textContent = 'Session started & QR Code generated successfully! Students can scan this code.';
                messageElement.style.color = 'green';

                // Dynamically add class to trigger two-column layout animation
                twoColumnLayout.classList.add('show-two-columns');

            } else {
                messageElement.textContent = generateQrResult.error || 'Failed to generate QR code.';
                messageElement.style.color = 'red';
            }
        } catch (error) {
            console.error('Error during session creation or QR generation:', error);
            messageElement.textContent = 'Network error or server unavailable.';
            messageElement.style.color = 'red';
        }
    });
});
