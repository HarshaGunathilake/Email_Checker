import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd

df_global = None
filtered_df = None 

def upload_file():
    global df_global
    file_path = filedialog.askopenfilename(
        title="Select a CSV File",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    if file_path:
        try:
            df_global = pd.read_csv(file_path)
           
            upload_button.place_forget()
            
            left_label.pack(pady=5)
            tree.pack(fill=tk.BOTH, expand=True)
            dropdown_label.pack(pady=5)
            dropdown.pack(pady=5)
            save_button.pack(pady=10)
            
            dropdown["values"] = df_global.columns.tolist()
            dropdown.set("Select a column")
            
            populate_table(df_global, tree)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file\n{e}")

def populate_table(df, treeview):
    """Populate a Treeview with DataFrame data."""

    for row in treeview.get_children():
        treeview.delete(row)

    treeview["columns"] = df.columns.tolist()
    for col in df.columns:
        treeview.heading(col, text=col)
        treeview.column(col, anchor="w", width=100)
    
    for _, row in df.iterrows():
        treeview.insert("", "end", values=row.tolist())

def save_and_filter():
    """Filter data based on selected column and display below."""
    global filtered_df
    selected_column = dropdown.get()
    
    if selected_column == "Select a column" or not selected_column:
        messagebox.showerror("Error", "Please select a column from the dropdown.")
        return
    
    if df_global is not None:
        filtered_df = df_global[[selected_column]].drop_duplicates() 
        
        # Show filtered table
        filtered_label.pack(pady=10)
        filtered_tree.pack(fill=tk.BOTH, expand=True)
        export_button.pack(pady=10)
        
        populate_table(filtered_df, filtered_tree)
    else:
        messagebox.showerror("Error", "No data to filter. Please upload a CSV file first.")

def export_filtered_data():
    """Export the filtered data to a CSV file."""
    if filtered_df is not None:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Save Filtered Data"
        )
        if file_path:
            try:
                filtered_df.to_csv(file_path, index=False)
                messagebox.showinfo("Success", f"Filtered data saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file\n{e}")
    else:
        messagebox.showerror("Error", "No filtered data to export.")

# Create the main window
window = tk.Tk()
window.title("Email CSV ")
window.geometry('800x600')
window.configure(bg='#333333')

left_frame = tk.Frame(window, bg='#333333')
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

right_frame = tk.Frame(window, bg='#333333')
right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

left_label = tk.Label(left_frame, text="Table Data", bg='#333333', fg='white', font=("Arial", 12))
left_label.pack_forget()

tree = ttk.Treeview(left_frame, show="headings", height=10)
tree.pack_forget()

style = ttk.Style()
style.configure("Treeview", font=("Arial", 10), rowheight=25, background="white", foreground="black")
style.configure("Treeview.Heading", font=("Arial", 10, 'bold'), background="gray", foreground="gray")

dropdown_label = tk.Label(right_frame, text="Select a Table Header", bg='#333333', fg='white', font=("Arial", 12))
dropdown_label.pack_forget()

dropdown = ttk.Combobox(right_frame, state="readonly", font=("Arial", 10))
dropdown.pack_forget()

save_button = tk.Button(right_frame, text="Filter and Show Table", command=save_and_filter, bg='#007acc', fg='white', font=("Arial", 10))
save_button.pack_forget()

filtered_label = tk.Label(left_frame, text="Filtered Data", bg='#333333', fg='white', font=("Arial", 12))
filtered_label.pack_forget()

filtered_tree = ttk.Treeview(left_frame, show="headings", height=10)
filtered_tree.pack_forget()

export_button = tk.Button(left_frame, text="Export Filtered Data", command=export_filtered_data, bg='#28a745', fg='white', font=("Arial", 10))
export_button.pack_forget()

upload_button = tk.Button(window, text="Upload CSV", command=upload_file, bg='#555555', fg='white', font=("Arial", 10))
upload_button.place(relx=0.5, rely=0.5, anchor="center")

window.mainloop()
