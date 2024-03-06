from aiogram.fsm.state import StatesGroup, State



class ServiceState(StatesGroup):
    
    catName = State()
    serName = State()
    phoneNumber = State()
 
