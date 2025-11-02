import tkinter as tk
from tkinter import ttk, filedialog, messagebox
try:
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
except ImportError:
    print("Error: 'Pillow' (PIL) library not found.")
    print("Please install it by running: pip install Pillow")
    exit()

class ExiftractGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Exiftract")
        self.root.geometry("700x550") 

        self.BG_COLOR = "#2E2E2E"
        self.FG_COLOR = "#F0F0F0"
        self.WIDGET_BG = "#3A3A3A"
        self.SELECT_BG = "#5A5A5A"
        self.BUTTON_BG = "#4A4A4A"
        
        self.root.configure(bg=self.BG_COLOR)

        style = ttk.Style()
        style.theme_use('clam') 

        style.configure(".", 
            background=self.BG_COLOR, 
            foreground=self.FG_COLOR,
            fieldbackground=self.WIDGET_BG,
            bordercolor=self.WIDGET_BG
        )
        style.configure("TFrame", background=self.BG_COLOR)
        style.configure("TLabel", background=self.BG_COLOR, foreground=self.FG_COLOR)
        style.configure("TLabelFrame", background=self.BG_COLOR, bordercolor=self.WIDGET_BG)
        style.configure("TLabelFrame.Label", background=self.BG_COLOR, foreground=self.FG_COLOR)
        style.configure("TButton", 
            background=self.BUTTON_BG, 
            foreground=self.FG_COLOR,
            bordercolor=self.WIDGET_BG
        )
        style.map("TButton",
            background=[('active', self.SELECT_BG)],
            foreground=[('active', self.FG_COLOR)]
        )
        style.map("TEntry",
            fieldbackground=[('readonly', self.WIDGET_BG)],
            foreground=[('readonly', self.FG_COLOR)]
        )
        style.configure("Treeview", 
            background=self.WIDGET_BG,
            fieldbackground=self.WIDGET_BG,
            foreground=self.FG_COLOR
        )
        style.configure("Treeview.Heading", 
            background=self.BUTTON_BG, 
            foreground=self.FG_COLOR,
            bordercolor=self.WIDGET_BG
        )
        style.map("Treeview.Heading",
            background=[('active', self.SELECT_BG)]
        )
        style.map("Treeview",
            background=[('selected', self.SELECT_BG)],
            foreground=[('selected', self.FG_COLOR)]
        )
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

        file_frame = ttk.LabelFrame(main_frame, text="File")
        file_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        file_frame.columnconfigure(0, weight=1)

        self.file_path_var = tk.StringVar(value="No file selected.")
        self.path_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, state="readonly")
        self.path_entry.grid(row=0, column=0, padx=(5,2), pady=5, sticky="ew")
        
        ttk.Button(file_frame, text="Browse...", command=self.load_image).grid(row=0, column=1, padx=(2,5), pady=5, sticky="e")

        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        self.scan_button = ttk.Button(control_frame, text="Scan Selected Image", command=self.start_scan)
        self.scan_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.save_button = ttk.Button(control_frame, text="Save Report as .txt", command=self.save_report)
        self.save_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

        results_frame = ttk.LabelFrame(main_frame, text="Metadata")
        results_frame.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(results_frame)
        self.tree["columns"] = ("Tag", "Value")
        self.tree.column("#0", width=0, stretch=tk.NO) 
        self.tree.column("Tag", anchor=tk.W, width=150)
        self.tree.column("Value", anchor=tk.W, width=500)
        self.tree.heading("Tag", text="Metadata Tag", anchor=tk.W)
        self.tree.heading("Value", text="Value", anchor=tk.W)
        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.status_var = tk.StringVar(value="Ready.")
        ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN).grid(row=3, column=0, sticky="ew", padx=5, pady=(5,0))

    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image File",
            filetypes=(
                ("Image Files", "*.jpg *.jpeg *.tif *.tiff"),
                ("PNG Files", "*.png"), 
                ("All Files", "*.*")
            )
        )
        if not file_path:
            return
        self.file_path_var.set(file_path)
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.status_var.set("File loaded. Click 'Scan' to extract metadata.")

    def start_scan(self):
        file_path = self.file_path_var.get()
        if not file_path or file_path == "No file selected.":
            messagebox.showerror("Error", "Please browse for an image file first.")
            return
        self.extract_metadata(file_path)

    def extract_metadata(self, file_path):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        try:
            image = Image.open(file_path)
            self.tree.insert("", "end", values=("File Format", image.format))
            self.tree.insert("", "end", values=("Image Size", f"{image.width}x{image.height}"))
            self.tree.insert("", "end", values=("Image Mode", image.mode))

            exif_data_raw = image._getexif()

            if not exif_data_raw:
                self.status_var.set("No advanced EXIF metadata found.")
                messagebox.showinfo(
                    "No EXIF Data",
                    "Successfully loaded basic info, but no EXIF (camera/GPS) metadata was found.\n\nThis is normal for PNG files or images saved from social media."
                )
                return

            for tag_id, value in exif_data_raw.items():
                tag_name = TAGS.get(tag_id, tag_id)

                if tag_name == "GPSInfo":
                    for gps_tag_id, gps_value in value.items():
                        gps_tag_name = GPSTAGS.get(gps_tag_id, gps_tag_id)
                        self.tree.insert("", "end", values=(f"GPS: {gps_tag_name}", f"{gps_value}"))
                else:
                    if isinstance(value, bytes):
                        value = value.decode(errors='replace').strip()
                        if len(value) > 100:
                            value = value[:100] + "..."
                    self.tree.insert("", "end", values=(f"{tag_name}", f"{value}"))
            
            self.status_var.set(f"Successfully extracted all metadata.")

        except Image.UnidentifiedImageError:
            self.status_var.set("Error: Cannot identify image file.")
            messagebox.showerror("Error", "The selected file is not a valid image.")
        except Exception as e:
            self.status_var.set(f"An error occurred: {e}")
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")

    def save_report(self):
        if not self.tree.get_children():
            messagebox.showwarning("Empty Report", "There is no metadata to save.")
            return

        file_path = filedialog.asksaveasfilename(
            title="Save Report As",
            defaultextension=".txt",
            initialfile="exiftract_report.txt",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
        )
        
        if not file_path:
            return

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"--- Exiftract Metadata Report ---\n")
                f.write(f"Source File: {self.file_path_var.get()}\n")
                f.write("--------------------------------\n\n")
                
                for item in self.tree.get_children():
                    data = self.tree.item(item, 'values')
                    if data:
                        tag = data[0]
                        value = data[1]
                        f.write(f"{tag}: {value}\n")
            
            self.status_var.set(f"Report saved to {file_path.split('/')[-1]}")
            messagebox.showinfo("Success", f"Report saved successfully to:\n{file_path}")
            
        except Exception as e:
            self.status_var.set(f"Error saving file: {e}")
            messagebox.showerror("Error", f"Could not save file: {e}")

if __name__ == "__main__":
    app_root = tk.Tk()
    gui = ExiftractGUI(app_root)
    app_root.mainloop()
