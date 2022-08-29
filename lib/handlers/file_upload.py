
import ntpath
import re
import os
from lib.data.data_model import CourseModel
from loader import repo
from pyrogram import Client, types
from .ffmpeg_metadata import VideoMeatadata
# queue_list [[gen_name, name_fold, [list_files_names], [list_path]]]



class FileUploader:
        async def upload_files(client: Client,chat_id: int,  data_list: list, teamplate_id: int):
                async def progress(current, total, file_path, msg:int):
                        with open("tmp_text.txt", encoding='utf8' ) as file:
                                old_text = file.read()                
                                file.close()
                        length = 10 
                        fill = '❇️'
                        decimals = 1
                        prefix ='Progress'
                        suffix = 'Complete'
                        percent = ("{0:." + str(decimals) + "f}").format(100 * (current / float(total)))
                        int_precent = float(percent)
                        if old_text == 'progress':
                                filledLength = int(length * current // total)
                                bar = fill * filledLength + '-' * (length - filledLength)

                                text =f' {prefix} |{bar}| {percent}% {suffix} \n `{file_path}`'
                                
                                with open("tmp_text.txt", "w", encoding='utf8') as file:
                                        file.flush()
                                        file.write(text)
                                        file.close()
                                        
                                await client.edit_message_text(chat_id=chat_id,message_id=msg,text=text)
                        else:           
                                search = re.search(r'\d+\.+\d+\%', old_text)
                                # [:-1] remove % literal
                                old_precent = float(search.group(0)[:-1])
                                if int_precent - old_precent >= 5.0:
                                        filledLength = int(length * current // total)
                                        bar = fill * filledLength + '-' * (length - filledLength)
                                        
                                        text =f' {prefix} |{bar}| {percent}% {suffix} \n  `{file_path}`'
                                        
                                        with open("tmp_text.txt", "w", encoding='utf8') as file:
                                                file.flush()
                                                file.write(text)
                                                file.close()
                                        await client.edit_message_text(chat_id=chat_id,message_id=msg,text=text)
                                        print(text)
                                        
                teamplate_msg = await client.get_messages(chat_id=chat_id,message_ids=teamplate_id)                        
                teamplate_link = teamplate_msg.link
                list_path = data_list[-1]
                list_file_name = data_list[-2]
                captions = []
                documents= []
                dir_name = os.path.dirname(list_path[0])
                for cap in list_path:
                        if 'cap.txt' in cap:
                                captions.append(cap)  
                for path in list_path:
                        index_for_name = list_path.index(path)
                        file_name = list_file_name[index_for_name]
                        
                        with open("tmp_text.txt", "w") as file:
                                        file.flush()
                                        file.write('progress')
                        
                        path = str(path) 
                        if 'cap.txt' in path:
                                continue
                        
                     
                        
                        if '.mp4' in path:          
                                metadata = VideoMeatadata.get_video_metadata(path)
                                file_name = ntpath.basename(path)
                        
                                caption=f" <i>имя файла</i>: `{file_name}` \n"
                                if captions:
                                        for caption_to_read in captions:
                                                cap_file_name = ntpath.basename(caption_to_read)
                                                
                                
                                                if file_name[0:5] == cap_file_name[0:5]:
                                                
                                                        cap = open(caption_to_read,'r', encoding='utf8')
                                                        cap_list =cap.readlines()
                                                        cap_list.insert(0,f" <i>имя файла</i>: `{file_name}` \n")
                                                        cap_list.insert(1,'\n')
                                                        caption = "".join(cap_list)
                                                        
                                                        break

                                        
                                msg = await client.send_message(chat_id=chat_id, text='progress')
                                args = (path, msg.id)
                                
                                caption = caption + f" \n [🔝 к оглавлению🔝]({teamplate_link})"
                                
                                await client.send_video(chat_id=chat_id,
                                                        video=path,
                                                        caption=caption,
                                                        width=metadata[0],
                                                        height=metadata[1],
                                                        duration=metadata[2],
                                                        progress=progress,
                                                        progress_args=args)
                                
                                repo.update_data(m=CourseModel(current_file=path,  isActive=True))
                                
                                await client.delete_messages(chat_id=chat_id,message_ids=msg.id)
                                
                        # elif '.ts' in path:
                        #         caption=f" <i>имя файла</i>: `{file_name}` \n"
                        #         if captions:
                        #                 for caption in captions:
                        #                         if path[0:4] == caption[0:4]:
                                                
                        #                                 cap = open(caption,'r', encoding='utf8')
                        #                                 cap_list =cap.readlines()
                        #                                 cap_list.insert(0,f" <i>имя файла</i>: `{file_name}` \n")
                        #                                 cap_list.insert(1,'\n')
                        #                                 caption = "".join(cap_list)       
                        #         msg = await client.send_message(chat_id=chat_id, text='progress')
                        #         args = (path, msg.id)
                        #         client.send_document(chat_id=chat_id,
                        #                              document=path,
                        #                              caption=caption
                        #                              , progress=progress,progress_args=args)
                        #         await client.delete_messages(chat_id=chat_id,message_ids=msg.id)
                        elif '.mp3' in path: 
                                
                                caption = f" \n \n [🔝 к оглавлению🔝]({teamplate_link})"
                                
                                sended_mesage = await client.send_audio(chat_id=chat_id,
                                                     audio=path,
                                                     caption=caption)
                                
                                repo.update_data(m=CourseModel(current_file=path,  isActive=True))
                                
                        else:  
                                documents.append(types.InputMediaDocument(path)) 
                
                if documents:
                        if len(documents)==1:
                                
                                caption = f" \n \n [🔝 к оглавлению🔝]({teamplate_link})"
                                 
                                sended_mesage = await client.send_document(chat_id=chat_id,
                                                     document=documents[0].media,
                                                     caption=caption)
                                
                                file_name = sended_mesage.document.file_name
                                
                                current_file = dir_name + "\\" + file_name
                                repo.update_data(m=CourseModel(current_file=current_file,  isActive=True))
                                                     
                        
                        else:
                                a = 0
                                b = 10
                                while True: 
                                        if len(documents) < 10:
                                        
                                                sended_mesages = await client.send_media_group(chat_id=chat_id,
                                                                              media=documents[a:b])

                                                file_name = sended_mesages[-1].document.file_name

                                                caption = f" \n \n [🔝 к оглавлению🔝]({teamplate_link})"

                                                last_id =sended_mesages[-1].id

                                                await client.edit_message_caption(chat_id=chat_id,
                                                                            message_id=last_id,
                                                                            caption=caption)


                                                current_file = dir_name + "\\" + file_name
                                                repo.update_data(m=CourseModel(current_file=current_file,  isActive=True))

                                                break
                                        
                                        if b > len(documents):
                                                b = len(documents)
                                                if not documents[a:b]:
                                                        break
                                                sended_mesages = await client.send_media_group(chat_id=chat_id,
                                                                              media=documents[a:b])

                                                file_name = sended_mesages[-1].document.file_name

                                                caption = f" \n \n [🔝 к оглавлению🔝]({teamplate_link})"

                                                last_id =sended_mesages[-1].id

                                                await client.edit_message_caption(chat_id=chat_id,
                                                                            message_id=last_id,
                                                                            caption=caption)
                                                current_file = dir_name + "\\" + file_name
                                                repo.update_data(m=CourseModel(current_file=current_file,  isActive=True))

                                                break
                                        
                                        
                                        
                                        sended_mesages = await client.send_media_group(chat_id=chat_id,
                                                                      media=documents[a:b])

                                        file_name = sended_mesages[-1].document.file_name

                                        caption = f" \n \n [🔝 к оглавлению🔝]({teamplate_link})"

                                        last_id =sended_mesages[-1].id

                                        await client.edit_message_caption(chat_id=chat_id,
                                                                       message_id=last_id,
                                                                       caption=caption)
                                        current_file = dir_name + "\\" + file_name
                                        repo.update_data(m=CourseModel(current_file=current_file,  isActive=True))

                                        b+=10
                                        a+=10       
                                
