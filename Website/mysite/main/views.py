from django.shortcuts import render, redirect
from .forms import PlayerForm, TeamForm
from .models import Player, Team
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.forms import ModelChoiceField, Form
from django import forms
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages 


def home(request):
   return render(request, "home.html", {})

def index(request, id):
    ls = Player.objects.get(puid=id)
    return render(request, "list.html", {"ls":ls})

def players_list(request):
    players = Player.objects.all()
    return render(request, 'player_teams/players_list.html', {'players': players})

def player_add(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Player added successfully!')
            return redirect('players_list')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = PlayerForm()
    return render(request, 'player_teams/player_add.html', {'form': form})


def player_edit(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    if request.method == 'POST':
        form = PlayerForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            messages.success(request, 'Player updated successfully!')
            players = Player.objects.all()
            return render(request, 'player_teams/players_list.html', {'players': players})
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = PlayerForm(instance=player)
    return render(request, 'player_teams/player_edit.html', {'form': form})


def player_delete(request, player_id):
    try:
        obj = Player.objects.get(pk=player_id)
        obj.delete()
        return redirect('players_list')  
    except Player.DoesNotExist:
        pass


def teams_list(request):
    teams = Team.objects.all()
    return render(request, 'player_teams/teams_list.html', {'teams': teams})

def team_add(request):
  players = Player.objects.all()
  if request.method == 'POST':
    form = TeamForm(request.POST)
    selected_players = request.POST.getlist('players')
    if form.is_valid():
        team = form.save()
        for player_id in selected_players:
            player = Player.objects.get(pk=player_id)
            team.playerteam_set.create(player=player, team=team)
        messages.success(request, 'Team added successfully!')
        return redirect('teams_list')
    else:
        messages.error(request, 'Please correct the errors in the form.')
  else:
      form = TeamForm()
  return render(request, 'player_teams/team_add.html', {'form': form, 'players': players})

def team_edit(request, team_id):
    team = Team.objects.get(pk=team_id)
    assigned_players = team.playerteam_set.all()
    print(assigned_players)
    available_players = Player.objects.exclude(playerteam__team=team)
    if request.method == 'POST':
      form = TeamForm(request.POST, instance=team)
      selected_players = request.POST.getlist('players') 
      if form.is_valid():
          form.save()
          existing_assignments = team.playerteam_set.all()
          for assignment in existing_assignments:
            assignment.delete()

          for player_id in selected_players:
              player = Player.objects.get(pk=player_id)
              team.playerteam_set.create(player=player, team=team)
          messages.success(request, 'Team saved successfully!')
          return redirect('teams_list') 
      else:
          messages.error(request, 'Please correct the errors in the form.')
    else:
      form = TeamForm(instance=team)
    return render(request, 'player_teams/team_edit.html', {'form': form, 'team': team, 'assigned_players': assigned_players, 'available_players': available_players})

def team_delete(request, team_id):
    try:
        obj = Team.objects.get(pk=team_id)
        obj.delete()
        return redirect('teams_list')  
    except Team.DoesNotExist:
        pass
    
def stats(request):
    players = Player.objects.all()
    selected_player = None
    player_winrate = None
    player_team_count = None
    highest_winrate_team = None
    lowest_winrate_team = None
    highest_winrate = None
    lowest_winrate = None

    if request.method == 'GET':
        selected_player_id = request.GET.get('player')
        if selected_player_id:
            selected_player = Player.objects.get(pk=selected_player_id)
            player_winrate = calculate_player_winrate(selected_player)
            player_team_count = selected_player.playerteam_set.count()
            highest_winrate_team, highest_winrate, lowest_winrate_team, lowest_winrate = calculate_team_winrates(selected_player)

    context = {'players': players, 'selected_player': selected_player,
                'player_winrate': player_winrate, 'player_team_count': player_team_count,
                'highest_winrate_team': highest_winrate_team, 'lowest_winrate_team': lowest_winrate_team,
                'highest_winrate': highest_winrate, 'lowest_winrate': lowest_winrate}

    return render(request, 'stats.html', context)

def calculate_player_winrate(player):
  playerteams = player.playerteam_set.all()
  wins = 0
  losses = 0
  for pt in playerteams:
      team = pt.team
      wins = wins + team.wins
      losses = losses + team.losses
  if wins + losses == 0:
      return 0
  return round(wins/(wins + losses), 2)

def calculate_team_winrates(player):
    playerteams = player.playerteam_set.all()
    high = -1
    low = 1
    hr = None
    lr = None
    for pt in playerteams:
        team = pt.team
        if team.wins + team.losses == 0:
          winrate = 0
        else:
          winrate = round(team.wins / (team.wins + team.losses),2)
          if winrate > high:
              high = winrate
              hr = team
          if winrate < low:
              low = winrate
              lr = team
    if high == -1:
        return None, 0, None, 0
    return hr, high, lr, low


"""

def register(request):
    form = PlayerForm()
    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            puid = form.cleaned_data["puid"]
            n = form.cleaned_data["name"]
            nn = form.cleaned_data["nickname"]
            e = form.cleaned_data["purdue_email"]
            p = form.cleaned_data["position"]
            player = Player(puid = puid, name = n, nickname = nn, purdue_email = e, position = p)
            player.save()

            return redirect('table_view')
        else:
            form = PlayerForm()

    context = {"form":form} 
    return render(request, "register.html", context) 

def table_view(request):
  data = Player.objects.all()
  context = {'data': data}
  if request.method == 'DELETE':
    pk = request.POST.get('pk')
    print(pk)
    obj = Player.objects.get(pk=pk)
    obj.delete()
    return redirect('table_view')
  return render(request, 'players.html', context)




class EditPlayerForm(forms.ModelForm):
    class Meta:
        model = Player 
        fields = ['name', 'nickname', 'purdue_email', 'position'] 

    name = forms.CharField(max_length=50, label='Name')
    nickname = forms.CharField(max_length=50, label='Nickname')
    purdue_email = forms.EmailField(label='Purdue Email')
    position = models.CharField(choices=Player.POSITIONS)  # Use Player.POSITIONS directly

    


def edit_view(request, pk):
  obj = Player.objects.get(pk=pk)
  if request.method == 'POST':
    form = EditPlayerForm(request.POST, instance=obj)  # Pass instance for update
    if form.is_valid():
      form.save()
      # Consider redirecting back to the table view after edit
      return redirect('table_view')
  else:
    # Pre-populate form with existing data
    initial_data = {'name': obj.name, 'nickname': obj.nickname, 'purdue_email': obj.purdue_email, 'position': obj.position}
    form = EditPlayerForm(initial=initial_data)
  context = {'object': obj, 'form': form}
  return render(request, 'edit_form.html', context)

def delete_entry(request, pk):
    try:
        obj = Player.objects.get(pk=pk)
        obj.delete()
        return redirect('table_view')  # Redirect to table view after deletion
    except Player.DoesNotExist:  # Handle object not found case
        # Handle error (e.g., display message)
        pass
"""

"""
def edit_view(request, pk):
  obj = Player.objects.get(pk=pk)
  if request.method == 'POST':
    # Update form data (excluding pk) and save
    obj.puid = request.POST.get('puid')
    obj.name = request.POST.get('name')
    obj.nickname = request.POST.get('nickname')
    obj.purdue_email = request.POST.get('purdue_email')
    obj.position = request.POST.get('position')
    obj.save()
    return redirect('table_view')
  context = {'object': obj}
  return render(request, 'edit_form.html', context)
"""
