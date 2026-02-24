from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings



class Subjects(models.Model):
    
    subject_name=models.CharField(max_length=100 , unique=True)
    is_archived=models.BooleanField(default=False)

    class Meta:
        db_table = 'subjects'


    def __str__(self):
        return self.subject_name
    



class User(AbstractUser):

    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("teacher", "Teacher"),
        ("student", "Student"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    subjects = models.ManyToManyField(
        "Subjects",
        blank=True,
        related_name="assigned_teachers"
    )

    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} - {self.role}"
    
class Courses(models.Model):
    course_name=models.CharField(max_length=100,unique=True)
    is_archived=models.BooleanField(default=False)
    subjects = models.ManyToManyField(Subjects, blank=True)
    
    class Meta:
        db_table='courses'
    
    def __str__(self):
        return self.course_name




    

class Batches(models.Model):
    batch_name=models.CharField(max_length=100, unique=True)
    is_archived=models.BooleanField(default=False)
    start_date=models.DateField(null=True, blank=True)
    duration=models.CharField(max_length=100)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='batches')
    
    
    class Meta:
        db_table='batches'

    def __str__(self):
        return self.batch_name

class SubjectTeacher(models.Model):
    batch=models.ForeignKey(Batches,on_delete=models.CASCADE,related_name="subject_teachers")
    subject=models.ForeignKey(Subjects, on_delete=models.CASCADE,related_name="batch_subjects")
    teacher = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="teacher_batches",
    limit_choices_to={"role": "teacher"}
)

    class Meta:
        db_table='subject_teacher'

    class Meta:
        db_table = "subject_teacher"
        unique_together = ("batch", "subject", "teacher")

    def __str__(self):
        return f"{self.batch.batch_name} - {self.subject.subject_name} - {self.teacher.username}"




class Enrollments(models.Model):

    batch = models.ForeignKey(
        Batches,
        on_delete=models.CASCADE,
        related_name="batch_enrollment"
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_enrollments",
        limit_choices_to={"role": "student"}
    )

    is_archived = models.BooleanField(default=False)



class Marks(models.Model):

    enrollment = models.ForeignKey(
        Enrollments,
        on_delete=models.CASCADE,
        related_name="student_marks"
    )

    subject = models.ForeignKey(
        Subjects,
        on_delete=models.CASCADE,
        related_name="subject_marks"
    )

    mark = models.IntegerField()

    class Meta:
        unique_together = ("enrollment", "subject")







##########################
# class Teachers(models.Model):
#     teacher_name=models.CharField(max_length=100)
#     is_archived=models.BooleanField(default=False)
#     subjects=models.ManyToManyField(Subjects,blank=True)

#     class Meta:
#         db_table='teachers'

#     def __str__(self):
#         return self.teacher_name
    


# class Marks(models.Model):
#     enrollment=models.ForeignKey(Enrollments,on_delete=models.CASCADE,related_name="student_mark")
#     course=models.ForeignKey(Courses,on_delete=models.CASCADE, related_name="course_mark")
#     subject=models.ForeignKey(Subjects,on_delete=models.CASCADE,related_name="subject_mark")
#     mark=models.IntegerField()

#     class Meta:
#         db_table="marks"s

    
#     def __str__(self):
#         return f"{self.enrollment.student.student_name} - {self.subject.subject_name}"


# class Enrollments(models.Model):
#     batch=models.ForeignKey(Batches,on_delete=models.CASCADE,related_name="batch_enrollment")
#     student=models.ForeignKey(Students, on_delete=models.CASCADE,related_name="student_enrollment")
#     is_archived=models.BooleanField(default=False)

#     class Meta:
#         db_table='Enrollment'
    
#     def __str__(self):
#         return f"{self.batch.batch_name} - {self.student.student_name}"

# class Students(models.Model):
#     student_name=models.CharField(max_length=100)
#     birth_date=models.DateField()
#     choices=[('Male','Male'),
#              ('Female','Female'),
#              ('Other','Other')]
#     gender=models.CharField(max_length=100, choices=choices)
#     is_archived=models.BooleanField(default=False)

#     class Meta:
#         db_table='students'
    
#     def __str__(self):
#         return self.student_name
