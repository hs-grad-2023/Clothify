from django.shortcuts import redirect

class RestrictedSocialLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 로그인되어 있을 경우에만 차단
        if request.user.is_authenticated:
            if 'oauth2' in request.get_full_path():
                return redirect('/')
        response = self.get_response(request)
        return response