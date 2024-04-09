import graphene
from graphene_django import DjangoObjectType     # used to change Django object into a format that is readable by GraphQL
from .models import Book
from django.contrib.auth import get_user_model
# from account.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        exclude = ["password"]




class BookType(DjangoObjectType):
    # Describe the data that is to be formatted into GraphQL fields
    author = graphene.Field(UserType)
    class Meta:
            ## register you model
        model = Book
            ## add fields 
        # fields = "__all__"


        ## this is for complete crud operation
class Query(graphene.ObjectType):

        ## query BookType to get list of books..... list out all the data present there
    list_book = graphene.List(BookType)

        ## retrive any particular data.... retrive by quering the name field
    read_book = graphene.Field(BookType, name=graphene.String(required=True)) # name=graphene.String() gives name an string datatype

        ## retrive any particular data.... retrive by quering the id field
    # read_book = graphene.Field(BookType, id=graphene.Int()) # id=graphene.Int() gives id an integer datatype

    def resolve_list_book(root, info):
            ## We can easily optimize query count in the resolve method
        return Book.objects.all()
            ## you can return data like this
        # return BookType.objects.all().order_by('name')


    def resolve_read_book(root, info, name):
            ## get that particular data where name in the database is same as the qurery name = name queried from the frontend
        return Book.objects.get(name=name)

    
    # def resolve_read_book(root, info, id):
            ## get data where id in the database = id queried from the frontend
        # return Book.objects.get(id=id)

    ## register your query here
# schema = graphene.Schema(query=Query)





    ## Mutation in GraphQL is used to modify data or create data in the database and returns a value.
class BookCreateMutation(graphene.Mutation):
        ## define the class we are getting the fields from
    book = graphene.Field(BookType)
    class Arguments:
            ## Add fields you would like to create. This will corelate with the BookType fields above.
            ## ID is auto generated field ... so i want to add the remaining two field
        name=graphene.String(required=True)
        language=graphene.String(required=True)
        author_id=graphene.ID(required=True)

    

    ## you can use class method ... write those fields which you will get from the request
    @classmethod
    def mutate(cls, root, info, name, language, author_id):
            ## function that will save the data
        new_book = Book(name=name, language=language, author_id=author_id) ## accepts all fields
            ## save the new_book data
        new_book.save()
        return BookCreateMutation(book= new_book)





        ## for update
class BookUpdateMutation(graphene.Mutation):
    class Arguments:
            ## add fields you will like to create. This will corelate with the BookType fields above
        id = graphene.ID(required=True) # new
        name=graphene.String()
        language=graphene.String()
        author_id = graphene.ID()
    book = graphene.Field(BookType) # define the class we are getting the fields from
    errors = graphene.List(graphene.String)

    # @classmethod
    # def mutate(cls, root, info,id, name, language, author):
    #     try:
    #         get_book = Book.objects.get(id=id)
    #     except Exception as e:
    #         return BookUpdateMutation(book={'msg':'No record'})
    #     get_book.name = name #override name
    #     get_book.phone_number = phone_number #override phone_number
    #     get_book.save()
    #     return BookUpdateMutation(book=get_book)

    @classmethod
    def mutate(cls, root, info, id ,name=None, language=None, author_id=None):
        # try:
        #     get_book = Book.objects.get(id=id)
        # except Exception as e:
        #     # return BookUpdateMutation(book={'msg':'No record'})
        #     return BookUpdateMutation(book=None, errors=["book not found"])
        try:
            get_book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return BookUpdateMutation(book=None, errors=["Book not found"])
        if name is not None:
            get_book.name = name
        if language is not None:
            get_book.language = language
        if author_id is not None:
            get_book.author_id = author_id
        get_book.save()
        return BookUpdateMutation(book=get_book, errors=[])




class BookDeleteMutation(graphene.Mutation):
    book = graphene.Field(BookType)
    # book = graphene.List(graphene.String)
    errors = graphene.List(graphene.String)
    class Arguments:
        id = graphene.ID(required=True)


    # @classmethod   
    # def mutate(cls, root, info, id):
    #     book = Book(id=id)
    #     #########Delete##############
    #     book.delete()

    @classmethod
    def mutate(cls, root, info, id):
        try:
            get_book = Book.objects.get(id=id)
        except Exception:
            return BookDeleteMutation(book=None, errors=["book not found"])
        get_book.delete()
        return BookDeleteMutation(book=None, errors=[])




class Mutation(graphene.ObjectType):
    # keywords that will be used to do the mutation in the frontend
    create_book = BookCreateMutation.Field()  
    update_book = BookUpdateMutation.Field()
    delete_book = BookDeleteMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation) # Tell the schema about the mutation you just created.
