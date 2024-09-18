const express = require('express');
const multer = require('multer');
const { exec } = require('child_process');
const path = require('path');
const app = express();

// Serve static frontend files
app.use(express.static('frontend'));

// File upload setup
const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, 'uploads/'),
  filename: (req, file, cb) => {
    if (file.fieldname === 'wordList') {
      cb(null, 'CensoredDictionary.txt');
    } else if (file.fieldname === 'video') {
      cb(null, 'input.mp4');
    }
  }
});
const upload = multer({ storage });

// Route to upload the word list and video
app.post('/upload', upload.fields([{ name: 'wordList' }, { name: 'video' }]), (req, res) => {
  const wordListPath = path.join('uploads', 'CensoredDictionary.txt');
  const videoPath = path.join('uploads', 'input.mp4');

  // Execute the bash script to run the Python script
  exec(`bash backend/process.sh ${wordListPath} ${videoPath}`, (err, stdout, stderr) => {
    if (err) {
      console.error(`Error: ${err.message}`);
      return res.status(500).send('Error processing video');
    }
    res.send('Video processed successfully');
  });
});

// Start the server
app.listen(3000, () => console.log('Server running on http://localhost:3000'));
