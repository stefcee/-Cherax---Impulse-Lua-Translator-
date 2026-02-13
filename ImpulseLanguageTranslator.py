"""
Impulse Language Translator
Created by: Stefc3
GitHub: github.com/Stefcee
Discord: DC.gg/chatify
Version: 1.0.0

Professional translation tool for Impulse nested JSON language files.
Supports 56 languages with smart batch processing and resume function.

Developed with AI assistance from Claude Sonnet
"""

import json
import time
import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import webbrowser
from deep_translator import GoogleTranslator

class ImpulseLanguageTranslator:
    def __init__(self, root):
        self.root = root
        self.root.title("Impulse Language Translator")
        self.root.geometry("800x920")
        self.running = False
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.target_lang_name = tk.StringVar(value="French")

        # Erweiterte Sprachenliste
        self.languages = {
            "Afrikaans": "af", "Albanian": "sq", "Arabic": "ar", "Armenian": "hy", "Azerbaijani": "az",
            "Basque": "eu", "Belarusian": "be", "Bengali": "bn", "Bulgarian": "bg", "Catalan": "ca",
            "Chinese (Simp)": "zh-CN", "Chinese (Trad)": "zh-TW", "Croatian": "hr", "Czech": "cs",
            "Danish": "da", "Dutch": "nl", "English": "en", "Estonian": "et", "Filipino": "tl",
            "Finnish": "fi", "French": "fr", "Galician": "gl", "Georgian": "ka", "German": "de",
            "Greek": "el", "Gujarati": "gu", "Haitian Creole": "ht", "Hebrew": "iw", "Hindi": "hi",
            "Hungarian": "hu", "Icelandic": "is", "Indonesian": "id", "Irish": "ga", "Italian": "it",
            "Japanese": "ja", "Kannada": "kn", "Korean": "ko", "Latvian": "lv", "Lithuanian": "lt",
            "Macedonian": "mk", "Malay": "ms", "Maltese": "mt", "Norwegian": "no", "Persian": "fa",
            "Polish": "pl", "Portuguese": "pt", "Romanian": "ro", "Russian": "ru", "Serbian": "sr",
            "Slovak": "sk", "Slovenian": "sl", "Spanish": "es", "Swahili": "sw", "Swedish": "sv",
            "Tamil": "ta", "Telugu": "te", "Thai": "th", "Turkish": "tr", "Ukrainian": "uk",
            "Urdu": "ur", "Vietnamese": "vi", "Welsh": "cy", "Yiddish": "yi"
        }

        self.setup_ui()
        self.update_ip()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="🚀 IMPULSE LANGUAGE TRANSLATOR", font=("Arial", 18, "bold")).pack(pady=5)
        ttk.Label(main_frame, text="Created by Stefc3 • 56 Languages", font=("Arial", 9, "italic")).pack(pady=5)

        # Dateiauswahl
        file_frame = ttk.LabelFrame(main_frame, text="📁 FILE SELECTION", padding="10")
        file_frame.pack(fill=tk.X, pady=5)

        ttk.Button(file_frame, text="SOURCE JSON", command=self.select_input).grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(file_frame, textvariable=self.input_path, width=55).grid(row=0, column=1, padx=5)

        ttk.Button(file_frame, text="OUTPUT PATH", command=self.select_output).grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(file_frame, textvariable=self.output_path, width=55).grid(row=1, column=1, padx=5)

        # Einstellungen
        set_frame = ttk.LabelFrame(main_frame, text="⚙️ SETTINGS", padding="10")
        set_frame.pack(fill=tk.X, pady=10)

        ttk.Label(set_frame, text="Target Language:").grid(row=0, column=0, padx=5, sticky="w")
        self.lang_combo = ttk.Combobox(set_frame, textvariable=self.target_lang_name, 
                                       values=list(self.languages.keys()), state="readonly", width=35)
        self.lang_combo.grid(row=0, column=1, padx=5, pady=5)
        self.lang_combo.bind("<<ComboboxSelected>>", self.auto_update_filename)

        ttk.Label(set_frame, text="Translation Speed:").grid(row=1, column=0, padx=5, pady=10, sticky="w")

        # Status Label VOR dem Slider erstellen
        self.status_lbl = ttk.Label(set_frame, text="Normal Speed (Recommended)", 
                                    foreground="orange", font=("Arial", 9, "bold"))
        self.status_lbl.grid(row=2, column=1, pady=2)

        self.aggro_slider = ttk.Scale(set_frame, from_=1.0, to=3.0, orient=tk.HORIZONTAL, 
                                     command=self.update_status_text)
        self.aggro_slider.set(2.0)
        self.aggro_slider.grid(row=1, column=1, sticky="ew", padx=5)

        # Progress
        self.progress_bar = ttk.Progressbar(main_frame, length=100, mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=10)

        self.log_text = tk.Text(main_frame, height=15, bg="#f5f5f5", fg="#333333", 
                               font=('Consolas', 9), wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=5)

        scrollbar = ttk.Scrollbar(self.log_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.log_text.yview)

        # Control Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10, fill=tk.X)

        self.start_btn = ttk.Button(btn_frame, text="▶ START TRANSLATION", 
                                    command=self.start_translation)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = ttk.Button(btn_frame, text="🛑 STOP", 
                                   command=self.stop_translation, state='disabled')
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        self.ip_display = ttk.Label(btn_frame, text="IP: Checking...", font=('Arial', 9, 'bold'))
        self.ip_display.pack(side=tk.LEFT, padx=15)

        ttk.Button(btn_frame, text="🔄 REFRESH IP", command=self.update_ip).pack(side=tk.LEFT, padx=5)

        # Separator
        ttk.Separator(main_frame, orient='horizontal').pack(fill=tk.X, pady=5)

        # Links Frame
        links_frame = ttk.Frame(main_frame)
        links_frame.pack(pady=5)

        ttk.Label(links_frame, text="Created by Stefc3", font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=10)

        discord_btn = ttk.Button(links_frame, text="💬 Discord", 
                                command=lambda: self.open_link("https://DC.gg/chatify"))
        discord_btn.pack(side=tk.LEFT, padx=5)

        github_btn = ttk.Button(links_frame, text="⭐ GitHub", 
                               command=lambda: self.open_link("https://github.com/Stefcee"))
        github_btn.pack(side=tk.LEFT, padx=5)

    def open_link(self, url):
        """Open URL in default browser"""
        try:
            webbrowser.open(url)
            self.log(f"🌐 Opened: {url}")
        except Exception as e:
            self.log(f"❌ Failed to open link: {e}")

    def update_status_text(self, event=None):
        val = float(self.aggro_slider.get())
        if val < 1.6:
            self.status_lbl.config(text="Slow & Safe (Recommended for large files)", foreground="green")
        elif val < 2.6:
            self.status_lbl.config(text="Normal Speed (Balanced)", foreground="orange")
        else:
            self.status_lbl.config(text="MAX Speed ⚡ (Risk of rate limit)", foreground="red")

    def auto_update_filename(self, event=None):
        if self.input_path.get():
            lang_code = self.languages.get(self.target_lang_name.get(), "fr").upper()
            base = os.path.splitext(self.input_path.get())[0]
            import re
            base = re.sub(r'_[A-Z]{2}(-[A-Z]{2})?$', '', base)
            self.output_path.set(f"{base}_{lang_code}.json")

    def select_input(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if path:
            self.input_path.set(path)
            self.auto_update_filename()

    def select_output(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", 
                                           filetypes=[("JSON files", "*.json")])
        if path:
            self.output_path.set(path)

    def update_ip(self):
        def _fetch():
            self.ip_display.config(text="IP: Loading...", foreground="gray")
            try:
                ip = requests.get('https://api.ipify.org', timeout=5).text
                self.ip_display.config(text=f"IP: {ip}", foreground="blue")
                self.log(f"✓ IP Address: {ip}")
            except Exception as e:
                self.ip_display.config(text="IP: Error", foreground="red")
                self.log(f"✗ Failed to fetch IP: {e}")
        threading.Thread(target=_fetch, daemon=True).start()

    def log(self, msg):
        self.log_text.config(state='normal')
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {msg}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def stop_translation(self):
        self.running = False
        self.log("⏸ Stopping translation... Please wait.")
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')

    def start_translation(self):
        if not self.input_path.get():
            messagebox.showwarning("Warning", "Please select a source JSON file!")
            return

        if not self.output_path.get():
            messagebox.showwarning("Warning", "Please select an output path!")
            return

        self.running = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.log("=" * 60)
        self.log("🚀 Starting translation process...")
        threading.Thread(target=self.run_translation, daemon=True).start()

    def flatten_dict(self, d, parent_key='', sep='|||'):
        """Flatten nested dictionary into flat structure for translation"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self.flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def unflatten_dict(self, d, sep='|||'):
        """Reconstruct nested dictionary from flat structure"""
        result = {}
        for key, value in d.items():
            parts = key.split(sep)
            current = result
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = value
        return result

    def run_translation(self):
        lang_name = self.target_lang_name.get()
        target_code = self.languages.get(lang_name, "fr")
        cache_file = f"cache_{target_code}_nested.json"
        separator = " ||| "

        try:
            self.log(f"📖 Loading source file: {os.path.basename(self.input_path.get())}")
            with open(self.input_path.get(), 'r', encoding='utf-8') as f:
                source_data = json.load(f)

            if "strings" not in source_data:
                messagebox.showerror("Error", "Invalid JSON structure! Missing 'strings' key.")
                self.running = False
                return

            self.log("🔄 Flattening nested structure...")
            flat_source = self.flatten_dict(source_data["strings"])

            flat_translated = {}
            if os.path.exists(cache_file):
                try:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        flat_translated = json.load(f)
                    self.log(f"💾 Resumed: {len(flat_translated)} items loaded from cache")
                except:
                    self.log("⚠ Cache file corrupted, starting fresh")

            keys_todo = [k for k in flat_source.keys() if k not in flat_translated]
            total_items = len(flat_source)

            self.log(f"📊 Total items: {total_items}")
            self.log(f"✅ Already translated: {len(flat_translated)}")
            self.log(f"⏳ Remaining: {len(keys_todo)}")
            self.log(f"🌍 Target language: {lang_name} ({target_code})")
            self.log("-" * 60)

            translator = GoogleTranslator(source='auto', target=target_code)

            i = 0
            batch_count = 0
            while i < len(keys_todo) and self.running:
                aggro = float(self.aggro_slider.get())

                if aggro < 1.6:
                    limit, delay = 0, 0.5
                elif aggro < 2.6:
                    limit, delay = 4000, 0.25
                else:
                    limit, delay = 4900, 0.1

                current_batch_keys = []
                current_batch_char_count = 0

                if limit > 0:
                    while i < len(keys_todo) and self.running:
                        k = keys_todo[i]
                        val = flat_source[k]

                        if val is None:
                            flat_translated[k] = None
                            i += 1
                            continue

                        txt = str(val)
                        if current_batch_char_count + len(txt) + 10 < limit:
                            current_batch_keys.append(k)
                            current_batch_char_count += len(txt) + 5
                            i += 1
                        else:
                            break

                    if not current_batch_keys and i < len(keys_todo):
                        current_batch_keys.append(keys_todo[i])
                        i += 1
                else:
                    if i < len(keys_todo):
                        current_batch_keys.append(keys_todo[i])
                        i += 1

                if not current_batch_keys:
                    continue

                try:
                    if len(current_batch_keys) == 1:
                        key = current_batch_keys[0]
                        val = flat_source[key]
                        if val is None or str(val).strip() == "":
                            flat_translated[key] = val
                        else:
                            flat_translated[key] = translator.translate(str(val))
                    else:
                        combined = separator.join([str(flat_source[k]) if flat_source[k] is not None else "" 
                                                  for k in current_batch_keys])
                        translated_res = translator.translate(combined)

                        if not translated_res:
                            raise Exception("Empty response from translator")

                        parts = translated_res.split(separator.strip())

                        if len(parts) == len(current_batch_keys):
                            for idx, k in enumerate(current_batch_keys):
                                flat_translated[k] = parts[idx].strip() if parts[idx].strip() else flat_source[k]
                        else:
                            self.log(f"⚠ Batch mismatch, retrying individually...")
                            for k in current_batch_keys:
                                if not self.running:
                                    break
                                val = flat_source[k]
                                if val is None:
                                    flat_translated[k] = None
                                else:
                                    flat_translated[k] = translator.translate(str(val))
                                time.sleep(0.3)

                    with open(cache_file, 'w', encoding='utf-8') as f:
                        json.dump(flat_translated, f, ensure_ascii=False, indent=4)

                    batch_count += 1
                    progress = len(flat_translated)
                    self.root.after(0, lambda p=progress: self.progress_bar.config(maximum=total_items, value=p))

                    if batch_count % 10 == 0 or progress == total_items:
                        self.log(f"⏳ Progress: {progress}/{total_items} ({int(progress/total_items*100)}%)")

                    time.sleep(delay)

                except Exception as e:
                    self.log(f"❌ Error: {str(e)}")
                    self.log(f"⏸ Paused at {len(flat_translated)}/{total_items}")
                    self.running = False
                    break

            if not self.running and len(flat_translated) < total_items:
                self.log(f"⏸ Translation paused. Progress saved to cache.")
                self.log(f"📊 {len(flat_translated)}/{total_items} items completed")
            elif len(flat_translated) >= total_items:
                final_flat = {k: flat_translated.get(k, flat_source[k]) for k in flat_source.keys()}

                self.log("🔄 Reconstructing nested structure...")
                final_strings = self.unflatten_dict(final_flat)

                final_output = {
                    "font": source_data.get("font", 0),
                    "strings": final_strings
                }

                with open(self.output_path.get(), 'w', encoding='utf-8') as f:
                    json.dump(final_output, f, ensure_ascii=False, indent=4)

                self.log("=" * 60)
                self.log(f"✅ TRANSLATION COMPLETE!")
                self.log(f"📁 Output saved: {os.path.basename(self.output_path.get())}")
                self.log(f"📊 Total items translated: {total_items}")
                self.log(f"🌍 Language: {lang_name}")

                if os.path.exists(cache_file):
                    os.remove(cache_file)
                    self.log("🗑 Cache file cleaned up")

                messagebox.showinfo("Success", f"Translation completed!\n\nFile saved to:\n{self.output_path.get()}")

        except Exception as e:
            self.log(f"❌ Critical Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred:\n\n{str(e)}")
            self.running = False

        finally:
            self.root.after(0, lambda: self.start_btn.config(state='normal'))
            self.root.after(0, lambda: self.stop_btn.config(state='disabled'))
            self.running = False


if __name__ == "__main__":
    root = tk.Tk()
    app = ImpulseLanguageTranslator(root)
    root.mainloop()
