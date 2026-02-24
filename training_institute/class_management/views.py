from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly,MarkPermission
import requests
from django.conf import settings


# Create your views here.
###################################################Subjects################################################
class Subject(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get(self,request):
        subject=Subjects.objects.filter(is_archived=False)
        serializer= subjectserializer(subject,many=True)
        return Response({
                'success':True,
                'message': 'Subject List',
                'Data': serializer.data
            }) 




    def post(self,request):

        serializer=subjectserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success':True,
                'message': 'Subject added successfully',
                'Data': serializer.data
            }) 
        return Response({
                'success':False,
                'message': 'There is some error in adding subject',
                'Data': serializer.data
            }) 



    def put(self,request):
            subject=Subjects.objects.get(id=request.data['id'])
            serializer = subjectserializer(subject,data=request.data)
            if serializer.is_valid():
                print(serializer.errors)
                serializer.save()
                return Response({
                'success':True,
                'message': 'Subject Updated successfully',
                'Data': serializer.data
            }) 
            return Response({
                'success':False,
                'message': 'Invalid ID',
                'Data': serializer.data
            }) 
        

    def patch(self,request):
            subject=Subjects.objects.get(id=request.data['id'])
            serializer=subjectserializer(subject,data=request.data, partial=True)
            if serializer.is_valid():
                print(serializer.errors)
                serializer.save()
                return Response({
                    'success':True,
                    'message': 'Subject updated successfully',
                    'Data': serializer.data
                }) 
            return Response({
                'success':False,
                'message': 'Invalid ID',
                'Data': serializer.data
            }) 
        

    
    def delete(self,request):
            subject=Subjects.objects.get(id=request.data['id'])
            subject.is_archive = True
            subject.save()
            return Response({
                'success':True,
                'message': 'Subject deleted succesfully',
                'Data': None
            }) 
##########################################user######################################
class UserView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get(self, request):
        users = User.objects.prefetch_related("subjects")

        serializer = UserSerializer(users, many=True)

        return Response({
            "success": True,
            "message": "User List",
            "data": serializer.data
        })

    def post(self, request):
        
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "User created successfully",
                "data": serializer.data
            }, status=201)

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=400)

    def patch(self, request):
        user=User.objects.get(id=request.data['id'])
        serializer = UserSerializer(user,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "User Updated successfully",
                "data": serializer.data
            }, status=201)

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=400)
    
    def delete(self,request):
            user=User.objects.get(id=request.data['id'])
            user.is_archive = True
            user.save()
            return Response({
                'success':True,
                'message': 'User deleted succesfully',
                'Data': None
            }) 

####################################################Courses#########################3
class Course(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get(self,request):
        course=Courses.objects.filter(is_archived=False)
        serializer= courseserializer(course,many=True)
        return Response({
                'success':True,
                'message': 'Course List',
                'Data': serializer.data
            }) 


    def post(self, request):
        serializer = courseserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Course and Subjects created successfully",
                "Data": serializer.data  
            })
        
        return Response({
            "success": False,
            "message": "There is some error in adding course",
            "Data": serializer.data
        })
    
    def patch(self,request):
            course=Courses.objects.get(id=request.data['id'])
            serializer=courseserializer(course,data=request.data, partial=True)
            if serializer.is_valid():
                print(serializer.errors)
                serializer.save()
                return Response({
                    'success':True,
                    'message': 'Course updated successfully',
                    'Data': serializer.data
                }) 
            return Response({
                'success':False,
                'message': 'Invalid ID',
                'Data': serializer.data
            }) 
    

    def delete(self,request):
            course=Courses.objects.get(id=request.data['id'])
            course.is_archived = True
            course.save()
            return Response({
                'success':True,
                'message': 'Course deleted succesfully',
                'Data': None
            }) 



    
#####################################################Batch######################################


