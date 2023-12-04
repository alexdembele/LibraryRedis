import redis

#Book format :
#
#       key : ISBN
#
#       value : {Title,channel, author, number, language, year }



class BookPublisher:
    def __init__(self,channel):
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)
        self.channel = channel
        self.pubsub=self.redis_client.pubsub()
        self.pubsub.subscribe(self.channel)
        self.books_key = channel

    def add_book(self, book_title,description):
        '''
        Ajoute un livre et le dit ans le channel associé
        '''
        message = f"New book added : {book_title}"
        self.redis_client.publish(description["channel"], message)

        print(message)

        #Check if the book is already in the base
        if self.redis_client.exists(self.books_key,book_title):
            print("This book already exists")
            quantity = self.redis_client.hgetall(book_title)["number"]
            self.redis_client.hset(book_title,'number', str(int(quantity)+1))
        else:
            print("This book is new")
            self.redis_client.hset(book_title,mapping=description)

    def delete_book(self,book_title):
        '''
        Delete a book from the library
        '''
        self.redis_client.delete(book_title)
        message = f"Book deleted: {book_title}"
        self.redis_client.publish(self.channel, message)
        print("Book",book_title,"deleted.")


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

    # def listen_for_books(self):
    #     '''
    #     Liste des livres disponibles dans le channel
    #     '''
    #     for message in self.pubsub.listen():
    #         if message['type'] == 'message':
    #             print(f"Commande received : {message['data']}")
    #             break
    #         else:
    #             print(f"Nothing changed")
    #             break




    def find_book(self,book_title):
        '''
        Book research
        '''
        try:
            description = self.redis_client.hgetall(book_title)
            if description is not None:
                print(book_title, " : ", description)
            else:
                print("This book is not in our library")
        except:
            print("This book is not in our library")

    def borrow_a_book(self,book_title):
        '''
        Borrow a book if it exists
        '''
        # Check if book is available
        if self.redis_client.exists(self.books_key,book_title):


            quantity = int(self.redis_client.hgetall(book_title)["number"])
            if quantity >0:
                self.redis_client.hset(book_title,'number', str(quantity-1))
                print("This book is available")
            else:
                print("This book is not available")

            #Borrow the book
        else:
            print("This book is not available")

    def return_a_book(self,book_title):
        if book_title in self.books:
            self.redis_client.hset(book_title,'number', str(int(quantity)-1))
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



                    book_title = key.split(':')[-1]
                    book_data = self.redis_client.hgetall(key)
                    if book_data['channel'] == self.channel:

                        books[book_title] = book_data
            print(books)
