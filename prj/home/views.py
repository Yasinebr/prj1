from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from post.models import Post, Comment, Like
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from post.forms import PostCreateUpdateForm, CommentCreateForm, CommentReplyForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'home/index.html', {'posts':posts})

class PostDetailView(View):
    form_class = CommentCreateForm
    form_class_reply = CommentReplyForm

    def setup(self, request, *args, **kwargs):
        self.post_istance = get_object_or_404(Post, pk=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, post_id, post_slug):
        comments = self.post_istance.pcomment.filter(is_reply=False)
        can_like = False
        if request.user.is_authenticated and self.post_istance.user_can_like(request.user):
            can_like = True
        return render(request, 'home/detail.html', {'post':self.post_istance, 'comments':comments,
        'form':self.form_class, 'reply_form':self.form_class_reply, 'can_like':can_like})

    method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_istance
            new_comment.save()
            messages.success(request, 'Your comment has been posted', 'success')
            return redirect('home:post', self.post_istance.id, self.post_istance. slug)

class DeletePostView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post,pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, 'post delete successfully', 'success')
            return redirect('home:home')
        else:
            messages.error(request, 'you are not allowed to delete this post', 'danger')
            return redirect('home:home')

class UpdatePostView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm
    template_name = 'home/update.html'

    def setup(self, request, *args, **kwargs):
        self.post_class = get_object_or_404(Post,pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_class
        if not post.user.id == request.user.id:
            messages.error(request, 'you cant update this post', 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_class
        form = self.form_class(instance=post)
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        post = self.post_class
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, 'post updated successfully', 'success')
            return redirect('home:post', post.pk, post.slug)
        else:
            messages.error(request, 'invalid form', 'danger')
            return render(request, 'home/update.html', {'form':form})

class CreatePostView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm
    template_name = 'home/create.html'

    def get(self, request , *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form':form})

    def post(self, request , *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'post created successfully', 'success')
            return redirect('home:post', new_post.id, new_post.slug)
        else:
            messages.error(request, 'invalid form', 'danger')
            return render(request, self.template_name, {'form':form})

class ReplyPostView(LoginRequiredMixin, View):
    form_class = CommentReplyForm

    def post(self, request, post_id, comment_id):
        post = get_object_or_404(Post, pk=post_id)
        comment = get_object_or_404(Comment, pk=comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request, 'post replayed successfully', 'success')
        return redirect('home:post', post.id, post.slug)

class LikePostView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        like = Like.objects.filter(post=post, user=request.user)
        if like.exists() :
            messages.error(request, 'You have already liked this post', 'danger')
        else:
            Like.objects.create(post=post, user=request.user)
            messages.success(request, 'post liked successfully', 'success')
        return redirect('home:post', post.id, post.slug)

