from rest_framework import serializers
from .models import *

class subjectserializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = ["id", "subject_name"]


from rest_framework import serializers
from .models import User, Subjects

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    subjects = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Subjects.objects.all(),
        required=False
    )

    subjects_details = subjectserializer(
        source="subjects",
        many=True,
        read_only=True
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "role",
            "is_archived",
            "subjects",
            "subjects_details"
        ]

    def create(self, validated_data):
        subjects = validated_data.pop("subjects", [])
        password = validated_data.pop("password")

        user = User.objects.create(**validated_data)
        user.set_password(password)   
        user.save()

        user.subjects.set(subjects)
        return user
 
class courseserializer(serializers.ModelSerializer):
    subjects=serializers.PrimaryKeyRelatedField(many=True,queryset=Subjects.objects.all(),write_only=True)
    subjects_details = subjectserializer(
        source='subjects',
        many=True,
        read_only=True
    )
    class Meta:
        model = Courses
        fields = ["id", "course_name", "is_archived","subjects", "subjects_details"]
    



###################################Batch##############################################################


class SubjectTeacherSerializer(serializers.ModelSerializer):

    subject_name = serializers.CharField(
        source="subject.subject_name",
        read_only=True
    )

    teacher_name = serializers.CharField(
        source="teacher.username",
        read_only=True
    )

    class Meta:
        model = SubjectTeacher
        fields = [
            "subject",
            "subject_name",
            "teacher",
            "teacher_name"
        ]
    



class BatchSerializer(serializers.ModelSerializer):

    subject_teachers = SubjectTeacherSerializer(many=True)
    course_name = serializers.CharField(
        source="course.course_name",
        read_only=True
    )

    class Meta:
        model = Batches
        fields = [
            "id",
            "batch_name",
            "start_date",
            "duration",
            "course",
            "course_name",
            "subject_teachers"
        ]

    def create(self, validated_data):
        subject_teachers_data = validated_data.pop("subject_teachers")
        batch = Batches.objects.create(**validated_data)

        course_subject_ids = list(
            batch.course.subjects.values_list("id", flat=True)
        )

        for item in subject_teachers_data:
            subject = item["subject"]
            teacher = item["teacher"]

            
            if subject.id not in course_subject_ids:
                raise serializers.ValidationError(
                    f"{subject.subject_name} not part of course."
                )

            
            if not teacher.subjects.filter(id=subject.id).exists():
                raise serializers.ValidationError(
                    f"{teacher.username} does not teach {subject.subject_name}."
                )

            SubjectTeacher.objects.create(
                batch=batch,
                subject=subject,
                teacher=teacher
            )

        return batch



class EnrollmentSerializer(serializers.ModelSerializer):

    student_name = serializers.CharField(
        source="student.username",
        read_only=True
    )

    batch_name = serializers.CharField(
        source="batch.batch_name",
        read_only=True
    )

    class Meta:
        model = Enrollments
        fields = [
            "id",
            "batch",
            "batch_name",
            "student",
            "student_name",
            "is_archived"
        ]

    def validate(self, data):
        batch = data.get("batch")
        student = data.get("student")

        if student.role != "student":
            raise serializers.ValidationError(
                "Selected user is not a student."
            )

        if batch.is_archived:
            raise serializers.ValidationError(
                "Cannot enroll in archived batch."
            )

        if student.is_archived:
            raise serializers.ValidationError(
                "Archived student cannot enroll."
            )

        if Enrollments.objects.filter(
            batch=batch,
            student=student
        ).exists():
            raise serializers.ValidationError(
                "Student already enrolled."
            )

        return data
    

class MarksSerializer(serializers.ModelSerializer):

    batch_name = serializers.CharField(
        source="enrollment.batch.batch_name",
        read_only=True
    )
    course_name=serializers.CharField(source="enrollment.batch.course.course_name",read_only=True)

    student_name = serializers.CharField(
        source="enrollment.student.username",
        read_only=True
    )

    subject_name = serializers.CharField(
        source="subject.subject_name",
        read_only=True
    )

    class Meta:
        model = Marks
        fields = [
            "id",
            "enrollment",
            "batch_name",
            "course_name",
            "student_name",
            "subject",
            "subject_name",
            "mark"
        ]

    def validate(self, data):
        enrollment = data.get("enrollment")
        subject = data.get("subject")

        
        if not enrollment.batch.course.subjects.filter(id=subject.id).exists():
            raise serializers.ValidationError(
                "Subject does not belong to student's course."
            )

        
        if Marks.objects.filter(
            enrollment=enrollment,
            subject=subject
        ).exists():
            raise serializers.ValidationError(
                "Marks already assigned."
            )

        return data




























