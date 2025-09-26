// Frontend JavaScript for QR scanning and attendance submission

const attendanceForm = document.getElementById('attendance-form');
const nameInput = document.getElementById('name');
const rollNumberInput = document.getElementById('roll-number');
const qrDataInput = document.getElementById('qr-data');
const messageElement = document.getElementById('message');
// Removed sessionsAttendedDisplay and sessionCountSpan
const attendanceAnimation = document.getElementById('attendance-animation');
const sessionEndMessage = document.getElementById('session-end-message');

// Function to get query parameters from the URL
function getQueryParams() {
    const params = {};
    window.location.search.substring(1).split('&').forEach(pair => {
        const [key, value] = pair.split('=').map(decodeURIComponent);
        params[key] = value;
    });
    return params;
}

// Populate qrData from URL query parameter
const queryParams = getQueryParams();
if (queryParams.qr_data) {
    qrDataInput.value = queryParams.qr_data;
    messageElement.textContent = `Session: ${queryParams.qr_data}. Please enter your details.`;
    messageElement.style.color = 'green';
} else {
    messageElement.textContent = 'No session data found. Please scan a QR code from the teacher page.';
    messageElement.style.color = 'red';
}

attendanceForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const name = nameInput.value;
    const rollNumber = rollNumberInput.value;
    const qrData = qrDataInput.value; // This is now the session name

    if (!name || !rollNumber || !qrData) {
        messageElement.textContent = 'Please fill in all fields.';
        messageElement.style.color = 'red';
        return;
    }

    messageElement.textContent = 'Submitting attendance...';
    messageElement.style.color = 'blue';
    attendanceForm.querySelector('button[type="submit"]').disabled = true; // Disable button to prevent double submission

    try {
        const response = await fetch('http://127.0.0.1:5000/submit_attendance', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, roll_number: rollNumber, qr_data: qrData }),
        });

        const result = await response.json();

        if (response.ok) {
            if (result.is_duplicate) {
                messageElement.textContent = 'Attendance already marked for this session.';
                messageElement.style.color = 'orange';
            } else {
                // Successful new attendance
                attendanceForm.classList.add('slide-up-fade-out');
                setTimeout(() => {
                    attendanceForm.style.display = 'none';
                    attendanceForm.classList.remove('slide-up-fade-out'); // Clean up class

                    attendanceAnimation.style.display = 'block';
                    messageElement.textContent = 'Attendance submitted successfully!';
                    messageElement.style.color = 'green';

                    setTimeout(() => {
                        attendanceAnimation.classList.add('fade-out');
                        messageElement.classList.add('fade-out');

                        setTimeout(() => {
                            attendanceAnimation.style.display = 'none';
                            messageElement.style.display = 'none';
                            attendanceAnimation.classList.remove('fade-out');
                            messageElement.classList.remove('fade-out');

                            sessionEndMessage.style.display = 'block';
                            // Optional: Redirect after a few seconds or reset for next attendance
                            // setTimeout(() => { window.location.reload(); }, 3000); 
                        }, 2000); // Wait for fade-out to complete
                    }, 1500); // Show animation for a bit before fading out

                }, 500); // Wait for form slide-up to start
            }
        } else {
            messageElement.textContent = result.error || 'An error occurred during submission.';
            messageElement.style.color = 'red';
        }
    } catch (error) {
        console.error('Error submitting attendance:', error);
        messageElement.textContent = 'Network error or server unavailable.';
        messageElement.style.color = 'red';
    } finally {
        attendanceForm.querySelector('button[type="submit"]').disabled = false;
    }
});
