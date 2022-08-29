from re import I
from .data_model import CourseModel
from typing import List


class CourseRepository():
    def __init__(self):
        self.db = CourseModel
    
    
    async def create_course(c: CourseModel) -> CourseModel | None:
        '''Create New Course data'''

        CourseData = CourseModel(
            id=c.id,
            courseName=c.courseName,
            rootLoclaDir=c.rootLoclaDir,
            queue=c.queue,
            current_module=c.current_module,
            current_fold=c.current_fold,
            current_file=c.current_file,
            current_teamplate_ids=c.current_teamplate_ids,
            tmp_links=c.tmp_links,
            tmp_file_names=c.tmp_file_names,
            isActive=c.isActive,
            chatId=c.chatId
        )
        insert = await CourseData.create()
        return insert

    async def change_course_status(self, name:str) -> CourseModel | None:
        data = self.db.find({'courseName': name}).to_list()
        model = data[0]
        model.isActive = not model.isActive
        await model.replace()
         




    async def get_all_courses(self) -> List[CourseModel]| None:  
        all = await self.db.all().to_list()
        return all 
    
    async def get_data_all_courses(self) -> List[str]:
        list_models = await self.get_all_courses()
        list_names= []
        if list_models is not None: 
            for model  in list_models:
                if model.isActive:
                    status = '🟢'
                else: 
                    status = '🔴'
                list_names.append(f" ❇️ Name: `{model.courseName}` | Status: **{model.isActive}** {status} \n")
        return list_names   
    
    
    
    async def get_course(self) -> CourseModel:
        '''Get full Course data'''

        course = await self.db.find({'isActive': True}).to_list()
        return course[0]


    
    async def get_values(self) -> List:
        model =  await self.get_course()

        result =[]

        result.append(f"**current module**: {model.current_module}") 
        
        result.append(f"**current fold**: {model.current_fold}") 
        
        result.append(f"**curent file**: {model.current_file}")
        


        result.append(f"**current teamplate ids**: ```{model.current_teamplate_ids}``` ")   

        result.append(f"**tmp links**: {model.tmp_links}")
           

        result.append(f"**tmp file names**: {model.tmp_file_names}")
            
        
        return result   

    async def delete_course(self, name:str) -> bool:
        doc = await self.db.find({'courseName': name}, limit=1).to_list()
        model =doc[0]
        return await model.delete()

    async def update_data(self, m: CourseModel) -> CourseModel | None:
        data =  await self.get_course()
        update_data =  m.dict(exclude_none=True)
    
        await data.inc(update_data)
        await data.replace()
        data =  await self.get_course()
        return data