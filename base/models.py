from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#class is the model/table and the attributes are the columns of that table 

class Task(models.Model):
    user= models.ForeignKey(User, on_delete= models.CASCADE, null=True, blank= True)
    title= models.CharField(max_length=50)
    description= models.TextField(null=True, blank=True)
    complete= models.BooleanField(default=False)
    created= models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.title
    
    #any complete model shld be sent at the bottom of the list because its done and we need to do deal with it 
    class Meta:
        ordering= ['complete']
