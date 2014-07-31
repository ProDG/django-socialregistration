from django.core.urlresolvers import reverse
from socialregistration.contrib.github.client import Github
from socialregistration.contrib.github.models import GithubProfile, GithubAccessToken
from socialregistration.views import OAuthRedirect, OAuthCallback, SetupCallback

class GithubRedirect(OAuthRedirect):
    client = Github
    template_name = 'socialregistration/github/github.html'

class GithubCallback(OAuthCallback):
    client = Github
    template_name = 'socialregistration/github/github.html'
    
    def get_redirect(self):
        return reverse('socialregistration:github:setup')

class GithubSetup(SetupCallback):
    client = Github
    profile = GithubProfile
    template_name = 'socialregistration/github/github.html'
    
    def get_lookup_kwargs(self, request, client):
        login = client.get_user_info()['login']
        # workaround for the case, when user changes his username at GitHub
        try:
            old_github_profile = GithubAccessToken.objects.get(access_token=client._access_token).profile
            old_github_profile.github = login
            old_github_profile.save(force_update=True)
        except GithubAccessToken.DoesNotExist:
            pass
        # end of workaround
        return {'github': login}

