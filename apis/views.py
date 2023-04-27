from django.shortcuts import render
from .models import *
from .serializer import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
# Create your views here.

class StaffView(APIView):
    
    def post(self, request):
        serializer = StaffSerializer(data= request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    def get(self, request, staffno):
        staff = Staff.objects.filter(staffno = staffno).first()
        serializer = StaffSerializer(staff)
        return Response(serializer.data)
    
class BranchCreateView(APIView):
    def post(self, request):
        serializer = BranchSerializer(data= request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OwnerCreateView(APIView):
    def post(self, request):
        serializer = OwnerManageSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientCreateView(APIView):
    def post(self, request):
        serializer = ClientRentalSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PropertyCreateView(APIView):
    def post(self, request):
        serializer = PropertySerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LeaseCreateView(APIView):
    def post(self, request):
        serializer = LeaseSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BranchDetailView(APIView):
    def get(self, request, br_id):
        list = []
        branch = Branches.objects.get(bnumber = br_id)
        queryset = Staff.objects.filter(brno = br_id)
        for staff in queryset:
            staff_data = {
                "staff_no": staff.staffno,
                "staff_name": staff.fname,
                "position": staff.sposition
            }
            list.append(staff_data)
        data = {
            "branch_no":br_id,
            "branch_address": branch.baddress,
            "mobile1": branch.mobileno1,
            "mobile2": branch.mobileno2,
            "mobile3": branch.mobileno3,
            "staff": list
        }
        return Response(data, status= status.HTTP_200_OK)
    
class PropertyListView(APIView):

    def get(self, request):
        search_query  = request.GET.get("q", '')
        tokens = [t.strip() for t in search_query.split(',')]
        q_objects = Q()
        for token in tokens:
            q_objects |= Q(pnumber__icontains = token)
            q_objects |= Q(ptype__icontains = token)
            q_objects |= Q(rent__icontains = token)
            q_objects |= Q(rooms__icontains = token)
            q_objects |= Q(paddress__icontains = token)
            q_objects |= Q(pin__icontains = token)
            q_objects |= Q(city__icontains = token)
        properties = Property.objects.filter(q_objects)
        data = [{
            'pnumber': p.pnumber, 'ptype': p.ptype, 'rooms': p.rooms, 'rent': p.rent, 'paddress': p.paddress, 'city': p.city }for p in properties
        ]
        return Response({'data': data})

#incomplete
class PropertyDetailView(APIView):
    def get(self, request, pnum):
        property = Property.objects.get(pnumber = pnum)
        clients = property.clientrental_set.all()
        clients_info = []
        if clients:
            for client in clients:
                info = {
                    "cnumber": client.cnumber,
                    "cname":client.cname,
                    "comment": client.comments
                }
                clients_info.append(info)
        data = {
            "pnumber" : property.pnumber,
            "ptype": property.ptype,
            "paddress": property.paddress,
            "rent": property.rent,
            "clients" : clients_info,
        }
        return Response(data)