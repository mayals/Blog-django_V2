from django.shortcuts import render,get_object_or_404,redirect
from django.db.models import Count
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
from django.views.generic import CreateView, UpdateView, DeleteView,FormView
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy

from .models import Post,Comment
from .forms import PostCreateForm, PostShareForm, PostSearchForm, CommentCreateForm 

from taggit.models import Tag
from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank
from django.contrib.postgres.search import TrigramSimilarity         #-- not work !



# -----------------# posts all display # # filter by tag_slug-----------------------------------------------#
def posts_view(request,tag_slug=None): 
    posts = Post.objects.filter(p_status='p')
    
    # filter by tag_slug 
    # ---tag -- belong show all posts-----   
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(p_tags__in=[tag])
       
    #--- paginator -- belong show all posts--------
    paginator = Paginator(posts, 4)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_page)

    # ----context for post_all_show ---
    context = {
        'title': 'Posts',
        'posts': posts,
        'page' : page,
        'tag'  : tag,
    }
    return render(request,'blog/posts.html',context)




# -----------------# advanced search display # -----------------------------------------------#
def advanced_search(request):
    context = {
    }
    return render(request,'blog/advanced_search.html',context)




# -----------------# search results display # -----------------------------------------------#
def search_results(request):
    posts = None
    src_subj     = None
    src_body     = None
    tit_sub      = None
    tit_body     = None

    posts = Post.objects.all().filter(p_status='p')
    
    # search by subject ---
    if 'src_subj' in request.GET:
        src_subj = request.GET['src_subj']
        if src_subj :
            posts = posts.filter(P_subject__icontains=src_subj)
            tit_subj = 'you are search about Posts Subject : {}'.format(src_subj)

    # search by body ---
    if 'src_body' in request.GET:
        src_body = request.GET['src_body']
        if src_body:
            posts = posts.filter(p_body__icontains=src_body)
            tit_body = 'you are search about Posts Body  : {}'.format(src_body)
        
    context = {
        'tit_sub':tit_subj,
        'src_subj': src_subj ,
        'tit_body':tit_body,
        'src_body' : src_body ,
        'posts_result' : posts, 
    }
    return render(request,'blog/search_results.html',context)





# -----------------# post detail # -----------------------------------------------#
# -- post detail display + comments about this post display +  create comment form  #--------
def post_detail(request,post_id):
    # post detail display
    post  = get_object_or_404(Post,id=post_id, p_status='p' )
    # comments about this post display
    post_comments = Comment.objects.filter(c_post=post, c_status='p')
    
    # -- form for add new commment for this selected post 
    new_comment = None
    comment_form = CommentCreateForm()
    if request.method == 'POST':
        comment_form = CommentCreateForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.c_post = post
            new_comment.save()
            messages.success(request,'Thank you for add comment')   
        else :
            messages.warning(request, 'please complete * fields')  
            
   # -- List of similar posts of the selected post
    post_tags_ids = post.p_tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(p_status='p').filter(p_tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('p_tags')).order_by('-same_tags','-p_published_at')[:4]
 
    context = {
        'post':post,
        'comment_form': comment_form,
        'new_comment': new_comment,
        'comments': post_comments,
        'similar_posts': similar_posts,
    }
    return render(request,'blog/post_detail.html',context)
 




