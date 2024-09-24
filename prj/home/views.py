from django.contrib.messages import success
from django.shortcuts import render, redirect
from django.views import View
from post.models import Post
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from post.forms import PostUpdateForm
from django.utils.text import slugify

class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'home/index.html', {'posts':posts})

class PostDetailView(View):
    def get(self, request, post_id, post_slug):
        post = Post.objects.get(pk=post_id, slug=post_slug)
        return render(request, 'home/detail.html', {'post':post})

class DeletePostView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, 'post delete successfully', 'success')
            return redirect('home:home')
        else:
            messages.error(request, 'you are not allowed to delete this post', 'danger')
            return redirect('home:home')

class UpdatePostView(LoginRequiredMixin, View):
    form_class = PostUpdateForm
    template_name = 'home/update.html'

    def setup(self, request, *args, **kwargs):
        self.post_class = Post.objects.get(pk=kwargs['post_id'])
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