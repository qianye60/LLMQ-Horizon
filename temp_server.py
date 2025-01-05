from pathlib import Path
import socketserver
import http.server
import signal
import os
import sys
import shutil
from datetime import datetime
from email import message_from_bytes
import re

root_path = Path(__file__).resolve().parents[0]
temp_server_dir = root_path / "temp_server"
port = 5000
host = "0.0.0.0"

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"访问日志: {self.address_string()} - {format%args}")

    def list_directory(self, path):
        try:
            entries = os.listdir(path)
        except OSError:
            self.send_error(404, "目录不存在")
            return None

        entries.sort(key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower()))
        
        rel_path = os.path.relpath(path, temp_server_dir)
        parent_path = os.path.dirname(rel_path) if rel_path != '.' else None

        with open(os.path.join(root_path, 'static/style.css'), 'r', encoding='utf-8') as f:
            css_content = f.read()

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>文件管理系统</title>
            <style>{css_content}</style>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2><i class="fas fa-folder-open"></i> 文件管理 - {rel_path if rel_path != '.' else '根目录'}</h2>
                </div>
        """

        if parent_path:
            html_content += f'<a href="/{parent_path}" class="parent-link"><i class="fas fa-arrow-left"></i> 返回上级目录</a>'

        html_content += """
        <div class="upload-form">
            <form enctype="multipart/form-data" method="post">
                <input type="file" name="file" multiple>
                <button type="submit" class="upload-btn"><i class="fas fa-upload"></i> 上传文件</button>
            </form>
        </div>
        """

        if entries:
            current_path = '/' + rel_path if rel_path != '.' else '/'
            html_content += f"""
            <form method="POST" action="{current_path}">
                <div class="actions-top">
                    <label class="select-all-label">
                        <input type="checkbox" id="select-all">
                        <span>全选</span>
                    </label>
                </div>
                <div class="file-list">
            """
            
            for name in entries:
                fullpath = os.path.join(path, name)
                displaypath = os.path.join('/' + rel_path if rel_path != '.' else '', name)
                if displaypath.startswith('//'):
                    displaypath = displaypath[1:]
                
                if os.path.isdir(fullpath):
                    html_content += f'''
                    <div class="file-item">
                        <input type="checkbox" name="files" value="{os.path.join(rel_path, name) if rel_path != '.' else name}">
                        <i class="fas fa-folder icon"></i>
                        <a href="{displaypath}" class="directory">{name}/</a>
                        <button type="button" class="rename-btn" onclick="renameItem('{os.path.join(rel_path, name) if rel_path != "." else name}', '{name}')">
                            <i class="fas fa-edit"></i>
                        </button>
                    </div>
                    '''
                else:
                    size = os.path.getsize(fullpath)
                    mtime = datetime.fromtimestamp(os.path.getmtime(fullpath)).strftime('%Y-%m-%d %H:%M:%S')
                    size_str = f"{size/1024:.1f}KB" if size > 1024 else f"{size}B"
                    
                    html_content += f'''
                    <div class="file-item">
                        <input type="checkbox" name="files" value="{os.path.join(rel_path, name) if rel_path != '.' else name}">
                        <i class="fas fa-file icon"></i>
                        <a href="{displaypath}">{name}</a>
                        <span class="size">{size_str}</span>
                        <span class="time">{mtime}</span>
                        <button type="button" class="rename-btn" onclick="renameItem('{os.path.join(rel_path, name) if rel_path != "." else name}', '{name}')">
                            <i class="fas fa-edit"></i>
                        </button>
                    </div>
                    '''
            
            html_content += """
                </div>
                <div class="actions">
                    <button type="submit" class="submit-btn" onclick="return confirm('确定要删除选中的文件/文件夹吗？');">
                        <i class="fas fa-trash"></i> 删除所选项目
                    </button>
                </div>
            </form>
            """
        else:
            html_content += '<p class="no-files">目录为空</p>'
        
        html_content += "</div></body></html>"
        
        html_content = html_content.replace('</head>', '''
            <script>
                function renameItem(path, oldName) {
                    const newName = prompt("请输入新名称:", oldName);
                    if (newName && newName !== oldName) {
                        fetch(`/rename?old=${encodeURIComponent(path)}&new=${encodeURIComponent(newName)}`, {
                            method: 'POST'
                        }).then(response => {
                            if (response.ok) {
                                window.location.reload();
                            } else {
                                alert("重命名失败");
                            }
                        });
                    }
                }

                document.addEventListener('DOMContentLoaded', function() {
                    const selectAll = document.getElementById('select-all');
                    const checkboxes = document.querySelectorAll('input[name="files"]');
                    
                    selectAll.addEventListener('change', function() {
                        checkboxes.forEach(checkbox => {
                            checkbox.checked = this.checked;
                        });
                    });

                    // 当单个复选框状态改变时，检查是否需要更新全选框状态
                    checkboxes.forEach(checkbox => {
                        checkbox.addEventListener('change', function() {
                            const allChecked = Array.from(checkboxes).every(c => c.checked);
                            const anyChecked = Array.from(checkboxes).some(c => c.checked);
                            selectAll.checked = allChecked;
                            selectAll.indeterminate = anyChecked && !allChecked;
                        });
                    });
                });
            </script>
        </head>
        ''')
        
        encoded = html_content.encode('utf-8')
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)
        return None

    def do_GET(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            return self.list_directory(path)
        return super().do_GET()

    def do_POST(self):
        if self.path.startswith('/rename'):
            from urllib.parse import parse_qs, urlparse
            query = parse_qs(urlparse(self.path).query)
            old_path = query.get('old', [''])[0]
            new_name = query.get('new', [''])[0]

            if old_path and new_name:
                try:
                    old_full_path = os.path.join(temp_server_dir, old_path)
                    new_full_path = os.path.join(os.path.dirname(old_full_path), new_name)
                    
                    if os.path.exists(new_full_path):
                        self.send_error(400, "目标文件已存在")
                        return
                    
                    os.rename(old_full_path, new_full_path)
                    self.send_response(200)
                    self.end_headers()
                    return
                except Exception as e:
                    self.send_error(500, str(e))
                    return

        elif self.headers.get('content-type', '').startswith('multipart/form-data'):
            content_type = self.headers['content-type']
            boundary = content_type.split('=')[1].encode()

            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            message = message_from_bytes(b'Content-Type: ' + content_type.encode() + b'\n\n' + post_data)
            
            current_path = os.path.relpath(self.translate_path(self.path), temp_server_dir)
            if current_path == '.':
                current_path = ''

            for part in message.walk():
                if part.get_content_maintype() == 'multipart':
                    continue

                content_disposition = str(part.get('Content-Disposition', ''))
                filename_match = re.search(r'filename="(.+?)"', content_disposition)
                if not filename_match:
                    continue
                
                filename = filename_match.group(1)
                if not filename:
                    continue

                safe_filename = os.path.basename(filename)
                if not safe_filename:
                    continue

                upload_dir = os.path.join(temp_server_dir, current_path)
                os.makedirs(upload_dir, exist_ok=True)

                filepath = os.path.join(upload_dir, safe_filename)

                try:
                    base, ext = os.path.splitext(filepath)
                    counter = 1
                    while os.path.exists(filepath):
                        filepath = f"{base}_{counter}{ext}"
                        counter += 1

                    with open(filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))
                    print(f"文件已上传: {filepath}")
                except Exception as e:
                    print(f"文件上传失败: {str(e)}")
                    continue

            self.send_response(302)
            self.send_header("Location", f"/{current_path}")
            self.end_headers()
            return

        elif not self.path.startswith('/rename'):
            current_rel_path = os.path.relpath(self.translate_path(self.path), temp_server_dir)
            if current_rel_path == '.':
                current_rel_path = ''

            length = int(self.headers.get('Content-Length', 0))
            field_data = self.rfile.read(length).decode('utf-8')

            files_to_delete = []
            for item in field_data.split('&'):
                if item.startswith('files='):
                    from urllib.parse import unquote_plus
                    filename = unquote_plus(item.split('=', 1)[1])
                    full_path = os.path.join(temp_server_dir, filename)
                    files_to_delete.append(full_path)

            deleted_parent = False
            for path in files_to_delete:
                try:
                    if os.path.exists(path):
                        if os.path.isdir(path) and (
                            os.path.abspath(os.path.join(temp_server_dir, current_rel_path)).startswith(os.path.abspath(path))
                        ):
                            deleted_parent = True
                        
                        if os.path.isdir(path):
                            shutil.rmtree(path)
                            print(f"已删除目录: {path}")
                        else:
                            os.remove(path)
                            print(f"已删除文件: {path}")
                except Exception as e:
                    print(f"删除失败: {path} - {str(e)}")

            if deleted_parent:
                parent_path = os.path.dirname(current_rel_path)
                self.send_response(302)
                self.send_header("Location", f"/{parent_path}")
                self.end_headers()
            else:
                # 否则保持在当前目录
                self.send_response(302)
                self.send_header("Location", self.path)
                self.end_headers()
        else:
            super().do_POST()

def signal_handler(signum, frame):
    """处理退出信号"""
    print("\n正在关闭服务器...")
    raise KeyboardInterrupt

class ThreadedHTTPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

def start_temp_server():
    """
    临时 HTTP 文件服务器 (多线程)。
    """
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        os.makedirs(temp_server_dir, exist_ok=True)
        os.chdir(temp_server_dir)

        handler = CustomHTTPRequestHandler
        server = ThreadedHTTPServer((host, port), handler)

        print(f"临时文件服务器已启动 (多线程)")
        print(f"监听地址: {host}")
        print(f"端口: {port}")
        print(f"目录: {temp_server_dir}")
        print("按 Ctrl+C 可以关闭服务器")

        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print("服务器已安全关闭")
        sys.exit(0)
    except PermissionError:
        print("错误：没有权限启动服务器，请检查端口权限或尝试使用sudo运行")
        sys.exit(1)
    except OSError as e:
        print(f"错误：启动服务器失败 - {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    start_temp_server()