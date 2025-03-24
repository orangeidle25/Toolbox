import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import tkinter.simpledialog as simpledialog
import time
import random
import string
import requests
import qrcode
from PIL import Image, ImageTk
import datetime
import winsound

class ToolboxApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Toolbox v1.0.0")
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.geometry("900x700")

        try:
            self.iconbitmap("app_logo.ico")
        except Exception:
            try:
                img = tk.PhotoImage(file="app_logo.png")
                self.call('wm', 'iconphoto', self._w, img)
            except Exception:
                pass

        # Create the notebook (tab container)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=1, fill="both")

        # Create frames (tabs) for each tool
        self.timer_frame = ttk.Frame(self.notebook)
        self.stopwatch_frame = ttk.Frame(self.notebook)
        self.calculator_frame = ttk.Frame(self.notebook)
        self.notepad_frame = ttk.Frame(self.notebook)
        self.password_frame = ttk.Frame(self.notebook)
        self.unit_converter_frame = ttk.Frame(self.notebook)
        self.currency_converter_frame = ttk.Frame(self.notebook)
        self.qr_generator_frame = ttk.Frame(self.notebook)
        self.alarm_frame = ttk.Frame(self.notebook)

        # Add tabs to the notebook, with labels
        self.notebook.add(self.timer_frame, text="Timer")
        self.notebook.add(self.stopwatch_frame, text="Stopwatch")
        self.notebook.add(self.calculator_frame, text="Calculator")
        self.notebook.add(self.notepad_frame, text="Notepad")
        self.notebook.add(self.password_frame, text="PassGen")
        self.notebook.add(self.unit_converter_frame, text="Unit Converter")
        self.notebook.add(self.currency_converter_frame, text="Currency Converter")
        self.notebook.add(self.qr_generator_frame, text="QR Generator")
        self.notebook.add(self.alarm_frame, text="Alarm")

        # Build each tool's UI
        self._build_timer_ui()
        self._build_stopwatch_ui()
        self._build_calculator_ui()
        self._build_notepad_ui()
        self._build_password_generator_ui()
        self._build_unit_converter_ui()
        self._build_currency_converter_ui()
        self._build_qr_generator_ui()
        self._build_alarm_ui()

    # ---------------------- TIMER FUNCTIONS ---------------------- #
    def _build_timer_ui(self):
        self.timer_label = ttk.Label(self.timer_frame, text="00:00:00", font=("Helvetica", 48))
        self.timer_label.pack(pady=20)

        entry_frame = ttk.Frame(self.timer_frame)
        entry_frame.pack(pady=10)
        self.hours_var = tk.StringVar(value="0")
        self.minutes_var = tk.StringVar(value="0")
        self.seconds_var = tk.StringVar(value="0")
        ttk.Label(entry_frame, text="Hours:").grid(row=0, column=0, padx=5)
        ttk.Entry(entry_frame, width=3, textvariable=self.hours_var).grid(row=0, column=1, padx=5)
        ttk.Label(entry_frame, text="Min:").grid(row=0, column=2, padx=5)
        ttk.Entry(entry_frame, width=3, textvariable=self.minutes_var).grid(row=0, column=3, padx=5)
        ttk.Label(entry_frame, text="Sec:").grid(row=0, column=4, padx=5)
        ttk.Entry(entry_frame, width=3, textvariable=self.seconds_var).grid(row=0, column=5, padx=5)

        controls_frame = ttk.Frame(self.timer_frame)
        controls_frame.pack(pady=10)
        self.timer_start_button = ttk.Button(controls_frame, text="Start Timer", command=self.start_timer)
        self.timer_start_button.grid(row=0, column=0, padx=5)
        self.timer_stop_button = ttk.Button(controls_frame, text="Stop Timer", command=self.stop_timer)
        self.timer_stop_button.grid(row=0, column=1, padx=5)
        self.timer_reset_button = ttk.Button(controls_frame, text="Reset Timer", command=self.reset_timer)
        self.timer_reset_button.grid(row=0, column=2, padx=5)

        self.timer_running = False
        self.timer_remaining = 0

    def start_timer(self):
        if not self.timer_running:
            try:
                hours = int(self.hours_var.get())
                minutes = int(self.minutes_var.get())
                seconds = int(self.seconds_var.get())
            except ValueError:
                return
            self.timer_remaining = hours * 3600 + minutes * 60 + seconds
            if self.timer_remaining > 0:
                self.timer_running = True
                self._run_timer()

    def _run_timer(self):
        if self.timer_running and self.timer_remaining >= 0:
            hrs = self.timer_remaining // 3600
            mins = (self.timer_remaining % 3600) // 60
            secs = self.timer_remaining % 60
            self.timer_label.config(text=f"{hrs:02d}:{mins:02d}:{secs:02d}")
            if self.timer_remaining == 0:
                self.timer_running = False
                messagebox.showinfo("Time's Up", "The timer has ended!")
                return
            else:
                self.timer_remaining -= 1
                self.after(1000, self._run_timer)

    def stop_timer(self):
        self.timer_running = False

    def reset_timer(self):
        self.stop_timer()
        self.timer_label.config(text="00:00:00")

    # ---------------------- STOPWATCH FUNCTIONS ---------------------- #
    def _build_stopwatch_ui(self):
        self.stopwatch_label = ttk.Label(self.stopwatch_frame, text="00:00:00.00", font=("Helvetica", 48))
        self.stopwatch_label.pack(pady=20)
        self.lap_listbox = tk.Listbox(self.stopwatch_frame, height=6)
        self.lap_listbox.pack(pady=10, fill="both", expand=True)

        controls_frame = ttk.Frame(self.stopwatch_frame)
        controls_frame.pack(pady=10)
        self.stopwatch_running = False
        self.stopwatch_start_time = None
        self.elapsed_time = 0.0
        self.lap_times = []

        self.sw_start_button = ttk.Button(controls_frame, text="Start", command=self.start_stopwatch)
        self.sw_start_button.grid(row=0, column=0, padx=5)
        self.sw_stop_button = ttk.Button(controls_frame, text="Stop", command=self.stop_stopwatch)
        self.sw_stop_button.grid(row=0, column=1, padx=5)
        self.sw_reset_button = ttk.Button(controls_frame, text="Reset", command=self.reset_stopwatch)
        self.sw_reset_button.grid(row=0, column=2, padx=5)
        self.lap_button = ttk.Button(controls_frame, text="Lap", command=self.record_lap)
        self.lap_button.grid(row=0, column=3, padx=5)

    def start_stopwatch(self):
        if not self.stopwatch_running:
            self.stopwatch_start_time = time.perf_counter() - self.elapsed_time
            self.stopwatch_running = True
            self._update_stopwatch()

    def _update_stopwatch(self):
        if self.stopwatch_running:
            self.elapsed_time = time.perf_counter() - self.stopwatch_start_time
            mins, secs = divmod(self.elapsed_time, 60)
            hours, mins = divmod(mins, 60)
            self.stopwatch_label.config(text=f"{int(hours):02d}:{int(mins):02d}:{secs:05.2f}")
            self.after(10, self._update_stopwatch)

    def stop_stopwatch(self):
        self.stopwatch_running = False

    def reset_stopwatch(self):
        self.stop_stopwatch()
        self.elapsed_time = 0.0
        self.stopwatch_label.config(text="00:00:00.00")
        self.lap_listbox.delete(0, tk.END)
        self.lap_times = []

    def record_lap(self):
        if self.stopwatch_running:
            lap_time = self.elapsed_time
            self.lap_times.append(lap_time)
            lap_number = len(self.lap_times)
            mins, secs = divmod(lap_time, 60)
            hours, mins = divmod(mins, 60)
            formatted_time = f"{int(hours):02d}:{int(mins):02d}:{secs:05.2f}"
            self.lap_listbox.insert(tk.END, f"Lap {lap_number}: {formatted_time}")

    # ---------------------- CALCULATOR FUNCTIONS ---------------------- #
    def _build_calculator_ui(self):
        self.calc_expression = ""
        self.calc_entry = ttk.Entry(self.calculator_frame, font=("Helvetica", 24), justify="right")
        self.calc_entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "=", "+"],
            ["C"]
        ]

        for r, row in enumerate(buttons, start=1):
            for c, char in enumerate(row):
                button = ttk.Button(self.calculator_frame, text=char, command=lambda ch=char: self.on_calc_button_click(ch))
                button.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")

        for i in range(len(buttons) + 1):
            self.calculator_frame.rowconfigure(i, weight=1)
        for j in range(4):
            self.calculator_frame.columnconfigure(j, weight=1)

    def on_calc_button_click(self, char):
        if char == "=":
            try:
                result = eval(self.calc_expression)
                self.calc_expression = str(result)
            except Exception:
                self.calc_expression = "Error"
            self.calc_entry.delete(0, tk.END)
            self.calc_entry.insert(tk.END, self.calc_expression)
        elif char == "C":
            self.calc_expression = ""
            self.calc_entry.delete(0, tk.END)
        else:
            self.calc_expression += str(char)
            self.calc_entry.delete(0, tk.END)
            self.calc_entry.insert(tk.END, self.calc_expression)

    # ---------------------- ENHANCED NOTEPAD FUNCTIONS ---------------------- #
    def _build_notepad_ui(self):
        # Main text widget with default font
        self.notepad_text = tk.Text(self.notepad_frame, wrap="word", font=("Helvetica", 12))
        self.notepad_text.pack(expand=1, fill="both", padx=5, pady=5)

        # File operation buttons
        file_frame = ttk.Frame(self.notepad_frame)
        file_frame.pack(fill="x", padx=5, pady=5)
        open_btn = ttk.Button(file_frame, text="Open", command=self.open_notepad_file)
        open_btn.pack(side="left", padx=5)
        save_btn = ttk.Button(file_frame, text="Save", command=self.save_notepad_file)
        save_btn.pack(side="left", padx=5)
        clear_btn = ttk.Button(file_frame, text="Clear", command=lambda: self.notepad_text.delete(1.0, tk.END))
        clear_btn.pack(side="left", padx=5)

        # Text styling controls: Bold, Italic, and Font Size Adjustment.
        style_frame = ttk.Frame(self.notepad_frame)
        style_frame.pack(fill="x", padx=5, pady=5)
        bold_btn = ttk.Button(style_frame, text="Bold", command=self.apply_bold)
        bold_btn.pack(side="left", padx=5)
        italic_btn = ttk.Button(style_frame, text="Italic", command=self.apply_italic)
        italic_btn.pack(side="left", padx=5)
        ttk.Label(style_frame, text="Font Size:").pack(side="left", padx=5)
        self.font_size_var = tk.IntVar(value=12)
        font_spinbox = ttk.Spinbox(style_frame, from_=8, to=48, width=5, textvariable=self.font_size_var, command=self.update_font_size)
        font_spinbox.pack(side="left", padx=5)

        # Configure text tags for bold and italic styles.
        self.notepad_text.tag_configure("bold", font=("Helvetica", 12, "bold"))
        self.notepad_text.tag_configure("italic", font=("Helvetica", 12, "italic"))

    def open_notepad_file(self):
        file_path = filedialog.askopenfilename(title="Open Text File", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                self.notepad_text.delete(1.0, tk.END)
                self.notepad_text.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file:\n{str(e)}")

    def save_notepad_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", title="Save Text File", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                content = self.notepad_text.get(1.0, tk.END)
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(content)
                messagebox.showinfo("Success", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file:\n{str(e)}")

    def apply_bold(self):
        try:
            current_tags = self.notepad_text.tag_names("sel.first")
            if "bold" in current_tags:
                self.notepad_text.tag_remove("bold", "sel.first", "sel.last")
            else:
                self.notepad_text.tag_add("bold", "sel.first", "sel.last")
        except tk.TclError:
            messagebox.showinfo("Info", "Please select text to apply bold formatting.")

    def apply_italic(self):
        try:
            current_tags = self.notepad_text.tag_names("sel.first")
            if "italic" in current_tags:
                self.notepad_text.tag_remove("italic", "sel.first", "sel.last")
            else:
                self.notepad_text.tag_add("italic", "sel.first", "sel.last")
        except tk.TclError:
            messagebox.showinfo("Info", "Please select text to apply italic formatting.")

    def update_font_size(self):
        new_size = self.font_size_var.get()
        self.notepad_text.config(font=("Helvetica", new_size))
        self.notepad_text.tag_configure("bold", font=("Helvetica", new_size, "bold"))
        self.notepad_text.tag_configure("italic", font=("Helvetica", new_size, "italic"))

    # ---------------------- PASSWORD GENERATOR FUNCTIONS ---------------------- #
    def _build_password_generator_ui(self):
        instruction_label = ttk.Label(self.password_frame, text="Generate a secure password:")
        instruction_label.pack(pady=5)
        options_frame = ttk.Frame(self.password_frame)
        options_frame.pack(pady=5)
        ttk.Label(options_frame, text="Length:").grid(row=0, column=0, padx=5)
        self.pw_length_var = tk.IntVar(value=12)
        self.length_spinbox = tk.Spinbox(options_frame, from_=6, to=64, width=5, textvariable=self.pw_length_var)
        self.length_spinbox.grid(row=0, column=1, padx=5)
        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Uppercase", variable=self.use_upper).grid(row=1, column=0, padx=5, sticky="w")
        ttk.Checkbutton(options_frame, text="Lowercase", variable=self.use_lower).grid(row=1, column=1, padx=5, sticky="w")
        ttk.Checkbutton(options_frame, text="Digits", variable=self.use_digits).grid(row=2, column=0, padx=5, sticky="w")
        ttk.Checkbutton(options_frame, text="Symbols", variable=self.use_symbols).grid(row=2, column=1, padx=5, sticky="w")
        generate_button = ttk.Button(self.password_frame, text="Generate", command=self.generate_password)
        generate_button.pack(pady=10)
        self.generated_password = tk.StringVar()
        password_entry = ttk.Entry(self.password_frame, textvariable=self.generated_password, font=("Helvetica", 16), justify="center")
        password_entry.pack(pady=5, fill="x", padx=20)
        copy_button = ttk.Button(self.password_frame, text="Copy to Clipboard", command=self.copy_password)
        copy_button.pack(pady=5)

    def generate_password(self):
        length = self.pw_length_var.get()
        char_pool = ""
        if self.use_upper.get():
            char_pool += string.ascii_uppercase
        if self.use_lower.get():
            char_pool += string.ascii_lowercase
        if self.use_digits.get():
            char_pool += string.digits
        if self.use_symbols.get():
            char_pool += string.punctuation
        if not char_pool:
            messagebox.showerror("Error", "Select at least one character type!")
            return
        password = ''.join(random.choice(char_pool) for _ in range(length))
        self.generated_password.set(password)

    def copy_password(self):
        password = self.generated_password.get()
        if password:
            self.clipboard_clear()
            self.clipboard_append(password)
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No password to copy!")

    # ---------------------- UNIT CONVERTER FUNCTIONS ---------------------- #
    def _build_unit_converter_ui(self):
        tk.Label(self.unit_converter_frame, text="Unit Converter", font=("Helvetica", 16)).pack(pady=10)
        type_frame = ttk.Frame(self.unit_converter_frame)
        type_frame.pack(pady=5)
        ttk.Label(type_frame, text="Conversion Type:").pack(side="left", padx=5)
        self.conversion_types = ["Temperature", "Length", "Weight"]
        self.conversion_type = tk.StringVar()
        self.conversion_type.set(self.conversion_types[0])
        self.type_combo = ttk.Combobox(type_frame, textvariable=self.conversion_type, values=self.conversion_types, state="readonly")
        self.type_combo.pack(side="left", padx=5)
        self.type_combo.bind("<<ComboboxSelected>>", self.update_unit_options)
        units_frame = ttk.Frame(self.unit_converter_frame)
        units_frame.pack(pady=5)
        ttk.Label(units_frame, text="From:").grid(row=0, column=0, padx=5, pady=2)
        self.from_unit = tk.StringVar()
        self.from_combo = ttk.Combobox(units_frame, textvariable=self.from_unit, state="readonly")
        self.from_combo.grid(row=0, column=1, padx=5, pady=2)
        ttk.Label(units_frame, text="To:").grid(row=1, column=0, padx=5, pady=2)
        self.to_unit = tk.StringVar()
        self.to_combo = ttk.Combobox(units_frame, textvariable=self.to_unit, state="readonly")
        self.to_combo.grid(row=1, column=1, padx=5, pady=2)
        input_frame = ttk.Frame(self.unit_converter_frame)
        input_frame.pack(pady=5)
        ttk.Label(input_frame, text="Value:").pack(side="left", padx=5)
        self.unit_input = ttk.Entry(input_frame, width=10)
        self.unit_input.pack(side="left", padx=5)
        convert_button = ttk.Button(self.unit_converter_frame, text="Convert", command=self.convert_units)
        convert_button.pack(pady=5)
        self.unit_result_label = ttk.Label(self.unit_converter_frame, text="Result: ", font=("Helvetica", 14))
        self.unit_result_label.pack(pady=5)
        self.update_unit_options()

    def update_unit_options(self, event=None):
        conversion_type = self.conversion_type.get()
        if conversion_type == "Temperature":
            units = ["Celsius", "Fahrenheit"]
        elif conversion_type == "Length":
            units = ["Meters", "Feet"]
        elif conversion_type == "Weight":
            units = ["Kilograms", "Pounds"]
        else:
            units = []
        self.from_combo['values'] = units
        self.to_combo['values'] = units
        if units:
            self.from_unit.set(units[0])
            self.to_unit.set(units[1] if len(units) > 1 else units[0])

    def convert_units(self):
        try:
            value = float(self.unit_input.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid input value!")
            return
        from_u = self.from_unit.get()
        to_u = self.to_unit.get()
        conversion_type = self.conversion_type.get()
        result = value
        if conversion_type == "Temperature":
            if from_u == to_u:
                result = value
            elif from_u == "Celsius" and to_u == "Fahrenheit":
                result = value * 9/5 + 32
            elif from_u == "Fahrenheit" and to_u == "Celsius":
                result = (value - 32) * 5/9
        elif conversion_type == "Length":
            if from_u == to_u:
                result = value
            elif from_u == "Meters" and to_u == "Feet":
                result = value * 3.28084
            elif from_u == "Feet" and to_u == "Meters":
                result = value / 3.28084
        elif conversion_type == "Weight":
            if from_u == to_u:
                result = value
            elif from_u == "Kilograms" and to_u == "Pounds":
                result = value * 2.20462
            elif from_u == "Pounds" and to_u == "Kilograms":
                result = value / 2.20462
        self.unit_result_label.config(text=f"Result: {result:.2f}")

    # ---------------------- CURRENCY CONVERTER FUNCTIONS ---------------------- #
    def _build_currency_converter_ui(self):
        tk.Label(self.currency_converter_frame, text="Currency Converter", font=("Helvetica", 16)).pack(pady=10)
        amount_frame = ttk.Frame(self.currency_converter_frame)
        amount_frame.pack(pady=5)
        ttk.Label(amount_frame, text="Amount:").pack(side="left", padx=5)
        self.currency_amount = ttk.Entry(amount_frame, width=10)
        self.currency_amount.pack(side="left", padx=5)
        currency_frame = ttk.Frame(self.currency_converter_frame)
        currency_frame.pack(pady=5)
        ttk.Label(currency_frame, text="From:").grid(row=0, column=0, padx=5, pady=2)
        self.from_currency = tk.StringVar()
        self.from_currency_combo = ttk.Combobox(currency_frame, textvariable=self.from_currency, state="readonly")
        self.from_currency_combo['values'] = ["USD", "EUR", "GBP", "JPY", "INR"]
        self.from_currency_combo.grid(row=0, column=1, padx=5, pady=2)
        self.from_currency.set("USD")
        ttk.Label(currency_frame, text="To:").grid(row=1, column=0, padx=5, pady=2)
        self.to_currency = tk.StringVar()
        self.to_currency_combo = ttk.Combobox(currency_frame, textvariable=self.to_currency, state="readonly")
        self.to_currency_combo['values'] = ["USD", "EUR", "GBP", "JPY", "INR"]
        self.to_currency_combo.grid(row=1, column=1, padx=5, pady=2)
        self.to_currency.set("EUR")
        convert_button = ttk.Button(self.currency_converter_frame, text="Convert", command=self.convert_currency)
        convert_button.pack(pady=5)
        self.currency_result_label = ttk.Label(self.currency_converter_frame, text="Result: ", font=("Helvetica", 14))
        self.currency_result_label.pack(pady=5)

    def convert_currency(self):
        try:
            amount = float(self.currency_amount.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid amount!")
            return
        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()
        url = f"https://api.exchangerate.host/convert?from={from_curr}&to={to_curr}&amount={amount}"
        try:
            response = requests.get(url)
            data = response.json()
            if data.get('success', True):
                result = data.get('result', None)
                if result is not None:
                    self.currency_result_label.config(text=f"Result: {result:.2f} {to_curr}")
                else:
                    messagebox.showerror("Error", "Conversion failed! Possible reasons: API not found, no internet.")
            else:
                messagebox.showerror("Error", "Conversion failed! Possible reasons: API not found, no internet.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve conversion rate: {str(e)}")

    # ---------------------- QR CODE GENERATOR FUNCTIONS ---------------------- #
    def _build_qr_generator_ui(self):
        instruction = ttk.Label(self.qr_generator_frame, text="Enter text or URL for QR Code:", font=("Helvetica", 14))
        instruction.pack(pady=10)
        self.qr_input = ttk.Entry(self.qr_generator_frame, font=("Helvetica", 12))
        self.qr_input.pack(pady=5, fill="x", padx=20)
        generate_btn = ttk.Button(self.qr_generator_frame, text="Generate QR Code", command=self.generate_qr)
        generate_btn.pack(pady=10)
        self.qr_label = ttk.Label(self.qr_generator_frame)
        self.qr_label.pack(pady=10)
        save_btn = ttk.Button(self.qr_generator_frame, text="Save QR Code", command=self.save_qr)
        save_btn.pack(pady=5)

    def generate_qr(self):
        data = self.qr_input.get()
        if not data:
            messagebox.showerror("Error", "Please enter text or URL for QR Code.")
            return
        try:
            self.qr_image = qrcode.make(data)
            self.tk_qr_image = ImageTk.PhotoImage(self.qr_image)
            self.qr_label.config(image=self.tk_qr_image)
        except Exception as e:
            messagebox.showerror("Error", f"Error generating QR Code: {str(e)}")

    def save_qr(self):
        if hasattr(self, 'qr_image'):
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
            if file_path:
                try:
                    self.qr_image.save(file_path)
                    messagebox.showinfo("Saved", "QR Code saved successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Error saving QR Code: {str(e)}")
        else:
            messagebox.showerror("Error", "No QR Code generated to save.")

    # ---------------------- ALARM FUNCTIONS ---------------------- #
    def _build_alarm_ui(self):
        tk.Label(self.alarm_frame, text="Set Alarm", font=("Helvetica", 16)).pack(pady=10)
        time_frame = ttk.Frame(self.alarm_frame)
        time_frame.pack(pady=5)
        ttk.Label(time_frame, text="Hour (0-23):").grid(row=0, column=0, padx=5, pady=2)
        ttk.Label(time_frame, text="Min:").grid(row=0, column=2, padx=5, pady=2)
        ttk.Label(time_frame, text="Sec:").grid(row=0, column=4, padx=5, pady=2)
        self.alarm_hour = tk.IntVar(value=datetime.datetime.now().hour)
        self.alarm_minute = tk.IntVar(value=0)
        self.alarm_second = tk.IntVar(value=0)
        ttk.Spinbox(time_frame, from_=0, to=23, width=5, textvariable=self.alarm_hour).grid(row=0, column=1, padx=5, pady=2)
        ttk.Spinbox(time_frame, from_=0, to=59, width=5, textvariable=self.alarm_minute).grid(row=0, column=3, padx=5, pady=2)
        ttk.Spinbox(time_frame, from_=0, to=59, width=5, textvariable=self.alarm_second).grid(row=0, column=5, padx=5, pady=2)
        set_button = ttk.Button(self.alarm_frame, text="Set Alarm", command=self.set_alarm)
        set_button.pack(pady=10)
        self.alarm_status_label = ttk.Label(self.alarm_frame, text="No alarm set", font=("Helvetica", 12))
        self.alarm_status_label.pack(pady=5)

    def set_alarm(self):
        try:
            h = self.alarm_hour.get()
            m = self.alarm_minute.get()
            s = self.alarm_second.get()
        except Exception:
            messagebox.showerror("Error", "Invalid alarm time!")
            return
        now = datetime.datetime.now()
        target_time = datetime.datetime.combine(now.date(), datetime.time(h, m, s))
        if target_time <= now:
            target_time += datetime.timedelta(days=1)
        delay = (target_time - now).total_seconds()
        self.alarm_status_label.config(text=f"Alarm set for: {target_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.after(int(delay * 1000), self.alarm_trigger)

    def alarm_trigger(self):
        for i in range(8):
            winsound.Beep(1000, 500)  # Frequency: 1000 Hz, Duration: 500 ms
    messagebox.showinfo("Alarm", "Alarm time reached!")

if __name__ == "__main__":
    app = ToolboxApp()
    app.mainloop()