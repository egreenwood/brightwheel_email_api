from rest_framework import viewsets, status
from rest_framework.response import Response
from api.models import EmailRequest
from api.serializers import EmailRequestSerializer
from api.email_request_service import EmailRequestService


class EmailViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        # serialize/validate data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # call email_service
        try:
            service = EmailRequestService(serializer.validated_data)
            response = service.send_email()
            if 200 <= response.status_code < 300:
                # 201 if we get a success response from the email servers
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                # 202 if we don't get a success response from the email servers
                return Response({'email_server_errors': response.data}, status=status.HTTP_202_ACCEPTED, headers=headers)

        except KeyError as e:
            Response(status=status.HTTP_400_BAD_REQUEST, data={"error": e.message})

    queryset = EmailRequest.objects.all()
    serializer_class = EmailRequestSerializer
