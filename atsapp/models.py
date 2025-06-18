from django.db import models
import json

CATEGORY_CHOICE = (
    ('10th', '10th'),
    ('12th', '12th'),
    ('Diploma', 'Diploma'),
    ('UG', 'Undergraduate'),
    ('PG', 'Postgraduate'),
    ('MBA', 'Master of Business Administration'),
    ('MCA', 'Master of Computer Applications'),
    ('PhD', 'Doctor of Philosophy'),
    ('BTech', 'Bachelor of Technology'),
    ('MTech', 'Master of Technology'),
    ('BSc', 'Bachelor of Science'),
    ('MSc', 'Master of Science'),
    ('BA', 'Bachelor of Arts'),
    ('MA', 'Master of Arts'),
    ('BCom', 'Bachelor of Commerce'),
    ('MCom', 'Master of Commerce'),
    ('LLB', 'Bachelor of Laws'),
    ('LLM', 'Master of Laws'),
    ('BBA', 'Bachelor of Business Administration'),
    ('BCA', 'Bachelor of Computer Applications'),
)


class Resume(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10,default='91+00000000')
    qualification = models.CharField(choices=CATEGORY_CHOICE,max_length=15)
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    job_role = models.CharField(max_length=255, default='Not Specified')
    ats_score = models.FloatField(default=0)
    matched_keywords = models.TextField()
    raw_text = models.TextField(blank=True, null=True)
    
    
    def set_matched_keywords(self, keywords):
        self.matched_keywords = json.dumps(keywords)
    
    def get_matched_keywords(self):
        return json.loads(self.matched_keywords)
    
    def __str__(self):
        return f"{self.job_role} - {self.ats_score}%"