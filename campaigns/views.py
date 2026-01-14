from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .models import Campaign, Application, Comment, CampaignView, Response
from .forms import CampaignForm, ApplicationForm, ResponseForm
from profiles.models import InfluencerProfile  # Importar el modelo de perfil de influencer

@login_required
def campaign_list(request):
    query = request.GET.get('q')
    if request.user.user_type == 'empresa':
        campaigns = Campaign.objects.filter(company=request.user)
        applied_campaign_ids = []
    else:
        # Obtener las categorías del influencer usando el campo correcto
        influencer_profile = InfluencerProfile.objects.get(profile__user=request.user)
        influencer_categories = influencer_profile.categories.all()
        # Filtrar campañas que tengan al menos una categoría en común con el influencer
        campaigns = Campaign.objects.filter(categories__in=influencer_categories).distinct()
        # Obtener campañas a las que el influencer ya se postuló
        applied_campaign_ids = list(Application.objects.filter(influencer=request.user).values_list('campaign_id', flat=True))
        if query:
            campaigns = campaigns.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )

    for campaign in campaigns:
        # Verificar si el usuario ya ha visto esta campaña
        if not CampaignView.objects.filter(campaign=campaign, user=request.user).exists():
            CampaignView.objects.create(campaign=campaign, user=request.user)
            campaign.views += 1
            campaign.save()

        # Calcular el engagement rate para cada campaña
        if campaign.views > 0:
            campaign.engagement_rate = round(((campaign.likes + campaign.comment_set.count()) / campaign.views) * 100, 2)
        else:
            campaign.engagement_rate = 0

        # Filtrar influencers por categorías de la campaña
        campaign.influencers = InfluencerProfile.objects.filter(categories__in=campaign.categories.all()).distinct()

    return render(request, 'campaigns/campaign_list.html', {
        'campaigns': campaigns,
        'applied_campaign_ids': applied_campaign_ids,
    })

@login_required
def campaign_create(request):
    if request.user.user_type != 'empresa':
        return redirect('campaigns:campaign_list')  # Solo empresas pueden crear campañas

    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.company = request.user
            campaign.save()
            form.save_m2m()  # Guardar las relaciones ManyToMany (como las categorías)
            return redirect('campaigns:campaign_list')
        else:
            print(form.errors)  # Para depuración: imprime errores en consola
    else:
        form = CampaignForm()
    return render(request, 'campaigns/campaign_create.html', {'form': form})

@login_required
def campaign_edit(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id, company=request.user)

    if request.method == 'POST':
        form = CampaignForm(request.POST, instance=campaign)
        if form.is_valid():
            form.save()
            return redirect('campaigns:campaign_list')
    else:
        form = CampaignForm(instance=campaign)

    return render(request, 'campaigns/campaign_edit.html', {'form': form, 'campaign': campaign})

@login_required
def apply_to_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    if request.user.user_type != 'influencer':
        return redirect('campaigns:campaign_list')

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.campaign = campaign
            application.influencer = request.user
            application.save()
            return redirect('campaigns:campaign_list')
    else:
        form = ApplicationForm()
    return render(request, 'campaigns/apply_to_campaign.html', {'form': form, 'campaign': campaign})

@login_required
def campaign_applications(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id, company=request.user)
    applications = campaign.applications.all()  # Relación inversa desde Application
    return render(request, 'campaigns/campaign_applications.html', {
        'campaign': campaign,
        'applications': applications,
    })

@login_required
def like_campaign(request, campaign_id):
    if request.user.user_type != 'influencer':
        return JsonResponse({'error': 'Solo los influencers pueden dar like.'}, status=403)

    campaign = get_object_or_404(Campaign, id=campaign_id)

    if request.user in campaign.liked_by.all():
        campaign.liked_by.remove(request.user)
        campaign.likes -= 1
        liked = False
    else:
        campaign.liked_by.add(request.user)
        campaign.likes += 1
        liked = True

    campaign.save()
    return JsonResponse({'liked': liked, 'likes_count': campaign.likes})

@login_required
def respond_to_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)

    # Verificar que el usuario sea parte de la conversación
    if request.user != application.campaign.company and request.user != application.influencer:
        return redirect('campaigns:campaign_list')

    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.application = application
            response.user = request.user
            response.save()
            return redirect('campaigns:respond_to_application', application_id=application.id)
    else:
        form = ResponseForm()

    return render(request, 'campaigns/respond_to_application.html', {
        'form': form,
        'application': application,
        'responses': application.responses.all()
    })

@login_required
def influencer_applications(request):
    # Filtrar las postulaciones del influencer actual
    applications = Application.objects.filter(influencer=request.user)

    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.user = request.user
            response.application = get_object_or_404(Application, id=request.POST.get('application_id'))
            response.save()
            return redirect('campaigns:influencer_applications')
    else:
        form = ResponseForm()

    return render(request, 'campaigns/influencer_applications.html', {
        'applications': applications,
        'form': form
    })

@login_required
def add_comment(request, campaign_id):
    if request.method == 'POST':
        campaign = get_object_or_404(Campaign, id=campaign_id)
        content = request.POST.get('content')

        if not content:
            # Puedes mostrar un mensaje de error si quieres, aquí solo recarga la página
            return redirect('campaigns:campaign_list')

        Comment.objects.create(user=request.user, campaign=campaign, content=content)
        return redirect('campaigns:campaign_list')