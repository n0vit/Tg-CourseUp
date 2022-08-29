import os
from pyrogram import Client, filters, types
from pyrogram.enums.chat_type import ChatType
from lib.data.data_model import CourseModel
from loader import repo


@Client.on_message(filters.command('entity', '!') )
async def reply_entity(client, message: types.Message):
    await message.reply(text=f"V! {message}")


@Client.on_message(filters.command('add', '!') )
async def add_channel_id(client, message: types.Message):
    if message.chat.type == ChatType.CHANNEL:
        chatId = message.chat.id
        course_name = message.command[1]
        root_dir = " ".join(message.command[2:])
        root_dir = os.path.normcase(root_dir)
        if os.path.isabs(root_dir):
            model = repo.create_course(CourseModel(courseName=course_name, chatId=chatId, rootLoclaDir=root_dir,isActive=True))
            await message.reply(text=f"Course data sucsessfuly added! \n **Course name**:  {model.courseName} 📃\n  Course rootLoclaDir:  `{model.rootLoclaDir}` 📁 \n Course status: `{model.isActive}` \n\
                                send `!start_course`")
        else:
            await message.reply(text=f"Command parameters error! \n expamle good commad: \n `!add course_name_without_spases C:\path_to_root_dir` \n your command: \n `{message.text}`")    
    else:
        await message.reply(text=f" Error: Chat type is ***not CHANNEL**")
        

@Client.on_message(filters.command('all', '!'))
async def all_courses(client: Client, message: types.Message):
    data_list = repo.get_data_all_courses()

    if len(data_list) ==0:
        text = "No courses in database"
    else:    
        text = "".join(data_list)

    await message.reply(text=text)

@Client.on_message(filters.command('delete', '!'))
async def delete_course(client: Client, message: types.Message):
    if len(message.command)==1:
        text = 'Icnorrect command ⛔: **missing Course_name** '
    name = message.command[1]
    model = repo.delete_course(name)
    text = 'Course deleted, try to check send `!all` command'
    await message.reply(text=text)


@Client.on_message(filters.command('change', '!'))
async def change_status(client: Client, message: types.Message):
    name = message.command[1]
    model = repo.change_course_status(name)
    if model is None:
        text = 'Error! ⛔ Incorrect name'
    else: 
        text =f"Status changed! \n current_data:  **Name** {model.courseName} | **status** `{model.isActive}`"
    await message.reply(text=text)

@Client.on_message(filters.command('start', '!'))
async def on_startup(client: Client, message: types.Message):
    await message.reply(text='avilible command: \r\n\
        /start - print this text\r\n\
        `!add` - create data for new course example `!add course_name_without_spases C:\path_to_root_dir` \r\n\
        `!start_course` - started loaded active course \r\n\
        `!all` print status data all courses \r\n\
        `!get data` print  data active course \r\n\
        `!change course_name` - changing course status \r\n\
        /stop - stoping script')
    


@Client.on_message(filters.command('get data', '!'))
async def get_data_from_course(client: Client, message: types.Message):
    data = repo.get_values()
    text = "\n".join(data)
    await message.reply(text=text)