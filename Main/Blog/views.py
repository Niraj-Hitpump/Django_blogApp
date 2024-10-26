from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .form import *
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BlogModel


# View for the home page
def home(request):
    context = {'blogs': BlogModel.objects.filter(is_approved=True)}  # Filter approved blogs only
    return render(request, 'home.html', context)


# View for the about page
def about(request):
    return render(request, 'about.html')

# View for the contact page
def contact(request):
    return render(request, 'contact.html')

# View for the features page
def features(request):
    return render(request, 'features.html')

def blog_detail(request, slug):
    blog_obj = get_object_or_404(BlogModel, slug=slug)
    context = {'blog_obj': blog_obj}
    return render(request, 'blog_detail.html', context)


def see_blog(request):
    context = {}
    try:
        # Retrieve all blog objects for the current user
        blog_objects = BlogModel.objects.filter(user=request.user)
        context = {'blog_objects': blog_objects}
    except Exception as e:
        print(e)
    return render(request, 'see_blog.html', context)


def update_blog(request, slug):
    context = {}
    try:
        blog_obj = BlogModel.objects.get(slug=slug) 

        if request.method == 'POST':
            form = BlogForm(request.POST, request.FILES, instance=blog_obj) 

            
            blog_obj.title = request.POST.get('title')  # Update title manually
            if request.FILES.get('image'):  # Only update the image if a new one is uploaded
                blog_obj.image = request.FILES.get('image')

            if form.is_valid():
                form.save()  # Save the updated blog
                blog_obj.save()
                messages.success(request, 'Blog updated successfully!')
                return redirect('see_blog')  
        else:
            form = BlogForm(instance=blog_obj) 

        context['form'] = form
        context['blog_obj'] = blog_obj

    except BlogModel.DoesNotExist:
        messages.error(request, 'Blog not found.')
        return redirect('see_blog')

    except Exception as e:
        print(e)
        messages.error(request, f'Error: {e}')

    return render(request, 'update_blog.html', context)


def delete_blog(request, id):
    try:
        blog_obj = BlogModel.objects.get(id=id)
        if blog_obj.user == request.user:
            blog_obj.delete()
            messages.success(request, 'Blog deleted successfully.')
        else:
            messages.error(request, 'You do not have permission to delete this blog.')
    except BlogModel.DoesNotExist:
        messages.error(request, 'Blog not found.')
    except Exception as e:
        messages.error(request, f'Error: {e}')
        
    return redirect('see_blog')  # Use the name of the URL instead of hardcoded redirect





# View for handling user login
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Check if the user has entered the correct credentials
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # User is authenticated
            login(request, user)  # Correctly passing the 'request' and 'user' arguments
            return redirect('home')
        else:
            # Invalid credentials, redirect back to login page with an error message
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

# View for handling user logout
def logoutUser(request):
    logout(request)
    return redirect('home')



@login_required(login_url='/login/')  # Redirect to login page if the user is not logged in
def add_Blog(request):
    context = {'form': BlogForm()}
    try:
        if request.method == 'POST':
            form = BlogForm(request.POST, request.FILES)  # Include request.FILES to handle image uploads
            image = request.FILES.get('image')
            title = request.POST.get('title')
            user = request.user

            if form.is_valid():
                content = form.cleaned_data['content']

                # Create the blog with is_approved set to False
                BlogModel.objects.create(
                    user=user,
                    title=title,
                    content=content,
                    image=image,
                    is_approved=False  # Set to False by default
                )

                # Add success message
                messages.success(request, 'Your blog has been submitted and will be reviewed by an admin before being published.')

                # Redirect after the blog creation
                return redirect('see_blog')  # Redirect to 'see_blog' instead of the same page

    except Exception as e:
        print(e)
        messages.error(request, 'An error occurred while adding the blog.')

    return render(request, 'add_blog.html', context)

# # register
# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password'])
#             user.save()
#             login(request, user)
#             # Sending Welcome Email to New User.
#             subject = 'Welcome to Our Mblog!'
#             message = f'Hi {user.username},\n\nThank you for signing up on our blog platform. We hope you enjoy your stay!\n\nBest regards,\nThe Team'
#             recipient_list = [user.email]
#             send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
#             return redirect('home')
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'blog/register.html', {'form': form})



from django.contrib.admin.views.decorators import staff_member_required
@staff_member_required
def approve_blog(request, id):
    try:
        blog_obj = BlogModel.objects.get(id=id)
        blog_obj.is_approved = True  # Set is_approved to True
        blog_obj.save()
        messages.success(request, 'Blog approved successfully!')
    except BlogModel.DoesNotExist:
        messages.error(request, 'Blog not found.')
    except Exception as e:
        messages.error(request, f'Error: {e}')
        
    return redirect('see_blog')  # Redirect back to see_blog or admin page