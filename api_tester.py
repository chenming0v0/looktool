#!/usr/bin/env python3
"""
Gmail 验证码获取工具
输入API Key，一键获取验证码
无需安装任何依赖
"""

import tkinter as tk
from tkinter import ttk, messagebox
import urllib.request
import urllib.error
import json
import threading

# ============== 配置 ==============
DEFAULT_BASE_URL = "http://localhost:8080"

class CodeFetcherApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Gmail 验证码获取工具")
        self.root.geometry("500x450")
        self.root.resizable(True, True)
        
        self.setup_ui()
    
    def setup_ui(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="Gmail 验证码获取工具", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # API地址
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=5)
        ttk.Label(url_frame, text="API地址:", width=10).pack(side=tk.LEFT)
        self.url_var = tk.StringVar(value=DEFAULT_BASE_URL)
        self.url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=40)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # API Key
        key_frame = ttk.Frame(main_frame)
        key_frame.pack(fill=tk.X, pady=5)
        ttk.Label(key_frame, text="API Key:", width=10).pack(side=tk.LEFT)
        self.key_var = tk.StringVar()
        self.key_entry = ttk.Entry(key_frame, textvariable=self.key_var, width=40)
        self.key_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 按钮区
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=20)
        
        self.fetch_btn = ttk.Button(btn_frame, text="获取最新验证码", command=self.fetch_latest_code)
        self.fetch_btn.pack(side=tk.LEFT, padx=5)
        
        self.fetch_all_btn = ttk.Button(btn_frame, text="获取所有验证码", command=self.fetch_all_codes)
        self.fetch_all_btn.pack(side=tk.LEFT, padx=5)
        
        self.copy_btn = ttk.Button(btn_frame, text="复制验证码", command=self.copy_code)
        self.copy_btn.pack(side=tk.LEFT, padx=5)
        
        # 状态
        self.status_var = tk.StringVar(value="请输入API Key后点击获取")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, foreground="gray")
        self.status_label.pack(pady=5)
        
        # 结果显示 - 验证码大字显示
        result_frame = ttk.LabelFrame(main_frame, text="验证码", padding="10")
        result_frame.pack(fill=tk.X, pady=10)
        
        self.code_var = tk.StringVar(value="------")
        self.code_label = ttk.Label(result_frame, textvariable=self.code_var, 
                                     font=("Consolas", 36, "bold"), foreground="#3B82F6")
        self.code_label.pack(pady=10)
        
        # 详细信息
        self.detail_var = tk.StringVar(value="")
        self.detail_label = ttk.Label(result_frame, textvariable=self.detail_var, 
                                       font=("Arial", 9), foreground="gray", wraplength=400)
        self.detail_label.pack()
        
        # 历史记录
        self.history_frame = ttk.LabelFrame(main_frame, text="历史记录", padding="5")
        self.history_frame.pack(fill=tk.BOTH, expand=True)
        
        self.history_text = tk.Text(self.history_frame, height=6, font=("Consolas", 9))
        self.history_text.pack(fill=tk.BOTH, expand=True)
    
    def fetch_latest_code(self):
        """获取最新验证码"""
        api_key = self.key_var.get().strip()
        if not api_key:
            messagebox.showwarning("提示", "请输入API Key")
            return
        
        self.status_var.set("正在获取...")
        self.fetch_btn.config(state=tk.DISABLED)
        
        def do_fetch():
            try:
                base_url = self.url_var.get().strip().rstrip('/')
                url = f"{base_url}/api/code/latest?api_key={api_key}"
                
                req = urllib.request.Request(url)
                req.add_header('Content-Type', 'application/json')
                
                with urllib.request.urlopen(req, timeout=30) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    self.root.after(0, lambda: self.show_result(data))
            except urllib.error.HTTPError as e:
                error_body = e.read().decode('utf-8')
                try:
                    error_data = json.loads(error_body)
                    error_msg = error_data.get('error', str(e))
                except:
                    error_msg = str(e)
                err = f"HTTP {e.code}: {error_msg}"
                self.root.after(0, lambda err=err: self.show_error(err))
            except Exception as e:
                err = str(e)
                self.root.after(0, lambda err=err: self.show_error(err))
            finally:
                self.root.after(0, lambda: self.fetch_btn.config(state=tk.NORMAL))
        
        threading.Thread(target=do_fetch, daemon=True).start()
    
    def fetch_all_codes(self):
        """获取所有验证码"""
        api_key = self.key_var.get().strip()
        if not api_key:
            messagebox.showwarning("提示", "请输入API Key")
            return
        
        self.status_var.set("正在获取...")
        self.fetch_all_btn.config(state=tk.DISABLED)
        
        def do_fetch():
            try:
                base_url = self.url_var.get().strip().rstrip('/')
                url = f"{base_url}/api/codes?api_key={api_key}"
                
                req = urllib.request.Request(url)
                req.add_header('Content-Type', 'application/json')
                
                with urllib.request.urlopen(req, timeout=30) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    self.root.after(0, lambda: self.show_all_codes(data))
            except urllib.error.HTTPError as e:
                error_body = e.read().decode('utf-8')
                try:
                    error_data = json.loads(error_body)
                    error_msg = error_data.get('error', str(e))
                except:
                    error_msg = str(e)
                err = f"HTTP {e.code}: {error_msg}"
                self.root.after(0, lambda err=err: self.show_error(err))
            except Exception as e:
                err = str(e)
                self.root.after(0, lambda err=err: self.show_error(err))
            finally:
                self.root.after(0, lambda: self.fetch_all_btn.config(state=tk.NORMAL))
        
        threading.Thread(target=do_fetch, daemon=True).start()
    
    def show_result(self, data: dict):
        """显示结果"""
        code = data.get('code', '')
        subject = data.get('subject', '')
        sender = data.get('from', '')
        time_str = data.get('date', '')
        
        if code:
            self.code_var.set(code)
            self.code_label.config(foreground="#10B981")  # 绿色
            self.status_var.set("获取成功!")
            self.detail_var.set(f"来自: {sender}\n主题: {subject}\n时间: {time_str}")
            
            # 添加到历史
            self.history_text.insert("1.0", f"[{time_str}] {code} - {subject[:30]}...\n")
        else:
            self.code_var.set("无验证码")
            self.code_label.config(foreground="#F59E0B")  # 黄色
            self.status_var.set("未找到验证码")
            self.detail_var.set("")
    
    def show_all_codes(self, data: dict):
        """显示所有验证码"""
        messages = data.get('messages', [])
        
        if messages:
            # 显示第一个
            first = messages[0]
            self.code_var.set(first.get('code', '无'))
            self.code_label.config(foreground="#10B981")
            self.status_var.set(f"获取成功! 共 {len(messages)} 条")
            self.detail_var.set(f"来自: {first.get('from', '')}\n主题: {first.get('subject', '')}")
            
            # 清空并添加所有到历史
            self.history_text.delete("1.0", tk.END)
            for msg in messages:
                code = msg.get('code', '无')
                subject = msg.get('subject', '')[:40]
                date = msg.get('date', '')
                self.history_text.insert(tk.END, f"[{date}] {code} - {subject}\n")
        else:
            self.code_var.set("无验证码")
            self.code_label.config(foreground="#F59E0B")
            self.status_var.set("未找到验证码")
            self.detail_var.set("")
    
    def show_error(self, error: str):
        """显示错误"""
        self.code_var.set("错误")
        self.code_label.config(foreground="#EF4444")  # 红色
        self.status_var.set(f"错误: {error}")
        self.detail_var.set("")
    
    def copy_code(self):
        """复制验证码到剪贴板"""
        code = self.code_var.get()
        if code and code not in ["------", "无验证码", "错误"]:
            self.root.clipboard_clear()
            self.root.clipboard_append(code)
            self.status_var.set("已复制到剪贴板!")
        else:
            messagebox.showinfo("提示", "没有可复制的验证码")

def main():
    root = tk.Tk()
    app = CodeFetcherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
