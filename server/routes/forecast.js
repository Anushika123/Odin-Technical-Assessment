const express = require('express');
const multer = require('multer');
const { spawn } = require('child_process');
const router = express.Router();

const upload = multer({ dest: 'fileupload/' });

router.post('/', upload.single('file'), (req, res) => {
  const python = spawn('python', ['model_run.py', req.file.path]);

  let output = '';
  python.stdout.on('data', data => {
    output += data.toString();
  });

  python.stderr.on('data', data => {
    console.error(`Python Error: ${data}`);
  });

  python.on('close', () => {
    try {
      const result = JSON.parse(output);
      res.json(result);
    } catch (error) {
      console.error('Failed to parse JSON', error);
      res.status(500).send('Model output error');
    }
  });
});

module.exports = router;
