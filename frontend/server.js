const express  = require('express');
const path = require('path');

const PORT = process.env['FRONTEND_PORT'];
const BUILD_DIR = path.resolve(__dirname, 'build');
const server = express();

server.use(express.static(BUILD_DIR));
server.use('/', (request, response) => {
  return response.sendFile(path.resolve(BUILD_DIR, 'index.html'));
});
server.listen(PORT, () => console.log(`Express server started at http://localhost:${PORT}`));