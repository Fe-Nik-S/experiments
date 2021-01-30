
const HTTP_MODULE = require('http');
const PORT = 9000;
const HOSTNAME = '127.0.0.1';


function index(req, resp) {
    resp.writeHead(200);
    resp.end('Hello, world!');
}

const server = HTTP_MODULE.createServer((req, resp) => {

    if (req.url == '/') {
        return index(req, resp)
    }

    resp.status = 404;
    resp.end(HTTP_MODULE.STATUS_CODES[404]);
});

server.listen(PORT, HOSTNAME, () => {
    console.log(`Server running at http://${HOSTNAME}:${PORT}`);
})
