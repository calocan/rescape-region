import graphene
from rescape_python_helpers import ramda as R
import graphql_jwt
from graphene import ObjectType, Schema
from graphene_django.debug import DjangoDebug
#from graphql_jwt.decorators import login_required
from graphql_jwt.decorators import login_required
from rescape_graphene import allowed_query_arguments
from rescape_graphene import CreateUser, UpdateUser, UserType, user_fields
from django.contrib.auth import get_user_model, get_user

from rescape_region.models import Region, Feature, FeatureCollection, UserState, GroupState
from rescape_region.schema_models.feature_collection_schema import FeatureCollectionType, feature_collection_fields, \
    CreateFeatureCollection, UpdateFeatureCollection
from rescape_region.schema_models.feature_schema import FeatureType, CreateFeature, UpdateFeature, feature_fields
from rescape_region.schema_models.group_state_schema import GroupStateType, group_state_fields
from rescape_region.schema_models.region_schema import RegionType, region_fields, CreateRegion, UpdateRegion
from rescape_region.schema_models.user_state_schema import UserStateType, user_state_fields


class Query(ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')
    users = graphene.List(UserType)
    viewer = graphene.Field(
        UserType,
        **allowed_query_arguments(user_fields, UserType)
    )

    @login_required
    def resolve_viewer(self, info, **kwargs):
       return info.context.user

    regions = graphene.List(
        RegionType,
        **allowed_query_arguments(region_fields, RegionType)
    )

    region = graphene.Field(
        RegionType,
        **allowed_query_arguments(feature_fields, RegionType)
    )

    features = graphene.List(
        FeatureType,
        **allowed_query_arguments(feature_fields, FeatureType)
    )

    feature = graphene.Field(
        FeatureType,
        **allowed_query_arguments(feature_fields, FeatureType)
    )

    feature_collections = graphene.List(
        FeatureCollectionType,
        **allowed_query_arguments(feature_collection_fields, FeatureCollectionType)
    )

    feature_collection = graphene.Field(
        FeatureCollectionType,
        **allowed_query_arguments(feature_collection_fields, FeatureCollectionType)
    )
    
    user_states = graphene.List(
        UserStateType,
        **allowed_query_arguments(user_state_fields, UserStateType)
    )

    user_state = graphene.Field(
        UserStateType,
        **allowed_query_arguments(user_state_fields, UserStateType)
    )

    group_states = graphene.List(
        GroupStateType,
        **allowed_query_arguments(group_state_fields, GroupStateType)
    )

    group_state = graphene.Field(
        GroupStateType,
        **allowed_query_arguments(group_state_fields, GroupStateType)
    )

    def resolve_users(self, info, **kwargs):
        return get_user_model().objects.filter(**kwargs)

    def resolve_current_user(self, info):
        context = info.context
        user = get_user(context)
        if not user:
            raise Exception('Not logged in!')

        return user

    def resolve_regions(self, info, **kwargs):
        # Small correction here to change the data filter to data__contains to handle any json
        # https://docs.djangoproject.com/en/2.0/ref/contrib/postgres/fields/#std:fieldlookup-hstorefield.contains
        return Region.objects.filter(
            deleted=False,
            **R.map_keys(lambda key: 'data__contains' if R.equals('data', key) else key, kwargs))

    def resolve_features(self, info, **kwargs):
        return Feature.objects.filter(**kwargs)

    def resolve_feature_collections(self, info, **kwargs):
        return FeatureCollection.objects.filter(**kwargs)

    def resolve_user_states(self, info, **kwargs):
        return UserState.objects.filter(**kwargs)

    def resolve_group_states(self, info, **kwargs):
        return GroupState.objects.filter(**kwargs)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    # login = Login.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    create_region = CreateRegion.Field()
    update_region = UpdateRegion.Field()

    create_feature = CreateFeature.Field()
    update_feature = UpdateFeature.Field()

    create_feature_collection = CreateFeatureCollection.Field()
    update_feature_collection = UpdateFeatureCollection.Field()


schema = Schema(query=Query, mutation=Mutation)