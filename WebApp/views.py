from django.shortcuts import render

# Create your views here.
def base(request):
    return render(request, 'base.html')

def home(request):
    return render(request, 'home.html')

def services(request):
    return render(request, 'services.html')

def products(request):
    return render(request, 'products.html')

# def contact(request):
#     return render(request, 'contact.html')

# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.core.mail import send_mail
# from django.conf import settings
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags
# from .forms import ContactForm

# def contact(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             contact_submission = form.save()
            
#             # Email to Admin (you)
#             admin_subject = f'New Enquiry: {contact_submission.subject}'
#             admin_message = f"""
#             New enquiry received:
            
#             Name: {contact_submission.name}
#             Email: {contact_submission.email}
#             Subject: {contact_submission.subject}
#             Category: {contact_submission.get_category_display()}
#             Message: 
#             {contact_submission.message}
            
#             Submission Time: {contact_submission.submitted_at}
#             """
            
#             # Email to User (thank you)
#             user_subject = "Thank you for your enquiry"
#             user_message = render_to_string('emails/thank_you_email.html', {
#                 'name': contact_submission.name,
#                 'subject': contact_submission.subject,
#             })
#             text_user_message = strip_tags(user_message)
            
#             # Send both emails
#             send_mail(
#                 admin_subject,
#                 admin_message,
#                 settings.DEFAULT_FROM_EMAIL,
#                 [settings.ENQUIRY_EMAIL],
#                 fail_silently=False,
#             )
            
#             send_mail(
#                 user_subject,
#                 text_user_message,
#                 settings.DEFAULT_FROM_EMAIL,
#                 [contact_submission.email],
#                 html_message=user_message,
#                 fail_silently=False,
#             )
            
#             messages.success(request, 'Your enquiry has been submitted successfully!')
#             return redirect('contact')
#     else:
#         form = ContactForm()
    
#     return render(request, 'contact.html', {'form': form})

#####################################################################################################
# from django.core.mail import EmailMultiAlternatives, get_connection
# from django.conf import settings

# def contact(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             contact_submission = form.save()
            
#             # Prepare both emails first
#             admin_subject = f'New Enquiry: {contact_submission.subject}'
#             admin_message = f"""..."""  # Same as before
            
#             user_subject = "Thank you for your enquiry"
#             user_html_message = render_to_string(...)  # Same as before
#             user_text_message = strip_tags(user_html_message)
            
#             # Set up email connection
#             try:
#                 connection = get_connection()
#                 connection.open()
                
#                 # Create admin email (plain text)
#                 admin_email = EmailMultiAlternatives(
#                     admin_subject,
#                     admin_message,
#                     settings.DEFAULT_FROM_EMAIL,
#                     [settings.ENQUIRY_EMAIL],
#                     connection=connection,
#                 )
                
#                 # Create user email (HTML + text alternative)
#                 user_email = EmailMultiAlternatives(
#                     user_subject,
#                     user_text_message,
#                     settings.DEFAULT_FROM_EMAIL,
#                     [contact_submission.email],
#                     connection=connection,
#                 )
#                 user_email.attach_alternative(user_html_message, "text/html")
                
#                 # Send both emails in a single connection
#                 connection.send_messages([admin_email, user_email])
                
#             except Exception as e:
#                 # Log error but don't crash the form submission
#                 print(f"Email sending failed: {str(e)}")
#             finally:
#                 connection.close()
            