#############################################################################################################
# class MarksSerializer(serializers.ModelSerializer):

    
#     batch_name = serializers.CharField(
#         source="enrollment.batch.batch_name",
#         read_only=True
#     )

#     student_name = serializers.CharField(
#         source="enrollment.student.student_name",
#         read_only=True
#     )

#     course_name = serializers.CharField(
#         source="course.course_name",
#         read_only=True
#     )

#     subject_name = serializers.CharField(
#         source="subject.subject_name",
#         read_only=True
#     )

#     class Meta:
#         model = Marks
#         fields = [
#             "id",
#             "enrollment",
#             "batch_name",
#             "student_name",
#             "course",
#             "course_name",
#             "subject",
#             "subject_name",
#             "mark"
#         ]
    

#         def validate(self, data):
#             enrollment = data.get("enrollment")
#             course = data.get("course")
#             subject = data.get("subject")

            
#             if not course.subjects.filter(id=subject.id).exists():
#                 raise serializers.ValidationError(
#                     "Subject does not belong to selected course."
#                 )

            
#             if enrollment.batch.course.id != course.id:
#                 raise serializers.ValidationError(
#                     "Course does not match student's batch course."
#                 )

            
#             if Marks.objects.filter(
#                 enrollment=enrollment,
#                 subject=subject
#             ).exists():
#                 raise serializers.ValidationError(
#                     "Marks already assigned for this subject."
#                 )

#             return data









# class UserSerializer(serializers.ModelSerializer):

#     subjects = serializers.PrimaryKeyRelatedField(
#         many=True,
#         queryset=Subjects.objects.all(),
#         required=False
#     )

#     subjects_details = subjectserializer(
#         source="subjects",
#         many=True,
#         read_only=True
#     )

#     class Meta:
#         model = User
#         fields = [
#             "id",
#             "username",
#             "first_name",
#             "last_name",
#             "email",
#             "role",
#             "is_archived",
#             "subjects",
#             "subjects_details"
#         ]


# class enrollmentserializer(serializers.ModelSerializer):

#     student_name = serializers.CharField(
#         source="student.student_name",
#         read_only=True
#     )

#     batch_name = serializers.CharField(
#         source="batch.batch_name",
#         read_only=True
#     )

#     class Meta:
#         model = Enrollments
#         fields = [
#             "id",
#             "batch",
#             "batch_name",
#             "student",
#             "student_name",
#             "is_archived"
#         ]
#         read_only_fields = ["is_archived"]

#     def validate(self, data):
#         batch = data.get("batch")
#         student = data.get("student")

        
#         if batch.is_archived:
#             raise serializers.ValidationError(
#                 "Cannot enroll in archived batch."
#             )

       
#         if student.is_archived:
#             raise serializers.ValidationError(
#                 "Archived student cannot be enrolled."
#             )

        
#         if Enrollments.objects.filter(
#             batch=batch,
#             student=student,
#             is_archived=False
#         ).exists():
#             raise serializers.ValidationError(
#                 "Student already enrolled in this batch."
#             )

#         return data


# class batchserializer(serializers.ModelSerializer):

#     subject_teachers = subjectteacherserializer(many=True)
#     course_name = serializers.CharField(
#         source="course.course_name",
#         read_only=True
#     )

   

#     class Meta:
#         model = Batches
#         fields = [
#             "id",
#             "batch_name",
#             "start_date",
#             "duration",
#             "course",
#             "course_name",
#             "subject_teachers"
#         ]

#     def create(self, validated_data):
#         subject_teachers_data = validated_data.pop("subject_teachers")
#         batch = Batches.objects.create(**validated_data)

        
#         course_subject_ids = batch.course.subjects.values_list("id", flat=True)

#         for item in subject_teachers_data:
#             subject = item["subject"]
#             teacher = item["teacher"]

            
#             if subject.id not in course_subject_ids:
#                 raise serializers.ValidationError(
#                     f"{subject.subject_name} is not part of selected course."
#                 )

            
#             teacher_subject_ids = teacher.subjects.values_list("id", flat=True)

#             if subject.id not in teacher_subject_ids:
#                 raise serializers.ValidationError(
#                     f"{teacher.teacher_name} does not teach {subject.subject_name}."
#                 )

#             Subject_teacher.objects.create(
#                 batch=batch,
#                 subject=subject,
#                 teacher=teacher
#             )
    
#         return batch






