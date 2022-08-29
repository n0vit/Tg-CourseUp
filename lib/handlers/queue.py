import ntpath
from re import template
from pyrogram import Client, filters, types
from lib.data.data_model import CourseModel
from loader import repo
from .scan_files import DirScan
from .file_upload import FileUploader
from .list_files import HeadlinesGen, files_list

# queue_list [[gen_name, name_fold, [list_files_names], [list_path]]]

@Client.on_message(filters.command('start_course', '!'))
async def queue(client: Client, message:types.Message):
    
    model = await repo.get_course()

    root_dir = model.rootLoclaDir
    course_name = model.courseName
    chat_id = model.chatId
    
    if model.current_fold is None:
        # raw_data = DirScan.scan_dir(root_dir)
        
        # queue = DataQueue.create_queue(data_list=raw_data)
        
        test_queue = DirScan.scan_dir(root_dir)
        queue = test_queue
        await repo.update_data(CourseModel(queue=queue, isActive=True))

        
        await HeadlinesGen.parse_to_list_headlines(client=client, data_list=queue, chat_id=chat_id)
    

        
        for items in queue:
            parse = files_list()
            
            model = await repo.update_data(CourseModel(current_module=items[0],current_fold=items[1],
                                                 tmp_file_names=items[2],
                                                 isActive=True))
            
            msgs = await parse.createMessage(client=client,
                                            chat_id=chat_id, files_names_list=model.tmp_file_names)
            
            
            model = await repo.update_data(CourseModel(current_teamplate_ids=msgs,
                                                 isActive=True))
            
            await FileUploader.upload_files(client=client,
                                            chat_id=chat_id,
                                            data_list=items,
                                           teamplate_id=model.current_teamplate_ids[0])
            
            links_list = await parse.get_link_from_files(client=client,chat_id=chat_id,
                                                         file_names_list=model.tmp_file_names)
            
            model = await repo.update_data(CourseModel(tmp_links=links_list,
                                                 isActive=True))
            
            await parse.editMessage(client=client,chat_id=chat_id,
                                    msg_ids=model.current_teamplate_ids,
                                    data_list=items,
                                    files_list=model.tmp_file_names,
                                    link_list=model.tmp_links)
    
    else:
        queue = model.queue
        for element in queue:
            if element[1] == model.current_fold and element[0] == model.current_module:
                list_history_id = [] 
                message.text
                
                current_name = ntpath.basename(model.current_file)
                
                async for  history_message in client.get_chat_history(chat_id=chat_id, limit=50):
            
                        list_history_id.append(history_message.id)
                        try:
                            
                            if history_message.document is not None:      
                                if current_name ==history_message.document.file_name:
                                    list_history_id.pop()
                                    break
                            
                            elif history_message.caption is not None:
                                if current_name in history_message.caption:
                                    list_history_id.pop()
                                    break
                            
                                    
                            elif current_name in  history_message.text:
                                list_history_id.pop()
                                break
                            
                            elif model.current_fold in history_message.text:        
                                break
                            
                            elif   'Teamplate message' in history_message.text:
                                break
                          
                        except:
                            list_history_id.clear()
                            break
                        
                if list_history_id:
                    await client.delete_messages(chat_id=chat_id,message_ids=list_history_id)
                    
                    
                index_q = queue.index(element)
                for items in queue[index_q:]:
                    
                    for last_file in items[3]:
                        if model.current_file == last_file:
                            
                      
                            tmp_name_indexed =[]
                            tmp_path_indexed = []
                            
                            
                            for vid in items[3]:
                                
                                if '.mp4' in vid:
                                    tmp_path_indexed.append(vid)
                            
                            for docs in items[3]:
                                if '.mp4' in docs:
                                    continue
                                tmp_path_indexed.append(docs)
                            
                            for vid in items[2]:
                                
                                if '.mp4' in vid:
                                    tmp_name_indexed.append(vid)
                            
                            for docs in items[2]:
                                if '.mp4' in docs:
                                    continue
                                tmp_name_indexed.append(docs)
                            
                            
                            
                            index = tmp_path_indexed.index(last_file)
            
                            
                            if len(tmp_path_indexed[index:]) == 1:
                                items = None             
                                        
                        
                            else:
                                items = [items[0],items[1],tmp_name_indexed[index +1:],tmp_path_indexed[index +1:]]
                                
                                parse = files_list()
                                
                                await FileUploader.upload_files(client=client,
                                                    chat_id=chat_id,
                                                    data_list=items,
                                                    teamplate_id=model.current_teamplate_ids[0])
                                
                                links_list = await parse.get_link_from_files(client=client,chat_id=chat_id,
                                                                 file_names_list=model.tmp_file_names)
                    
                                model = await repo.update_data(CourseModel(tmp_links=links_list,
                                                         isActive=True))
                    
                                await parse.editMessage(client=client,chat_id=chat_id,
                                            msg_ids=model.current_teamplate_ids,
                                            data_list=items,
                                            files_list=model.tmp_file_names,
                                            link_list=model.tmp_links)
                                
                                items = None
                            break
                        
           
                    
                    if items is None:
                        continue
                    
                   
                   
                    parse = files_list()
       
                        
                            
                        # model = repo.update_data(CourseModel(current_fold=items[1],
                        #                              tmp_file_names=items[2],
                        #                              isActive=True))
                        
                        
                    msgs = await parse.createMessage(client=client,
                                                chat_id=chat_id,
                                                files_names_list=items[2])
                                             
                    
                    model = await repo.update_data(CourseModel(current_module=items[0],
                                                         current_fold=items[1],
                                                         tmp_file_names=items[2],
                                                         current_teamplate_ids=msgs,
                                                         isActive=True))
                
                
                    
                    await FileUploader.upload_files(client=client,
                                                    chat_id=chat_id,
                                                    data_list=items,
                                                    teamplate_id=model.current_teamplate_ids[0])
                    
                    
                    links_list = await parse.get_link_from_files(client=client,chat_id=chat_id,
                                                                 file_names_list=model.tmp_file_names)
                    
                    model = await repo.update_data(CourseModel(tmp_links=links_list,
                                                         isActive=True))
                    
                    await parse.editMessage(client=client,chat_id=chat_id,
                                            msg_ids=model.current_teamplate_ids,
                                            data_list=items,
                                            files_list=model.tmp_file_names,
                                            link_list=model.tmp_links)
                    
                    
    
    await client.send_message(chat_id=chat_id,text='__**Load finished**__')
    
    model = await repo.change_course_status(course_name)
    
    await client.send_message(chat_id=chat_id,text=f"**Course name**:  {model.courseName} 📃\n  Course rootLoclaDir:  `{model.rootLoclaDir}` 📁 \n Course status: `{model.isActive}` \n")