#             messages.success(request, 'Your enquiry has been submitted successfully!')
#             return redirect('contact')
#####################################################################################################

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives, get_connection
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import ContactForm
from .utils import send_logged_email  # Make sure you've created this utility function
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/h', block=True)
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_submission = form.save()
            
            # Prepare email content
            admin_subject = f'New Enquiry: {contact_submission.subject}'
            admin_message = f"""
            New enquiry received:
            
            Name: {contact_submission.name}
            Email: {contact_submission.email}
            Mobile: {contact_submission.mobile}
            Subject: {contact_submission.subject}
            Category: {contact_submission.get_category_display()}
            Message: 
            {contact_submission.message}
            
            Submission Time: {contact_submission.submitted_at}
            """
            
            # Prepare thank you email
            user_subject = "Thank you for your enquiry"
            user_html_message = render_to_string('emails/thank_you_email.html', {
                'name': contact_submission.name,
                'subject': contact_submission.subject,
            })
            user_text_message = strip_tags(user_html_message)
            
            # Send emails with logging and connection management
            try:
                # Option 1: Using the logged email utility (recommended)
                send_logged_email(
                    admin_subject,
                    admin_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.ENQUIRY_EMAIL],
                    submission=contact_submission
                )
                
                send_logged_email(
                    user_subject,
                    user_text_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [contact_submission.email],
                    html_message=user_html_message,
                    submission=contact_submission
                )
                
                # Option 2: Using direct connection management (alternative)
                """
                connection = get_connection()
                connection.open()
                
                # Admin email
                admin_email = EmailMultiAlternatives(
                    admin_subject,
                    admin_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.ENQUIRY_EMAIL],
                    connection=connection,
                )
                
                # User email
                user_email = EmailMultiAlternatives(
                    user_subject,
                    user_text_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [contact_submission.email],
                    connection=connection,
                )
                user_email.attach_alternative(user_html_message, "text/html")
                
                connection.send_messages([admin_email, user_email])
                connection.close()
                """
                
            except Exception as e:
                # Log error but don't crash the form submission
                print(f"Email sending failed: {str(e)}")
                # You might want to log this to your error tracking system
                
            messages.success(request, 'Your enquiry has been submitted successfully!')
            return redirect(request.META.get('HTTP_REFERER', 'contact'))
    
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})



def blog(request):
    return render(request, 'blog.html')

def faq(request):
    return render(request, 'faq.html')

def about(request):
    return render(request, 'aboutus.html')

def metal(request):
    return render(request, 'metal.html')

def agro_commodities(request):
    return render(request, 'agro_commodities.html')

def industrialproduct(request):
    return render(request, 'industrialproduct.html')

def frozen_foods(request):
    return render(request, 'frozen_foods.html')


from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages

from .models import ContactSubmission
from .utils import send_logged_email  # Optional if you're using it
@ratelimit(key='ip', rate='5/h', block=True)
def contact_submit(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        subject = request.POST.get("subject", "")
        category = request.POST.get("category", "general")
        message = request.POST.get("message", "")
        country = request.POST.get("country", "")
        # Save to database
        contact_submission = ContactSubmission.objects.create(
            name=name,
            email=email,
            mobile=mobile,
            country=country,
            subject=subject,
            category=category,
            message=message
        )

        # Prepare admin email
        admin_subject = f"New Enquiry: {subject}"
        admin_message = f"""
        New enquiry received:

        Name: {name}
        Email: {email}
        Mobile: {mobile}
        Subject: {subject}
        Category: {contact_submission.get_category_display()}
        Message:
        {message}

        Submission Time: {contact_submission.submitted_at}
        """

        # Prepare user thank-you email
        user_subject = "Thank you for your enquiry"
        user_html_message = render_to_string('emails/thank_you_email.html', {
            'name': name,
            'subject': subject,
        })
        user_text_message = strip_tags(user_html_message)

        try:
            # Preferred: using utility function to log & send
            send_logged_email(
                admin_subject,
                admin_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ENQUIRY_EMAIL],
                submission=contact_submission
            )

            send_logged_email(
                user_subject,
                user_text_message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                html_message=user_html_message,
                submission=contact_submission
            )

            # Fallback: directly use EmailMultiAlternatives
            """
            admin_email = EmailMultiAlternatives(
                admin_subject,
                admin_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ENQUIRY_EMAIL],
            )
            user_email = EmailMultiAlternatives(
                user_subject,
                user_text_message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
            user_email.attach_alternative(user_html_message, "text/html")
            admin_email.send()
            user_email.send()
            """

        except Exception as e:
            print(f"Email sending failed: {e}")

        messages.success(request, "Your enquiry has been submitted successfully!")
        return redirect("thank_you")  # or your desired thank-you page

    return redirect("home")

def business_consulting(request):
    return render(request, 'business_consulting.html')

def MerchantExporterServices(request):
    return render(request, 'MerchantExporterServices.html')