# -----------------#  post share Form & send email to admin  # -----------------------------------------------#
def post_share_email(request,post_id):
    post_shared = get_object_or_404(Post, id=post_id, p_status='p')
    post_url = request.build_absolute_uri(post_shared.get_absolute_url())
    share_form = PostShareForm()
    sent = False
    if request.method == 'POST' :
        share_form = PostShareForm(request.POST)
        if share_form.is_valid():
            cd = share_form.cleaned_data
            subject = '{} ({}) recommends you reading "{}"'.format(cd['sender_name'], cd['sender_email'], post_shared.p_subject)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post_shared.p_subject, post_url, cd['sender_name'], cd['sender_comment'])
            # send email from 'admin email' to 'receiver email' contain sender subject comment on the shared post ----
            send_mail(subject, message, 'admin@myblog.com',[cd['share_to_email']])
            sent = True
            messages.success(request,'Thank you for share the post')
            return redirect('blog:posts')
        
        else:
            messages.warning(request,'Please enter valid information')

       # post_url = request.build_absolute_uri(post.get_absolute_url())
            # subject = '{} ({}) recommends you reading "
            # {}"'.format(cd['name'], cd['email'], post.title)
            # message = 'Read "{}" at {}\n\n{}\'s comments:
            # {}'.format(post.title, post_url, cd['name'], cd['comments'])
            # send_mail(subject, message, 'admin@myblog.com',[cd['to']])
            # sent = True
     
    context = {
        'share_form' : share_form,
        'post_shared': post_shared,
        'sent': sent,
    }
    return render(request,'blog/post_share.html',context)








# -----search inside tow fiels(p_subject , p_body) in Post model
def post_search(request):
    form = PostSearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = PostSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            # ------normal search -- Searching against multiple fields ---work ok---- #
            results = Post.objects.filter(p_status='p').annotate(search=SearchVector('p_subject','p_body'),).filter(search=query)

            # ---search with --- Stemming and ranking results ----work ok---#
            search_vector = SearchVector('p_subject', 'p_body')
            search_query = SearchQuery(query)
            results = Post.objects.annotate(search=search_vector,rank=SearchRank(search_vector, search_query)).filter(search=search_query).order_by('-rank')
            
            # ---- search with - Weighting queries -- work ok ----#
            search_vector = SearchVector('p_subject', weight='A') + SearchVector('p_body', weight='B')
            search_query = SearchQuery(query)
            results = Post.objects.annotate(rank=SearchRank(search_vector, search_query)).filter(rank__gte=0.3).order_by('-rank')
            
            # ----  Searching with trigram similarity ---- not work --#
            results = Post.objects.annotate(similarity=TrigramSimilarity('p_subject', query),).filter(similarity__gt=0.3).order_by('-similarity')

    context={
        'form': form,
        'query': query,
        'results': results,
    }
    return render(request,'blog/search.html',context)




# -----------------#  post Create  # -----------------------------------------------#
class PostCreateView(LoginRequiredMixin, FormView):
    model = Post
    # fields = ['title', 'content']
    template_name = 'blog/post_create.html'
    form_class = PostCreateForm
    success_url = reverse_lazy('blog:posts')

    def get(self, request, *args, **kwargs):
        form = self.form_class
        context = {
                "form": form
        }
        return render(request,'blog/post_create.html', context)
   
    def post(self, request, *args, **kwargs):
        if request.method == 'POST' :
            form = PostCreateForm(request.POST,request.FILES)
            if form.is_valid():
                  return self.form_valid(form)
            else:
                  return self.form_invalid(form)
   
    def form_valid(self, form):
        msg = """ New post add successfully."""
        request = self.request
        messages.success(request, msg)
        post           =  form.save(commit=False)
        post.p_author  =  self.request.user
        post.p_subject =  form.cleaned_data.get("p_subject")
        post.p_body    =  form.cleaned_data.get("p_body")  
        post.save() 
        p_tags         =  form.cleaned_data.get("p_tags")
        post.p_tags.set(p_tags)    # use set() with many to many
        post.save() 
        return HttpResponseRedirect(self.get_success_url())
   
    def form_invalid(self, form):
        print(form)
        msg = """Error done! please try again and enter correct data in the form fields."""
        request = self.request
        messages.warning(request, msg)
        # return self.get(request)
        return self.render_to_response(self.get_context_data(form=form))



# -----------------#    Post update   # -----------------------------------------------#
class PostUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/post_update.html'
    form_class = PostCreateForm
    success_url = 'blog:posts'

    def form_valid(self, form):
        form.instance.p_author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.p_author:
            return True
        else:
            return False



# -----------------#    Post delete   # -----------------------------------------------#
class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Post
    success_url = 'blog:posts'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.p_author:
            return True
        return False
