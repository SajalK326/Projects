# Simple Menu-Driven Library Management System
# Made by Sajal Kapoor (B. Tech CSE-B49, SAP_ID: 590011842)

# Functions:
#   (a) Add Book Details
#   (b) Delete book details
#   (c) Search for a Book
#   (d) View all the Books and their Author's Names
#   (e) Exit the Program

import sys,time
lib=[]
m=0

def Add_book():
    c=1
    while True :
        book=input(f"Enter the name of the Book-{c}: ")
        author=input(f"Enter the name of the author of the Book-{c}: ")
        book_det={book:author}
        lib.append(book_det)
        c+=1
        print("Book Details Added!!")
        print("\n")
        
        cont=input("Do you want to continue? [y/n]: ")
        if 'n' in cont or 'N' in cont:
            break

def Del_book():
    while True:
        a=input("Enter the name of the Book: ")
        for book_det in lib:
            if a in book_det:
                del book_det[a]
                print("Book Details have been Deleted!!")
                print("\n")
        
        cont=input("Do you want to continue? [y/n]: ")
        if 'n' in cont or 'N' in cont:
            break

def Search_book():
    while True:
        print("Enter 1 to Search using Book name")
        print("Enter 2 to Search using Author name")
        n=int(input("Enter Your Choice: "))
        if n==1:
            a=input("Enter the name of the Book: ")
            for book_det in lib:
                if a in book_det:
                    print("Book is Present in the Library")
                    print("Details: ", book_det)
                    print("\n")
                else:
                    print("Book is not present in the Library")
        elif n==2:
            a=input("Enter the Author's name of the Book: ")
            for book_det in lib:
                if a in book_det.values():
                    print("Book is Present in the Library")
                    print("Details: ", book_det)
                    print("\n")
                else:
                    print("Book is not present in the Library")

        cont=input("Do you want to continue? [y/n]: ")
        if 'n' in cont or 'N' in cont:
            break

def Display_All():
    print("All the details of the books:\n")
    print('\n'.join(str(book) for book in lib))
    
while m!=5:
    print("*_*_*_* Library Management System *_*_*_*\n")
    print("     Main Menu \n")
    print("Enter 1 to Add a book")
    print("Enter 2 to Delete a book")
    print("Enter 3 to Search a book")
    print("Enter 4 to Display all book Details")
    print("Enter 5 to Exit the program")
    m=int(input("Enter your choice: "))
    print("\n")

    if m==1:
        Add_book()
        print("\n")
    elif m==2:
        Del_book()
        print("\n")
    elif m==3:
        Search_book()
        print("\n")
    elif m==4:
        Display_All()
        print("\n")
    elif m==5:
        print(" © Sajal Kapoor. All Rights Reserved.")
        print("   B.Tech CSE, Batch: 49")
        print("   Sap_ID: 590011842")
        time.sleep(3)
        sys.exit()
    else:
        print("Enter a valid Choice")
        print("\n")
