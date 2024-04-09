import graphene
import account.schema
import book.schema

class Query(account.schema.Query, book.schema.Query, graphene.ObjectType):
    pass

class Mutation(account.schema.Mutation, book.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)