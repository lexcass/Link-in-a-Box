from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, UserLoginForm, ClipboardUpdateForm #, ForgotPasswordForm
from .models import Clipboard
from .functions import generate_key



# Register the user
# Display a form asking the user to set their email, username, and password
# for access to the app.
def register_user(request):
    template_name = 'user_registration.html'
    form = UserRegistrationForm()

    # Create the user and create a clipboard for the user
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            #send_confirmation_email(user, request.get_host())
            # Send a confirmation email to the user so that they can activate their account.

            # Get the protocol for the verification link used in the email.
            user_profile = user.userprofile

            # Generate confirmation code
            # Set the confirmation_code for the user's profile to test against the
            # confirmation code they provide when activating their account.
            confirmation_code = generate_key()
            user_profile.confirmation_code = confirmation_code
            user_profile.save()

            html = render_to_string('registration/confirmation_email.html', {
                'protocol': request.scheme,
                'domain': request.get_host(),
                'uid': user.id,
                'confirmation_code': confirmation_code
            })
            text = strip_tags(html)

            email_message = EmailMultiAlternatives(
                'CopyPaste Email Confirmation',
                text,
                'alexcassady22@gmail.com',
                [user.email]
            )
            email_message.attach_alternative(html, "text/html")
            email_message.send()
            return redirect('/confirmation_sent')

    return render(request, template_name, { 'form': form })

# Page the user is taken to informing them that a confirmation email has been sent.
def confirmation_sent(request):
    return render(request, 'registration/confirmation_sent.html')

# Confirm the user's email and activate their account
# The user is redirected to this view via the link with their confirmation code.
# If it matches the one assigned to their UserProfile in the database,
# their user account becomes active (email_confirmed = True).
def confirm_email(request, user_id, confirmation_code):
    message = "Failed to activate account. The user doesn't exist or their email is already confirmed."
    confirmed = False

    user = User.objects.filter(id=user_id).first()
    user_profile = user.userprofile
    if user is not None and not user_profile.email_confirmed:
        if user_profile.confirmation_code == confirmation_code:
            message = 'Your account has been activated!'
            user_profile.activate()
            confirmed = True

    return render(request, 'registration/confirmation_complete.html', {
        'message': message,
        'confirmed': confirmed
    })


# Login the user
# Display a form asking the user to provide their login credentials (username and password),
# so that they may access their clipboard.
def login_user(request):
    template_name = 'user_login.html'
    form_class = UserLoginForm
    form = form_class()
    message = ""

    if request.method == 'POST':
        message = "Username and password didn't match. Please try again."
        form = form_class(request.POST)
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None and user.is_active:
            if user.userprofile is not None:
                if user.userprofile.email_confirmed:
                    message = ""
                    login(request, user)
                    return redirect('/create_box')

    # Redirect user to clipboard if they are already logged in
    if request.user.is_authenticated:
        return redirect('/my_box')

    return render(request, template_name, {
        'form': form,
        'message': message
    })

# Logout the user
def logout_user(request):
    logout(request)
    return redirect('/login')



# Create a clipboard
# After a new user is registered, a clipboard is created for them.
# So, the user is redirected to this view before being redirected
# to the login page.
def create_clipboard(request):
    user = request.user

    if user.is_authenticated():
        # Create a clipboard for first login
        # Prevent duplicate clipboards for a single user
        if user.clipboard_set.count() < 1:
            clipboard = Clipboard(user=user, content='')
            clipboard.save()

        # Show the user their clipboard, if they already have one
        # and don't create another one.
        return redirect('/my_box', permanent=True)

    return redirect('/login')


# Show the user their clipboard
# Display the contents of the user's clipboard so that they may
# copy its contents or update its contents.
def show_clipboard(request):
    template_name = 'show_clipboard.html'
    user = request.user
    form = ClipboardUpdateForm()

    # Redirect the user to the login page if they try to directly access their
    # clipboard without loggin in
    if not user.is_authenticated():
        return redirect('/login')

    clipboard = user.clipboard_set.first()

    # Process
    if request.method == "POST":
        form = ClipboardUpdateForm(request.POST)
        if form.is_valid():
            clipboard = form.process(clipboard)

    return render(request, template_name, {
        'form': form,
        'clipboard': clipboard
    })


# Help page
def help(request):
    return render(request, 'help.html')