class Batch(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get(self, request):
        batches = Batches.objects.select_related("course").prefetch_related(
            "subject_teachers__subject",
            "subject_teachers__teacher"
        )

        serializer = BatchSerializer(batches, many=True)

        return Response({
            "success": True,
            "message": "Batch List",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BatchSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Batch created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        batch = get_object_or_404(Batches, id=request.data.get("id"))

        serializer = BatchSerializer(
            batch,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Batch updated successfully",
                "data": serializer.data
            })

        return Response(serializer.errors, status=400)

    def delete(self, request):
        batch = get_object_or_404(Batches, id=request.data.get("id"))
        batch.is_archived = True
        batch.save()

        return Response({
            "success": True,
            "message": "Batch deleted successfully"
        })



#####################################Enrollment#############################


class Enrollment(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get(self, request):
        enrollments = Enrollments.objects.select_related(
            "batch",
            "student"
        ).filter(is_archived=False)

        serializer = EnrollmentSerializer(enrollments, many=True)

        return Response({
            "success": True,
            "message": "Enrollment List",
            "data": serializer.data
        })

    def post(self, request):
        serializer = EnrollmentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Student enrolled successfully",
                "data": serializer.data
            }, status=201)

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=400)

    def delete(self, request):
        enrollment = get_object_or_404(
            Enrollments,
            id=request.data.get("id")
        )

        enrollment.is_archived = True
        enrollment.save()

        return Response({
            "success": True,
            "message": "Enrollment deleted successfully"
        })

###########################Marks##################


class Mark(APIView):

    permission_classes = [IsAuthenticated, MarkPermission]
   

    def get(self, request):
        marks = Marks.objects.select_related(
            "enrollment__batch",
            "enrollment__batch__course",
            "enrollment__student",
            "subject"
        )

        if request.user.role == "student":
            marks = marks.filter(enrollment__student=request.user)

        serializer = MarksSerializer(marks, many=True)

        return Response({
            "success": True,
            "message": "Marks List",
            "data": serializer.data
        })
        
      
    def post(self, request):
    
        serializer = MarksSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Marks assigned successfully",
                "data": serializer.data
            }, status=201)

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=400)
    
########################################Login#########################################3


class LoginView(APIView):

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        token_url = "http://127.0.0.1:8000/o/token/"

        data = {
            "grant_type": "password",
            "username": username,
            "password": password,
            "client_id": settings.CLIENT_ID,
            "client_secret": settings.CLIENT_SECRET,
        }

        response = requests.post(token_url, data=data)

        return Response(response.json(), status=response.status_code)
















####################################################################################
  # if request.user.role == "student":
        #     marks = Marks.objects.filter(
        #         enrollment__student=request.user
        #     )

        
        # elif request.user.role == "teacher":
        #     marks = Marks.objects.filter(
        #         enrollment__batch__subject_teachers__teacher=request.user
        #     )

        # else:
        #     return Response({"error": "Not allowed"}, status=403)

        # serializer = MarksSerializer(marks, many=True)
        # return Response({'Success':True,"message":"Mark List",'data':serializer.data})


##########################################################Teacher#####################################
# class Teacher(APIView):

#     def get(self,request):
#         teacher=Teachers.objects.all()
#         serializer= teacherserializer(teacher,many=True)
#         return Response({
#                 'success':True,
#                 'message': 'Teacher List',
#                 'Data': serializer.data
#             }) 


#     def post(self, request):
#         serializer = teacherserializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 "success": True,
#                 "message": "Teacher and Subjects created successfully",
#                 "Data": serializer.data  
#             })
        
#         return Response({
#             "success": False,
#             "message": "There is some error in adding teacher",
#             "Data": serializer.data
#         })
    
#     def patch(self,request):
#             teacher=Teachers.objects.get(id=request.data['id'])
#             serializer=teacherserializer(teacher,data=request.data, partial=True)
#             if serializer.is_valid():
#                 print(serializer.errors)
#                 serializer.save()
#                 return Response({
#                     'success':True,
#                     'message': 'Teacher updated successfully',
#                     'Data': serializer.data
#                 }) 
#             return Response({
#                 'success':False,
#                 'message': 'Invalid ID',
#                 'Data': serializer.data
#             }) 
    

#     def delete(self,request):
#             teacher=Teachers.objects.get(id=request.data['id'])
#             teacher.is_archived = True
#             teacher.save()
#             return Response({
#                 'success':True,
#                 'message': 'Teacher deleted succesfully',
#                 'Data': None
#             }) 



# class Mark(APIView):

