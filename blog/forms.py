from .models import Comment,Post
from django import forms
from ckeditor.widgets import CKEditorWidget


# -----------------# PostCreateForm  #create new post object  # -----------------------------------------------#
class PostCreateForm(forms.ModelForm):
    p_subject = forms.CharField(label='Post Subject')
    p_body    = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model  = Post
        fields = ['p_subject', 'p_body','p_tags']




# -----------------# Share POST by email Form # -----------------------------------------------#
class PostShareForm(forms.Form):
    sender_name    = forms.CharField(max_length=50)
    sender_email   = forms.EmailField()
    sender_comment = forms.CharField(widget=CKEditorWidget())
    share_to_email = forms.EmailField()




# -----------------# Search post Form   # -----------------------------------------------#
# search by fields ( p_subject, p_body ) of Post model 
class PostSearchForm(forms.Form):
    query = forms.CharField()




# -----------------# CommentCreateForm  #create a new comment object  # -----------------------------------------------#
class CommentCreateForm(forms.ModelForm):
    c_owner_name  = forms.CharField(label='your name')
    c_owner_email = forms.EmailField(label='your email')
    c_body        = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = Comment
        fields =['c_owner_name','c_owner_email','c_body']
    


