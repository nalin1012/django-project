from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from rest_framework.viewsets import ModelViewSet # ModelViewSet - To automatically get all CRUD operations
from .models import Post, Comment
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated # Built-in permission class
from .permissions import IsAuthorOrReadOnly # Importing your custom permission
from .forms import PostCreateForm, SignUpForm, CommentForm

# Create your views here.

# Creating a ViewSet for Post - To handle all crud operations in one class
class PostViewSet(ModelViewSet):
    
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    # Only logged-in users can access API
    # Applying multiple permissions
    # IsAuthenticated - Only logged-in users can access
    # IsAuthorOrReadOnly - Only author can edit/delete
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        # Automatically assign logged-in user as author
        serializer.save(author=self.request.user)


def home_view(request):
    posts = Post.objects.select_related('author').order_by('-created_at')
    
    # Pagination: 6 posts per page
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'home.html', {'page_obj': page_obj, 'posts': page_obj.object_list})


def blog_detail_view(request, pk):
    post = get_object_or_404(Post.objects.select_related('author').prefetch_related('comments'), pk=pk)
    comments = post.comments.all()
    comment_form = CommentForm()
    is_author = post.author == request.user
    user_liked = False
    if request.user.is_authenticated:
        user_liked = post.likes.filter(id=request.user.id).exists()
    
    return render(request, 'blog_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'is_author': is_author,
        'user_liked': user_liked
    })


@login_required
def like_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        messages.success(request, 'Post unliked.')
    else:
        post.likes.add(request.user)
        messages.success(request, 'Post liked!')
    return redirect('blog-detail', pk=pk)


@login_required
def add_comment_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment posted successfully!')
            return redirect('blog-detail', pk=pk)
    return redirect('blog-detail', pk=pk)


@login_required
def delete_comment_view(request, post_pk, comment_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    
    if comment.author == request.user or post.author == request.user:
        comment.delete()
        messages.success(request, 'Comment deleted.')
    else:
        messages.error(request, 'You cannot delete this comment.')
    
    return redirect('blog-detail', pk=post_pk)


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = SignUpForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Account created successfully.')
        return redirect('home')
    return render(request, 'signup.html', {'form': form})


@login_required
def create_post_view(request):
    form = PostCreateForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        messages.success(request, 'Post created successfully.')
        return redirect('blog-detail', pk=post.pk)
    return render(request, 'create_post.html', {'form': form})


@login_required
def edit_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if post.author != request.user:
        messages.error(request, 'You cannot edit this post.')
        return redirect('blog-detail', pk=pk)
    
    form = PostCreateForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Post updated successfully.')
        return redirect('blog-detail', pk=pk)
    
    return render(request, 'edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if post.author != request.user:
        messages.error(request, 'You cannot delete this post.')
        return redirect('blog-detail', pk=pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully.')
        return redirect('home')
    
    return render(request, 'confirm_delete.html', {'post': post})
