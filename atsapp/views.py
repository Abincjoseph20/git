from django.shortcuts import render,redirect,get_object_or_404
from .models import Resume 
import json  # Add this line at the top
import docx2txt
import fitz  # PyMuPDF
from .forms import ResumeForm
from django.http import FileResponse

JOB_KEYWORDS = {
    # Medical Field
    'doctor': ['mbbs', 'md', 'clinical', 'diagnosis', 'treatment', 'medical practice', 'patient care', 'hospital', 'medicine', 'surgeon', 'rounds'],
    'nurse': ['nursing', 'icu', 'patient care', 'hospital', 'emergency', 'bsc nursing', 'gnm', 'medication', 'vital signs', 'monitoring'],
    'pharmacist': ['pharmacy', 'medicines', 'dispensing', 'drug interactions', 'prescription', 'inventory', 'pharmacology'],
    'dentist': ['dental', 'oral care', 'cavity', 'tooth extraction', 'dentures', 'root canal', 'braces', 'clinic'],
    'physiotherapist': ['physiotherapy', 'rehabilitation', 'mobility', 'manual therapy', 'exercise therapy', 'pain relief'],
    'lab technician': ['lab', 'samples', 'microscope', 'blood test', 'pathology', 'reporting', 'equipment'],
    'medical transcriptionist': ['transcription', 'dictation', 'medical reports', 'audio typing', 'terminology', 'confidentiality'],

    # Legal Field
    'lawyer': ['legal', 'court', 'case', 'advocate', 'litigation', 'contract', 'legal advice', 'client', 'pleading'],
    'judge': ['judicial', 'hearing', 'judgment', 'case law', 'court', 'bench', 'verdict'],
    'legal advisor': ['legal advice', 'consultation', 'compliance', 'law', 'corporate law'],
    'notary public': ['notary', 'authentication', 'certify', 'affidavit', 'oath', 'documents'],
    'legal clerk': ['filing', 'case records', 'court assistance', 'scheduling', 'legal documentation'],

    # Technology Field
    'software developer': ['python', 'java', 'c++', 'git', 'api', 'backend', 'oop', 'debugging', 'programming'],
    'web developer': ['html', 'css', 'javascript', 'react', 'django', 'frontend', 'backend', 'node.js'],
    'frontend developer': ['html', 'css', 'javascript', 'react', 'ui', 'responsive design'],
    'backend developer': ['python', 'node.js', 'api', 'database', 'authentication', 'server'],
    'full-stack developer': ['frontend', 'backend', 'react', 'django', 'full-stack', 'api', 'ui'],
    'data analyst': ['excel', 'sql', 'powerbi', 'data cleaning', 'visualization', 'insights', 'tableau'],
    'data scientist': ['python', 'machine learning', 'data modeling', 'pandas', 'scikit-learn', 'statistics'],
    'cybersecurity expert': ['network security', 'firewall', 'ethical hacking', 'pen testing', 'vulnerabilities', 'encryption'],
    'mobile app developer': ['android', 'ios', 'flutter', 'react native', 'play store', 'xcode', 'ui/ux'],
    'cloud engineer': ['aws', 'azure', 'gcp', 'cloud computing', 'deployment', 'containers', 'kubernetes', 'docker'],
    'network engineer': ['networking', 'routing', 'switching', 'firewalls', 'vpn', 'lan', 'wan'],
    'robotic engineer': ['robotics', 'automation', 'control systems', 'mechatronics', 'sensors', 'actuators'],
    'blockchain developer': ['blockchain', 'smart contracts', 'ethereum', 'solidity', 'distributed ledger', 'decentralized'],
    'devops engineer': ['ci/cd', 'automation', 'docker', 'kubernetes', 'infrastructure', 'monitoring'],
    'ai engineer': ['artificial intelligence', 'machine learning', 'neural networks', 'deep learning', 'nlp', 'automation'],
    'iot developer': ['internet of things', 'sensors', 'automation', 'smart devices', 'raspberry pi', 'arduino'],
    'marketing': ['branding', 'digital marketing', 'content creation', 'SEO', 'social media', 'email marketing'],
    'sales': ['lead generation', 'sales strategy', 'negotiation', 'client relationship', 'CRM', 'cold calling'],
    'php developer' : [
        'php','laravel','codeigniter','symfony',
        'oop','mysql','postgresql',
        'database_management','rest_api','soap_api','html','css',
        'javascript','jquery','ajax','version_control','git','mvc',
        'debugging','backend','composer','deployment','server_management','linux',
        'api_integration','problem_solving','unit_testing','secure_coding'
    ],
    
    # 'HR Recruiter' :[  
    #     'talent acquisition', 'candidate sourcing', 'applicant tracking systems (ATS)',  
    #     'LinkedIn Recruiter', 'job post optimization', 'employer branding',  
    #     'interview coordination', 'workforce planning', 'compensation benchmarking',  
    #     'diversity hiring', 'HR compliance', 'behavioral interviewing',  
    #     'candidate assessment', 'onboarding strategies', 'employee retention',  
    #     'Glassdoor management', 'Boolean search', 'HR analytics', 'ATS integrations',  
    #     'EEOC compliance', 'cold outreach', 'job market analysis', 'salary negotiations',  
    #     'workday recruitment', 'greenhouse software', 'indeed hiring platform',  
    #     'candidate pipelining', 'skills gap analysis', 'recruitment marketing'  
    #     ]
}

