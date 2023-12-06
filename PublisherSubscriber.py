import redis

#Book format :
#
#       key : ISBN
#
#       value : {Title,channel, author, number, language, year }


expiration_time_seconds =15
class BookPublisher:
    def __init__(self,channel):
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)
        self.channel = channel
        self.pubsub=self.redis_client.pubsub()
        self.pubsub.subscribe(self.channel)
        self.books_key = channel

    def add_book(self, ISBN,channel,book_title,author,language,year):
        '''
        Ajoute un livre et le dit ans le channel associé
        '''
        message = f"New book added : {book_title}"
        self.redis_client.publish(channel, message)
        description = {'Title':book_title,'channel':channel,'author':author,'number':1,'language':language,'year':year}
        print(message)

        #Check if the book is already in the base
        if self.redis_client.exists(self.books_key,book_title):
            print("This book already exists")
            quantity = self.redis_client.hgetall(ISBN)["number"]
            self.redis_client.hset(ISBN,'number', str(int(quantity)+1))
            self.redis_client.expire(ISBN, expiration_time_seconds)
        else:
            print("This book is new")
            self.redis_client.hset(ISBN,mapping=description)
            self.redis_client.expire(ISBN, expiration_time_seconds)

    def delete_book(self,ISBN):
        '''
        Delete a book from the library
        '''
        try:
            self.redis_client.delete(ISBN)
            message = f"Book deleted: {ISBN}"
            self.redis_client.publish(self.channel, message)
            print("Book",ISBN,"deleted.")



        except:
            print("This book is not in our library")


class BookSubscriber:
    def __init__(self,channel):
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)
        self.channel = channel
        self.pubsub = self.redis_client.pubsub()
        self.pubsub.subscribe(self.channel)
        self.books_key = channel
        self.books=[]




    def listen_for_news(self):
        '''
        Liste des livres disponibles dans le channel
        '''

        message = self.pubsub.get_message()
        if message==None:
            print("Nothing new")
        else:
            channel = message['channel']
            data = message['data']
            if channel == self.channel and data!=1:
                print(data)
            else:
                print("Nothing new")



    def find_book_ISBN(self,ISBN):
        '''
        Book research with ISBN
        '''
        try:
            description = self.redis_client.hgetall(ISBN)
            if description is not None:
                print(ISBN, " : ", description)
            else:
                print("This book is not in our library")
        except:
            print("This book is not in our library")

    def find_book_title(self,book_title):
        '''
        Book research with title
        '''
        book_keys = self.redis_client.keys(f'*')
        for key in book_keys:
            ISBN = key.split(':')[-1]
            book_data = self.redis_client.hgetall(key)
            if book_data['Title']==book_title:
                print(key,book_data)
        print("End of search")
    def show_books(self):
        print(self.books)



    def borrow_a_book(self,ISBN):
        '''
        Borrow a book if it exists
        '''
        # Check if book is available
        if self.redis_client.exists(self.books_key,ISBN):


            quantity = int(self.redis_client.hgetall(ISBN)["number"])
            if quantity >0:
                self.redis_client.hset(ISBN,'number', str(quantity-1))
                print("This book is available")
                self.books.append(ISBN)
            else:
                print("This book is not available")

            #Borrow the book
        else:
            print("This book is not available")

    def return_a_book(self,ISBN):
        if ISBN in self.books:
            quantity = self.redis_client.hgetall(ISBN)["number"]
            self.redis_client.hset(ISBN,'number', str(int(quantity)+1))
            self.books.remove(ISBN)
            print("You returned this book")
        else:
            print("You don't have this book")


    def get_all_books(self):
            '''
            Show all books in base
            '''
            books = {}
            book_keys = self.redis_client.keys(f'*')
            for key in book_keys:
                if key !="foo":



                    ISBN = key.split(':')[-1]
                    book_data = self.redis_client.hgetall(key)


                    books[ISBN] = book_data
            print(books)