#     def get(self, request):
#         marks = Marks.objects.select_related(
#             "enrollment__batch",
#             "enrollment__student",
#             "course",
#             "subject"
#         ).all()

#         serializer = MarksSerializer(marks, many=True)

#         return Response(
#             {
#                 "success": True,
#                 "message": "Marks List",
#                 "data": serializer.data
#             },
           
#         )

#     def post(self, request):
#         serializer = MarksSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {
#                     "success": True,
#                     "message": "Marks assigned successfully",
#                     "data": serializer.data
#                 },
                
#             )

#         return Response(
#             {
#                 "success": False,
#                 "errors": serializer.errors
#             },
            
#         )
    



#############################################Students###################################
# class Student(APIView):

#     def get(self,request):
#         student=Students.objects.all()
#         serializer= studentserializer(student,many=True)
#         return Response({
#                 'success':True,
#                 'message': 'Student List',
#                 'Data': serializer.data
#             }) 




#     def post(self,request):

#         serializer=studentserializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 'success':True,
#                 'message': 'Student added successfully',
#                 'Data': serializer.data
#             }) 
#         return Response({
#                 'success':False,
#                 'message': 'There is some error in adding Student',
#                 'Data': serializer.data
#             }) 



    
#     def patch(self,request):
#             student=Students.objects.get(id=request.data['id'])
#             serializer=studentserializer(student,data=request.data, partial=True)
#             if serializer.is_valid():
#                 print(serializer.errors)
#                 serializer.save()
#                 return Response({
#                     'success':True,
#                     'message': 'Student updated successfully',
#                     'Data': serializer.data
#                 }) 
#             return Response({
#                 'success':False,
#                 'message': 'Invalid ID',
#                 'Data': serializer.data
#             }) 
        

    
#     def delete(self,request):
#             student=Students.objects.get(id=request.data['id'])
#             student.is_archived = True
#             student.save()
#             return Response({
#                 'success':True,
#                 'message': 'Student deleted succesfully',
#                 'Data': None
#             }) 


# class Enrollment(APIView):


#     def get(self,request):
#         enrollment=Enrollments.objects.all()
#         serializer= EnrollmentSerializer(enrollment,many=True)
#         return Response({
#                 'success':True,
#                 'message': 'Enrollment List',
#                 'Data': serializer.data
#             })

#     def post(self, request):
#         serializer = EnrollmentSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {
#                     "success": True,
#                     "message": "Student enrolled successfully",
#                     "data": serializer.data
#                 },
               
#             )

#         return Response(
#             {
#                 "success": False,
#                 "errors": serializer.errors
#             },
            
#         )
    


    
#     def delete(self,request):
#             enrollment=Enrollments.objects.get(id=request.data['id'])
#             enrollment.is_archived = True
#             enrollment.save()
#             return Response({
#                 'success':True,
#                 'message': 'Enrollment deleted succesfully',
#                 'Data': None
#             }) 


# class Batch(APIView):

#     def get(self,request):
#         batch=Batches.objects.all()
#         serializer= BatchSerializer(batch,many=True)
#         return Response({
#                 'success':True,
#                 'message': 'Batch List',
#                 'Data': serializer.data
#             }) 


#     def post(self, request):
#         serializer = BatchSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 "success": True,
#                 "message": "Batch created  successfully",
#                 "Data":serializer.data
#             })

#         return Response(serializer.errors)
    
#     def patch(self,request):
#             batch=Batches.objects.get(id=request.data['id'])
#             serializer=BatchSerializer(batch,data=request.data, partial=True)
#             if serializer.is_valid():
#                 print(serializer.errors)
#                 serializer.save()
#                 return Response({
#                     'success':True,
#                     'message': 'Batch updated successfully',
#                     'Data': serializer.data
#                 }) 
#             return Response({
#                 'success':False,
#                 'message': 'Invalid ID',
#                 'Data': serializer.data
#             }) 
    

#     def delete(self,request):
#             batch=Batches.objects.get(id=request.data['id'])
#             batch.is_archived = True
#             batch.save()
#             return Response({
#                 'success':True,
#                 'message': 'Batch deleted succesfully',
#                 'Data': None
#             }) 
