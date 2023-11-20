from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from keyboards.for_facts import get_choose, get_types_facts, in_category_facts
from bot_utils import get_facts

class FSMStates(StatesGroup):
    start = State()
    choose_type_fact = State()
    waiting_type_fact = State()
    history_fact = State()
    science_fact = State()
    day_fact = State()

router = Router() 

@router.message(Command("start"), default_state)
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(
        "We are happy to see you in this bot. Here you can get a lot of amazing and intersting facts.",
        reply_markup=get_choose()
    )

    await state.set_state(FSMStates.choose_type_fact)


@router.message(F.text.lower() == 'choose category', FSMStates.choose_type_fact)
async def categories(message: Message, state: FSMContext):
    await message.answer(
        text='Today we have 3 categories: History Fact, Fact of the Day, Science',
        reply_markup=get_types_facts()
    )

    await state.set_state(FSMStates.waiting_type_fact)

@router.message(F.text == 'Get Science Fact', FSMStates.waiting_type_fact)
@router.message(F.text == 'Get History Fact', FSMStates.waiting_type_fact)
@router.message(F.text == 'Fact of the Day', FSMStates.waiting_type_fact)
async def categories(message: Message, state: FSMContext):
    await message.answer(
        text='You can push send for get fact or come back',
        reply_markup=in_category_facts()
    )

    if message.text == 'Get Science Fact':
        await state.set_state(FSMStates.science_fact)
    elif message.text == 'Get History Fact':
        await state.set_state(FSMStates.history_fact)
    elif message.text == 'Fact of the Day':
        await state.set_state(FSMStates.day_fact)

@router.message(F.text == 'Send me fact', FSMStates.day_fact)
@router.message(F.text == 'Send me fact', FSMStates.science_fact)
@router.message(F.text == 'Send me fact', FSMStates.history_fact)
async def send_fact(message: Message, state: FSMContext):
    current_state = await state.get_state()
  
    if current_state == FSMStates.science_fact.state:
        response = get_facts(0)
        await message.answer(
            text=response
        )
    elif current_state == FSMStates.history_fact.state:
        response = get_facts(1)
        await message.answer(
            text=response
        )
    elif current_state == FSMStates.day_fact.state:
        response = get_facts(2)
        await message.answer(
            text=response
        )

@router.message(F.text == 'Back', FSMStates.science_fact)
@router.message(F.text == 'Back', FSMStates.day_fact)
@router.message(F.text == 'Back', FSMStates.history_fact)    
async def back(message: Message, state: FSMContext):
    await message.answer(
        text='Choose category',
        reply_markup=get_types_facts()
    )
    await state.set_state(FSMStates.waiting_type_fact)

@router.message(StateFilter(None), Command(commands=["cancel"]))
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    await state.set_data({})
    await message.answer(
        text="Your state canceled",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(Command(commands=["cancel"]))
@router.message(F.text == "Exit")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Will be happy to see you again! \n Write /start to run bot",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message()
async def incorrect_query(message: Message):
    await message.answer(
        text="I don't understand your query, please try again"
    )
