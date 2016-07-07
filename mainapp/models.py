from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=128)
    room = models.IntegerField()
    idno = models.CharField(max_length=20)
    hostel = models.CharField(max_length=10)
    sex = models.BooleanField()
    views = models.IntegerField(default=0)
    number_of_comments = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Comment(models.Model):
    student = models.ForeignKey(Student)
    title = models.TextField()
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def short_content(self):
        if len(self.content)>50:
            return self.content[0:50]+'...'
        else:
            return self.content
    def short_title(self):
        if len(self.title)>50:
            return self.title[0:50]+'...'
        else:
            return self.title
    def __str__(self):
        return self.title
