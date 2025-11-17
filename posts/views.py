from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Post
from .forms import PostForm
from django.http import JsonResponse
from django.template.loader import render_to_string


def home_view(request):
    """Home page: display posts and a form to create new ones.

    Only authenticated users can POST to create posts; anonymous users see the
    form disabled with links to login/signup.
    """
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created')
            # If AJAX, return JSON containing rendered HTML for the new post
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                html = render_to_string('post_item.html', {'post': post, 'user': request.user}, request=request)
                return JsonResponse({'success': True, 'html': html})
            return redirect('home')
    else:
        form = PostForm()

    posts_qs = Post.objects.order_by('-created_at')
    paginator = Paginator(posts_qs, 10)  # 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {'all_posts_list': page_obj, 'form': form, 'page_obj': page_obj})


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created and logged in')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    """Log the user out and redirect to the login page."""
    logout(request)
    return redirect('login')


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, 'You do not have permission to edit this post')
        return redirect('home')
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated')
            # respond to AJAX with updated item HTML
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                html = render_to_string('post_item.html', {'post': post, 'user': request.user}, request=request)
                return JsonResponse({'success': True, 'html': html})
            return redirect('home')
    else:
        form = PostForm(instance=post)
    # If AJAX GET, return form HTML fragment
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form_html = render_to_string('post_edit_form.html', {'form': form, 'post': post}, request=request)
        return JsonResponse({'form_html': form_html})
    return render(request, 'post_edit.html', {'form': form, 'post': post})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, 'You do not have permission to delete this post')
        return redirect('home')
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted')
        # If AJAX, return JSON with pk
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'pk': pk})
        return redirect('home')
    return render(request, 'post_confirm_delete.html', {'post': post})


def about_view(request):
    """About page."""
    return render(request, 'about.html')


def contact_view(request):
    """Contact page."""
    return render(request, 'contact.html')


def help_view(request):
    """Help page."""
    return render(request, 'help.html')
