# Simple Menu-Driven Library Management System
# Made by Sajal Kapoor (B. Tech CSE-B49, SAP_ID: 590011842)

# Functions:
#   (a) Add Book Details
#   (b) Delete book details
#   (c) Search for a Book
#   (d) View all the Books and their Author's Names
#   (e) Exit the Program

class record:
    def __init__(self):
        self.lib=[]

    def Add_book(self):
        c=1
        while True :
            book=input(f"Enter the name of the Book-{c}: ")
            author=input(f"Enter the name of the author of the Book-{c}: ")
            det={book:author}
            self.lib.append(det)
            c+=1
            print("Book Details Added!!")
            print("\n")
            
            con=input("Do you want to continue? [y/n]: ")
            if 'n' in con or 'N' in con:
                break

    def Del_book(self):
        while True:
            a=input("Enter the name of the Book: ")
            for det in self.lib:
                if a in det:
                    del det[a]
                    print("Book Details have been Deleted!!")
                    print("\n")
            
            con=input("Do you want to continue? [y/n]: ")
            if 'n' in con or 'N' in con:
                break

    def Search_book(self):
        while True:
            print("Enter 1 to Search using Book name")
            print("Enter 2 to Search using Author name")
            n=int(input("Enter Your Choice: "))
            if n==1:
                a=input("Enter the name of the Book: ")
                found=False
                for det in self.lib:
                    if a in det:
                        print("Book is Present in the Library")
                        print("Details: ", det)
                        print("\n")
                        found=True
                        break
                    else:
                        print("Book is not present in the Library")

            elif n==2:
                a=input("Enter the Author's name of the Book: ")
                found=False
                for det in self.lib:
                    if a in det.values():
                        print("Book is Present in the Library")
                        print("Details: ", det)
                        print("\n")
                        found=True
                        break
                    else:
                        print("Book is not present in the Library")
            
                if not found:
                    print("Book is NOT present in the library")
                print("\n")

            con=input("Do you want to continue? [y/n]: ")
            if 'n' in con or 'N' in con:
                break

    def Display_All(self):
        print("All the details of the books:\n")
        print('\n'.join(str(book) for book in self.lib))

rec=record()

while True:
    print("*_*_*_* Library Management System *_*_*_*\n")
    print("     Main Menu \n")
    print("Enter 1 to Add a book")
    print("Enter 2 to Delete a book")
    print("Enter 3 to Search a book")
    print("Enter 4 to Display all book Details")
    print("Press Ctrl+C to Exit the program")
    m=int(input("Enter your choice: "))
    print("\n")

    if m==1:
        rec.Add_book()
        print("\n")
    elif m==2:
        rec.Del_book()
        print("\n")
    elif m==3:
        rec.Search_book()
        print("\n")
    elif m==4:
        rec.Display_All()
        print("\n")
    else:
        print("Enter a valid Choice")
        print("\n")