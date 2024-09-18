document.getElementById('uploadForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const formData = new FormData();
    formData.append('wordList', document.getElementById('wordList').files[0]);
    formData.append('video', document.getElementById('video').files[0]);

    document.getElementById('status').innerText = 'Processing...';

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            document.getElementById('status').innerText = 'Video processed successfully!';
        } else {
            document.getElementById('status').innerText = 'Error processing video';
        }
    } catch (error) {
        document.getElementById('status').innerText = 'Error processing video';
    }
});
