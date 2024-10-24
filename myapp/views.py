from django.shortcuts import redirect, render
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Max, F, OuterRef, Subquery
from django.db.models.functions import Coalesce, Greatest
from django.urls import reverse_lazy

from .models import CustomUser, Message
from .forms import CustomUserModelForm, LoginForm, MessageModelForm, UsernameUpdateForm, EmailUpdateForm, ImageUpdateForm, PasswordUpdateForm


def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == "POST":
        form = CustomUserModelForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("myapp:index")
    
    else:
        form = CustomUserModelForm()

    context = {
        "form": form,
    }
    
    return render(request, "myapp/signup.html", context)

def login_view(request):
    if request.method == "POST":
        next = request.POST.get("next")
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            
            if user:
                login(request, user)
                if next == "None":
                    return redirect("myapp:friends")
                else:
                    return redirect(to=next)
    else:
        form = LoginForm()
        next = request.GET.get("next")
        
    context = {
        "form": form,
        "next": next,
    }
    return render(request, 'myapp/login.html', context)

@login_required
def friends(request):
    user = request.user

    latest_msg = Message.objects.filter(
        Q(from_user=OuterRef('pk'), to_user=user)
        | Q(from_user=user, to_user=OuterRef('pk'))
    ).order_by('-created_at')

    friends = (
        CustomUser.objects.exclude(id=user.id)
        .annotate(
            send_max=Max('from_user__created_at', filter=Q(from_user__to_user=user)),
            receive_max=Max('to_user__created_at', filter=Q(to_user__from_user=user)),
            latest_time=Greatest("send_max", "receive_max"),
            latest_msg_time=Coalesce("latest_time", "send_max", "receive_max"),
            latest_msg_talk=Subquery(latest_msg.values('content')[:1])
        ).order_by(F('latest_msg_time').desc(nulls_last=True))
    )

    query = request.GET.get('query')

    if query:
        friends = friends.filter(Q(username__icontains=query) | Q(email__icontains=query))
        

    # if Message.objects.filter(Q(from_user=user) | Q(to_user=user)).exists():
    #     message_list = Message.objects.filter(Q(from_user=user) | Q(to_user=user)).order_by("-created_at")
    #     for message in message_list:

    #         if friend_list.filter(Q(username=message.from_user) | Q(username=message.to_user)).exists() == False:
    #             continue


    #         saved_user = 0

    #         if message.from_user == user:
    #             saved_user = message.to_user
                
    #         else:
    #             saved_user = message.from_user

    #         if message_list.filter(id=message.id).exists():
    #             friend_list = friend_list.exclude(id=saved_user.id)

    #             message_ordered.append(message)
    #             message_list = message_list.exclude(Q(from_user=saved_user) | Q(to_user=saved_user))
                
    #         if message_list.count() == 0:
    #             break

    # context = {
    #     "friend_list": friend_list,
    #     "message_ordered": message_ordered,
    # }
    

    context = {
        'friends': friends,
    }

    return render(request, "myapp/friends.html", context)

def talk_room(request, friend_id):
    user = request.user
    friend = CustomUser.objects.get(id=friend_id)

    if request.method == "POST":
        form = MessageModelForm(request.POST)

        if form.is_valid():
            message = form.save(commit=None)
            message.from_user = user
            message.to_user = friend
            message.save()
            return redirect("myapp:talk_room", friend_id = friend_id)
    else:
        form = MessageModelForm()
    context = {
        "form": form,
        "friend": friend,
        "messages": Message.objects.filter(Q(from_user=user, to_user=friend) | Q(from_user=friend, to_user=user)).order_by("created_at"),
    }
    return render(request, "myapp/talk_room.html", context)

def setting(request):
    return render(request, "myapp/setting.html")

def update(request, update_id):
    user = request.user
    if request.method == "POST":
        if update_id ==1:
            form = UsernameUpdateForm(request.POST)
            user.username = request.POST['username']
        elif update_id == 2:
            form = EmailUpdateForm(request.POST)
            user.email = request.POST['email']
        elif update_id == 3:
            form = ImageUpdateForm(request.FILES)
            user.image = request.FILES['image']
            user.save()
            return redirect("myapp:updated", updated_id = update_id)

        if form.is_valid():
            user.save()
            return redirect("myapp:updated", updated_id = update_id)
    
    else:
        if update_id ==1:
            form = UsernameUpdateForm()
        elif update_id == 2:
            form = EmailUpdateForm()
        elif update_id == 3:
            form = ImageUpdateForm()

    if update_id ==1:
        page_title = 'ユーザーネーム変更'
    elif update_id == 2:
        page_title = 'メールアドレス変更'
    elif update_id == 3:
        page_title = 'アイコン変更'

    context = {
        "form": form,
        "id": update_id,
        "title": page_title,
    }
    return render(request, "myapp/update.html", context)

class PasswordChange(PasswordChangeView):
    form_class = PasswordUpdateForm
    success_url = reverse_lazy("myapp:password_updated")
    template_name = 'myapp/password_update.html'
    
def password_updated(request):
    return render(request, "myapp/password_updated.html")

def updated(request, updated_id):
    if updated_id ==1:
        title = "ユーザーネーム変更"
        updated_text = "ユーザーネーム変更完了"
    elif updated_id == 2:
        title = "メールアドレス変更"
        updated_text = "メールアドレス変更完了"
    elif updated_id == 3:
        title = "アイコン変更"
        updated_text = "アイコン変更完了"

    context = {
        "title": title,
        "text": updated_text,
    }
    return render(request, "myapp/updated.html", context)

def logout_view(request):
    logout(request)
    return render(request, "myapp/index.html")