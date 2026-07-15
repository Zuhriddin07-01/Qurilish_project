from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer

class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'client':
            return Order.objects.filter(client=user)
        elif user.role == 'builder':
            return Order.objects.filter(builder=user.builder_profile)
        return Order.objects.none()

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


class OrderDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user)

    def patch(self, request, *args, **kwargs):
        order = self.get_object()
        new_status = request.data.get('status')
        allowed = ['accepted', 'rejected', 'in_work', 'done']

        if new_status not in allowed:
            return Response({'error': 'Noto\'g\'ri status'}, status=400)

        order.status = new_status
        order.save()
        return Response(OrderSerializer(order).data)
        