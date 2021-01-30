

const HTTP_MODULE = require('http');
const PORT = 9000;
const HOSTNAME = '127.0.0.1';
const RESPONSE_ANSWER = 'Hello, World!\n';


const server = HTTP_MODULE.createServer((req, resp) => {
    resp.status = 200;
    resp.setHeader('Content-Type', 'text/plain');
    resp.end(RESPONSE_ANSWER);
});

server.listen(PORT, HOSTNAME, () => {
    console.log(`Server running at http://${HOSTNAME}:${PORT}`);
})
