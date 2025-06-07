
import tkinter as tk
from tkinter import messagebox, simpledialog
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# MongoDB setup
client = MongoClient(MONGO_URI)
db = client["paperref_manager"]
paper_collection = db["paper"]

# GUI App
class PaperRefManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Paper Reference Manager")
        self.root.geometry("600x400")

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.listbox = tk.Listbox(self.frame, height=15, width=80)
        self.listbox.pack(pady=10)

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack()

        tk.Button(btn_frame, text="Add Paper", command=self.add_paper).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update Selected", command=self.update_paper).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete Selected", command=self.delete_paper).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Refresh", command=self.load_papers).grid(row=0, column=3, padx=5)

        self.load_papers()

    def load_papers(self):
        self.listbox.delete(0, tk.END)
        self.paper_ids = []
        for paper in paper_collection.find():
            display = f"{paper['name']} by {paper['author']} ({paper['year']})"
            self.listbox.insert(tk.END, display)
            self.paper_ids.append(str(paper["_id"]))

    def add_paper(self):
        name = simpledialog.askstring("Title", "Enter paper title:")
        author = simpledialog.askstring("Author", "Enter author name:")
        year = simpledialog.askstring("Year", "Enter publication year:")
        if name and author and year:
            paper_collection.insert_one({"name": name, "author": author, "year": year})
            self.load_papers()

    def update_paper(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Select Paper", "Please select a paper to update.")
            return
        idx = selected[0]
        paper_id = self.paper_ids[idx]

        new_name = simpledialog.askstring("Update", "Enter new title:")
        new_author = simpledialog.askstring("Update", "Enter new author:")
        new_year = simpledialog.askstring("Update", "Enter new year:")

        if new_name and new_author and new_year:
            paper_collection.update_one(
                {"_id": ObjectId(paper_id)},
                {"$set": {"name": new_name, "author": new_author, "year": new_year}}
            )
            self.load_papers()

    def delete_paper(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Select Paper", "Please select a paper to delete.")
            return
        idx = selected[0]
        paper_id = self.paper_ids[idx]
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this paper?")
        if confirm:
            paper_collection.delete_one({"_id": ObjectId(paper_id)})
            self.load_papers()


if __name__ == "__main__":
    root = tk.Tk()
    app = PaperRefManager(root)
    root.mainloop()
