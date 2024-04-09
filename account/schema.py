import graphene, graphql_jwt
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import login_required
from graphql_jwt.shortcuts import create_refresh_token, get_token
from graphql import GraphQLError
from django.contrib.auth import authenticate
from .models import User



class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()



class LoginType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password']


class UserProfileUpdateType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = ['username', 'is_active']



class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()
    refresh_token = graphene.String()
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

            ####  option : 1 
    def mutate(self, info, username, email, password):
        user = User.objects.create_user(username=username, email=email, password=password)
        token = get_token(user)
        refresh_token = create_refresh_token(user)
        return CreateUser(user= user, token=token, refresh_token=refresh_token)
    
            ####  option : 2
    # def mutate(self, info, username, email, password):
    #     user = get_user_model()(username=username, email=email)
    #     user.set_password(password)
    #     user.save()
    #     token = get_token(user)
    #     refresh_token = create_refresh_token(user)
    #     return CreateUser(user= user, token=token, refresh_token=refresh_token)


class UserLogin(graphene.Mutation):
    token = graphene.String()
    refresh_token = graphene.String()
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    
    def mutate(self, info, email, password):
        user = authenticate(email=email, password=password)
        if user:
            token = get_token(user)
            refresh_token = create_refresh_token(user)
            return UserLogin(token=token, refresh_token=refresh_token)
        raise GraphQLError("Authentication failure ....")



class UserProfileUpdate(graphene.Mutation):
    success = graphene.Boolean()
    # profile_update = graphene.Field(UserProfileUpdateType)
    class Arguments:
        username = graphene.String()
        is_active = graphene.Boolean()

    @login_required
    def mutate(self, info, username=None, is_active=None):
        user = info.context.user
        if username:
            user.username = username
        if is_active is not None:
            user.is_active = is_active
        user.save()
        return UserProfileUpdate(success=True)
        # return UserProfileUpdate(profile_update=user)




class Query(graphene.ObjectType):
    reqUser = graphene.Field(UserType)
    users = graphene.List(UserType)

    @login_required
    def resolve_reqUser(self, info, **kwargs):
        # print(info.context)
        user = info.context.user
        if not user.is_authenticated:
            # raise Exception("Authentication failure ....")
            raise GraphQLError("Authentication failure ....")
        return user

    @login_required
    def resolve_users(self, info):
        print(info.context.user)
        return get_user_model().objects.all()


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    verify_token = graphql_jwt.Verify.Field()
    create_user = CreateUser.Field()
    user_login = UserLogin.Field()
    user_profile_update = UserProfileUpdate.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)