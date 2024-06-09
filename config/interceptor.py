from django.shortcuts import redirect
import logging
logger = logging.getLogger(__name__)


def my_interceptor(get_response):

    def middleware(request):
        logger.debug('interceptor!!!')
        logger.debug('request.path = ' + str(request.path))
        if (
                request.path != '/sign/signin/'
                and request.path != '/sign/signup/'
                and request.path != '/sign/signout/'
                and request.path != '/main/'
        ):
            sign_session = request.session.get('sign_session')
            if sign_session is None or sign_session == '':
                return redirect('sign/signin')

        response = get_response(request)
        return response

    return middleware
