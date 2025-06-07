
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["paperref_manager"]

paper_collection = db["paper"]
print(paper_collection)

def add_paper(name, author, year):
    paper_collection.insert_one({"name": name, "author": author, "year": year})

def list_paper():
    print("\n")
    print("*" * 60)
    for paper in paper_collection.find():
        print(f"ID: {paper["_id"]}, Name: {paper["name"]} and author: {paper["author"]} in {paper["year"]}")
    print("\n")
    print("*" * 60)
def update_paper(paper_id, new_name, new_author, new_year):
    paper_collection.update_one(
        {"_id" : ObjectId(paper_id)},
        {"$set": {"name": new_name, "author": new_author, "year": new_year}})

def delete_paper(paper_id):
    paper_collection.delete_one({"_id": ObjectId(paper_id)})

def main():
    while True:
        print("\n PaperRef_manager | choose an option")
        print("1. List all Paper references ")
        print("2. Add Paper references ")
        print("3. Update Paper references details ")
        print("4. Delete Paper references ")
        print("5. Exit the app ")
        choice = input("Enter your choice: ")

        if choice == "1":
            list_paper()

        elif choice == "2":
            name = input("Enter the new paper title: ")
            author = input("Enter the new author name: ")
            year = input("Enter the new year: ")
            add_paper(name, author, year)

        elif choice == "3": 
            paper_id = input("Enter the paper ID to update: ")
            author = input("Enter the new author name: ")
            year = input("Enter the new year: ")
            update_paper(paper_id, name, author,year)

        elif choice == "4": 
            paper_id = input("Enter the paper ID to delete: ")
            delete_paper(paper_id)

        elif choice == "5": 
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()