from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Conversation, ConversationMessage
from .forms import ConversationMessageForm
from users.models import CustomUser

@login_required
def inbox(request):
    # Obtén las conversaciones en las que participa el usuario autenticado
    conversations = Conversation.objects.filter(participants=request.user)
    
    # Agrega el otro participante a cada conversación
    for conversation in conversations:
        conversation.other_participant = conversation.get_other_participant(request.user)
    
    return render(request, 'messages_app/inbox.html', {'conversations': conversations})

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    
    # Marcar mensajes como leídos
    unread_messages = conversation.messages.filter(is_read=False).exclude(sender=request.user)
    unread_messages.update(is_read=True)
    
    # Obtener todos los mensajes de la conversación
    messages_list = conversation.messages.all()
    
    # Formulario para enviar un nuevo mensaje
    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.conversation = conversation
            new_message.sender = request.user
            new_message.save()
            
            # Actualizar la fecha de la conversación
            conversation.save()  # Esto actualiza el campo updated_at
            
            return redirect('messages_app:conversation_detail', conversation_id=conversation.id)
    else:
        form = ConversationMessageForm()
    
    # Obtener todas las conversaciones para el sidebar
    conversations = Conversation.objects.filter(participants=request.user)
    
    context = {
        'conversation': conversation,
        'messages_list': messages_list,
        'form': form,
        'conversations': conversations,
        'selected_conversation': conversation,
    }
    return render(request, 'messages_app/conversation_detail.html', context)

@login_required
def new_message(request):
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient')
        content = request.POST.get('content')
        
        if not recipient_id or not content:
            messages.error(request, "Por favor, selecciona un destinatario y escribe un mensaje.")
            return redirect('messages_app:new_message')
        
        try:
            recipient = CustomUser.objects.get(id=recipient_id)
            
            # Verificar si ya existe una conversación entre estos usuarios
            conversation = Conversation.objects.filter(participants=request.user).filter(participants=recipient).first()
            
            if not conversation:
                # Crear nueva conversación
                conversation = Conversation.objects.create()
                conversation.participants.add(request.user, recipient)
            
            # Crear nuevo mensaje
            new_message = ConversationMessage.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
            
            messages.success(request, "Mensaje enviado correctamente.")
            return redirect('messages_app:conversation_detail', conversation_id=conversation.id)
            
        except CustomUser.DoesNotExist:
            messages.error(request, "El destinatario seleccionado no existe.")
            return redirect('messages_app:new_message')
    
    # Obtener posibles destinatarios según el tipo de usuario
    if request.user.user_type == 'empresa':
        recipients = CustomUser.objects.filter(user_type='influencer')
    else:  # influencer
        recipients = CustomUser.objects.filter(user_type='empresa')
    
    context = {
        'recipients': recipients,
    }
    return render(request, 'messages_app/new_message.html', context)

