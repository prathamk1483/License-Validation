from django.urls import path
from ..views import machineHome
from ..Views.machineViews import *

urlpatterns = [
    path('',machineHome,name='machineHome'),
    path('create/',createMachine,name='createMachine'),
    path('update/',updateMachine,name='updateMachine'),
    path('delete/',deleteMachine,name='deleteMachine'),
    path('read/',getAllMachines,name='getAllMachines'),
    path('readbyid/',getMachineByAdd,name='getMachineByAdd'),
]

