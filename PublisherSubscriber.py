import redis

#Book format :
#
#       key : ISBN
#
#       value : {Title, author, number, language, year }

class BookPublisher:
    def __init__(self,channel):
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)
        self.channel = channel
        self.books_key = 'livres'

    def add_book(self, book_title,description):
        '''
        Ajoute un livre et le dit ans le channel associé
        '''
        message = f"Nouveau livre ajouté : {book_title}"
        self.redis_client.publish(self.channel, message)
        print(message)

        #Check if the book is already in the base
        if self.redis_client.exists(self.books_key,book_title):
            print("This book already exists")
            quantity = self.redis_client.hgetall(book_title)["number"]
            self.redis_client.hset(book_title,'number', str(int(quantity)+1))



        else:
            print("This book is new")
            self.redis_client.hset(book_title,mapping=description)


class BookSubscriber:
    def __init__(self,channel):
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)
        self.channel = channel
        self.pubsub = self.redis_client.pubsub()
        self.pubsub.subscribe(self.channel)
        self.books_key = 'livres'



    def listen_for_books(self):
        '''
        Liste des livres disponibles dans le channel
        '''
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                print(f"Commande reçue : {message['data']}")
            break


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

    def get_all_books(self):
            '''
            Show all books in base
            '''
            books = {}
            book_keys = self.redis_client.keys(f'*')
            for key in book_keys:


                print(key)
                book_title = key.split(':')[-1]
                book_data = self.redis_client.hgetall(key)

                books[book_title] = book_data
            print(books)
