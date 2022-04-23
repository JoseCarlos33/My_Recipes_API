import graphene
from graphene_django import DjangoObjectType
import recipes.schema
import users.schema

class Query(
  users.schema.Query,
  recipes.schema.Query,
  graphene.ObjectType
):
  pass
    

class Mutation(
  users.schema.Mutation,
  # recipes.schema.Mutation,
  graphene.ObjectType
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)