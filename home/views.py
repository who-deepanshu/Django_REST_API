from rest_framework.decorators import api_view
from rest_framework.response import Response
from home.models import Person
from home.serializers import PeopleSerializer, LoginSerializer, RegisterSerializer
from rest_framework.views import APIView
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.paginator import Paginator
from rest_framework.decorators import action


# Api for user registration
class RegisterAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data = data)

        if not serializer.is_valid():
            return Response(
                {'message' : serializer.errors},
                status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save()

        return Response({'message' : "user created"}, status.HTTP_201_CREATED)

        
# Login API
class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data = data)

        if not serializer.is_valid():
            return Response(
                {'message' : serializer.errors},
                status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(
            username = serializer.data['username'],
            password = serializer.data['password']
        )

        # if user is not exist
        if not user:
            return Response(
                {'message' : 'invalid credentials'},
                status.HTTP_400_BAD_REQUEST
            )

        token, _ = Token.objects.get_or_create(user = user)

        return Response(
            {'message' : 'user logged in', 'token' : str(token)},
            status.HTTP_201_CREATED
        )



@api_view(['GET', 'POST', 'PUT'])
def index(request):
    courses = {
            'course' : 'python',
            'learn' : ['flask', 'django', 'fastapi'],
            'course_provider' : 'Scaler'
        }
    if request.method == 'GET':
        return Response(courses)
    elif request.method == 'POST':
        data = request.data
        print(data)
        return Response(courses)
    


@api_view(['GET', 'POST', 'PUt', 'PATCH', 'DELETE'])
def person(request):
    if request.method == 'GET':
        objs = Person.objects.filter(color__isnull = False)
        serializer = PeopleSerializer(objs, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        serializer = PeopleSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'PUT':
        data = request.data
        objs = Person.objects.get(id = data['id'])
        serializer = PeopleSerializer(instance=objs, data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'PATCH':
        data = request.data
        objs = Person.objects.get(id = data['id'])
        serializer = PeopleSerializer(objs, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    else:
        data = request.data
        obj = Person.objects.get(id = data['id'])
        obj.delete
        return Response({'message' : 'deleted successfully'})
        
    return Response(serializer.errors)
        


# Login Serializer using Serializer class only
@api_view(['POST'])
def login(request):
    data = request.data
    serializer = LoginSerializer(data = data)
    if serializer.is_valid():
        data = serializer.validated_data
        return Response({'message' : 'success'})
    
    return Response(serializer.errors)




# Handling API requests using APIView class(Not API decorators)
class PersonAPI(APIView):
    # to serve data to only authenticated users
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        #objs = Person.objects.filter(color__isnull = False)
        # Pagination
        try:
            objs = Person.objects.all()
            page = request.GET.get('page', 1)
            page_size = 3 
            paginator = Paginator(objs, page_size)
            serializer = PeopleSerializer(paginator.page(page), many = True)
            #serializer = PeopleSerializer(objs, many = True)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                'message' : 'invalid page'
            })
    def post(self, request):
        data = request.data
        serializer = PeopleSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def put(self, request):
        data = request.data
        objs = Person.objects.get(id = data['id'])
        serializer = PeopleSerializer(instance=objs, data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    def patch(self, request):
        data = request.data
        objs = Person.objects.get(id = data['id'])
        serializer = PeopleSerializer(objs, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def delete(self, request):
        data = request.data
        obj = Person.objects.get(id = data['id'])
        obj.delete
        return Response({'message' : 'deleted successfully'})
    


# Handling all requests using Viewset
class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()


    # Filter method for GET 
    def list(self, request):
        search = request.GET.get('search')
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__startswith = search)

        serializer = PeopleSerializer(queryset, many = True)
        return Response({'data' : serializer.data})
    

    # action in ViewSet to add extra functions.routes in api
    @action(detail = True, methods=['post'])
    def send_mail_to_someone(self, request, pk):
        obj = Person.objects.get(id = pk)
        serializer = PeopleSerializer(obj)
        return Response({
            'message' : 'mail sent',
            'data' : serializer.data
        })