from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .form import *
from django.contrib import messages
from django.shortcuts import render, get_object_or_404

from .models import BlogModel


# View for the home page
def home(request):
    context={'blogs': BlogModel.objects.all()}
    return render(request, 'home.html',context)

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
        blog_obj = BlogModel.objects.get(slug=slug)  # Get the specific blog object

        if request.method == 'POST':
            form = BlogForm(request.POST, request.FILES, instance=blog_obj)  # Bind the form with POST data and files

            # Manually handle the title and image if needed
            blog_obj.title = request.POST.get('title')  # Update title manually
            if request.FILES.get('image'):  # Only update the image if a new one is uploaded
                blog_obj.image = request.FILES.get('image')

            if form.is_valid():
                form.save()  # Save the updated blog
                blog_obj.save()  # Save the changes to the blog object
                messages.success(request, 'Blog updated successfully!')
                return redirect('see_blog')  # Redirect to see_blog after success
        else:
            form = BlogForm(instance=blog_obj)  # Prepopulate the form with current data

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



def add_Blog(request):
    context = {'form': BlogForm()}
    try:
        if request.method == 'POST':
            form = BlogForm(request.POST)
            image = request.FILES.get('image')
            title = request.POST.get('title')
            user = request.user

            if form.is_valid():
                content = form.cleaned_data['content']

                # Create the blog
                BlogModel.objects.create(
                    user=user,
                    title=title,
                    content=content,
                    image=image
                )
                
                # Add success message
                messages.success(request, 'Your blog has been created successfully!')

                # Redirect after the blog creation
                return redirect('/blog/add_blog/')

    except Exception as e:
        print(e)

    return render(request, 'add_blog.html', context)