def extract_text_from_docx(file_path):
    return docx2txt.process(file_path)

def extract_text_from_pdf(file_path):
    text = ""
    doc = fitz.open(file_path)
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def ats_score(resume_text, job_role):
    keywords = JOB_KEYWORDS.get(job_role.lower(), [])
    print(f"Keywords for {job_role}: {keywords}")
    score = 0
    matched = []
    for keyword in keywords:
        if keyword.lower() in resume_text.lower():
            score += 1
            matched.append(keyword)
            print(f"Matched: {keyword}")
    total = len(keywords)
    if total == 0:
        return "No keywords found for selected role.", []
    percentage = (score / total) * 100
    print(percentage)
    return f"ATS Score: {score}/{total} ({percentage:.0f}%)", matched
    

def upload_resume(request):
    result = None
    matched_keywords = []
    selected_role = None
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        selected_role = request.POST.get('job_role')
        
        # Debugging: Check if form is valid and job_role is present
        print(f"Form valid: {form.is_valid()}")
        print(f"Selected Role: {selected_role}")
        
        if form.is_valid() and selected_role:
            resume = form.save()
            file_path = resume.file.path
            
            # Debugging: Ensure the file is correctly uploaded
            print(f"File path: {file_path}")
            
            try:
                if file_path.endswith('.docx'):
                    resume_text = extract_text_from_docx(file_path)
                elif file_path.endswith('.pdf'):
                    resume_text = extract_text_from_pdf(file_path)
                else:
                    resume_text = ""
                
                # Debugging: Check if resume text is extracted properly
                print(f"Extracted Text: {resume_text[:500]}")  # Print first 500 characters of text

                if resume_text:
                    result, matched_keywords = ats_score(resume_text, selected_role)
                    if "ATS Score:" in result:
                        try:
                            percentage = float(result.split('(')[1].split('%')[0])
                            resume.ats_score = percentage
                        except (IndexError, ValueError):
                            resume.ats_score = 0
                    else:
                        resume.ats_score = 0
                    
                    resume.matched_keywords = json.dumps(matched_keywords)
                    resume.raw_text = resume_text
                    resume.job_role = selected_role
                    resume.save()
                else:
                    result = "No text extracted from the resume."
            except Exception as e:
                result = f"Error reading file: {str(e)}"
        else:
            result = "Form is not valid or job role is not selected."
    else:
        form = ResumeForm()

    return render(request, 'upload.html', {
        'form': form,
        'result': result,
        'matched': matched_keywords,
        'roles': JOB_KEYWORDS.keys(),
        'selected_role': selected_role
    })



def high_score_resumes(request):
    # Get resumes with ATS score > 50%
    high_scoring_resumes = Resume.objects.filter(ats_score__gt=50).order_by('-ats_score')
    return render(request, 'high_score_resumes.html', {'resumes': high_scoring_resumes})

  
def resume_detail(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    file_url = request.build_absolute_uri(resume.file.url)  
    is_pdf = file_url.endswith('.pdf')
    
    return render(request, 'resume_detail.html',{
        'resume': resume,
        'file_url': file_url,
        'is_pdf': is_pdf
        
        })

def resume_detail(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    
    # Get the file URL
    file_url = resume.file.url if resume.file else None
    
    # Determine if the file is a PDF (for preview)
    is_pdf = file_url.lower().endswith('.pdf') if file_url else False

    context = {
        'resume': resume,
        'file_url': request.build_absolute_uri(file_url) if file_url else None,
        'is_pdf': is_pdf
    }

    return render(request, 'resume_detail.html', context)


def resume_detail(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    file_url = resume.file.url if resume.file else None
    is_pdf = file_url.lower().endswith('.pdf') if file_url else False

    return render(request, 'resume_detail.html', {
        'resume': resume,
        'file_url': file_url,
        'is_pdf': is_pdf
    })


def download_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    response = FileResponse(open(resume.file.path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{resume.file.name}"'
    return response



def resume_filter(request):
    job_role = request.GET.get('job_role', None)
    min_score = request.GET.get('min_score', 0)
    
    try:
        min_score = float(min_score)
    except (ValueError, TypeError):
        min_score = 0
    
    resumes = Resume.objects.all()
    
    if job_role:
        resumes = resumes.filter(job_role__iexact=job_role)
    
    resumes = resumes.filter(ats_score__gte=min_score).order_by('-ats_score')
    
    return render(request, 'filter.html', {
        'resumes': resumes,
        'roles': JOB_KEYWORDS.keys(),
        'selected_role': job_role,
        'min_score': min_score
    })
    
    
def home(request):
    return render(request,'home.html')
