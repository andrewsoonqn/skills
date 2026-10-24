// Static file server with byte-range support, so videos play in iOS Safari.
// Usage: node serve.mjs <root> <port>
import { createServer } from 'node:http'
import { createReadStream, statSync } from 'node:fs'
import { extname, join, normalize, resolve } from 'node:path'

const root = resolve(process.argv[2] ?? '.')
const port = Number(process.argv[3] ?? 8091)
const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.gif': 'image/gif', '.svg': 'image/svg+xml', '.mp4': 'video/mp4', '.webm': 'video/webm' }

createServer((req, res) => {
  const path = normalize(decodeURIComponent(new URL(req.url, 'http://x').pathname))
  const file = join(root, path.endsWith('/') ? path + 'index.html' : path)
  if (!file.startsWith(root)) return res.writeHead(403).end()
  let size
  try { const st = statSync(file); if (!st.isFile()) throw 0; size = st.size } catch { return res.writeHead(404).end('Not found') }
  const headers = { 'Content-Type': types[extname(file).toLowerCase()] ?? 'application/octet-stream', 'Accept-Ranges': 'bytes', 'Cache-Control': 'no-cache' }
  const range = /^bytes=(\d*)-(\d*)$/.exec(req.headers.range ?? '')
  if (range) {
    const start = range[1] === '' ? Math.max(0, size - Number(range[2])) : Number(range[1])
    const end = range[1] !== '' && range[2] !== '' ? Math.min(Number(range[2]), size - 1) : size - 1
    if (start > end || start >= size) return res.writeHead(416, { 'Content-Range': `bytes */${size}` }).end()
    res.writeHead(206, { ...headers, 'Content-Range': `bytes ${start}-${end}/${size}`, 'Content-Length': end - start + 1 })
    return req.method === 'HEAD' ? res.end() : createReadStream(file, { start, end }).pipe(res)
  }
  res.writeHead(200, { ...headers, 'Content-Length': size })
  req.method === 'HEAD' ? res.end() : createReadStream(file).pipe(res)
}).listen(port, '127.0.0.1', () => console.log(`serving ${root} on 127.0.0.1:${port}`))
