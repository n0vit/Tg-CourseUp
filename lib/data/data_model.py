from beanie import Document



class CourseModel(Document):
    id : str = None
    courseName: str | None
    rootLoclaDir: str | None
    queue: list =  None
    current_module: str = None
    current_fold: str = None
    current_file: str = None
    current_teamplate_ids: list = None
    tmp_links: list[str] = None
    tmp_file_names: list[str] = None
    chatId: int = None
    isActive: bool = None
    class Settings:
        name = "Courses"
    # class Config:
    #     underscore_attrs_are_private = False
    #     fields = {'key': '_key','id':'_id', 'rev':'_rev'}



