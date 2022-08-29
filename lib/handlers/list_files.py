import re
import struct
from loader import repo
from pyrogram import Client, filters, types
# queue_list [[gen_name, name_fold, [list_files_names], [list_path]]]



class spliter():
    def _add_surrogate(self, text):
        return ''.join(
        # SMP -> Surrogate Pairs (Telegram offsets are calculated with these).
        # See https://en.wikipedia.org/wiki/Plane_(Unicode)#Overview for more.
        ''.join(chr(y) for y in struct.unpack('<HH', x.encode('utf-16le')))
        if (0x10000 <= ord(x) <= 0x10FFFF) else x for x in text
        )


    def _del_surrogate(self, text):
        return text.encode('utf-16', 'surrogatepass').decode('utf-16')
    
    
    def _split_text(self, text, *, limit=4096,split_at=(r'\n', r'\s', '.')):

        text = self._add_surrogate(text)
        split_at = tuple(map(re.compile, split_at))

        while True:
            cur_limit = limit

            if len(text) <= cur_limit:
                break

            for split in split_at:
                for i in reversed(range(cur_limit)):
                    m = split.match(text, pos=i)
                    if m:
                        cur_text, new_text = text[:m.end()], text[m.end():]
                        yield self._del_surrogate(cur_text),
                        text = new_text
                        break
                else:
                    continue
                break
            else:
                # Can't find where to split, just return the remaining text and entities
                break

        yield self._del_surrogate(text)
    
    







class HeadlinesGen:

    
    async def parse_to_list_headlines(client: Client,chat_id: int,data_list: list):
        list_headlines = []
        list_gen_names = []
        for data in data_list:
            gen_name = data[0]
            fold_name = data[1]
            list_gen_names.append(gen_name)
            try:
                if gen_name == list_gen_names[-2]:
                    r_fold_name= str(fold_name).replace(" ", "_")
                    list_headlines.append(f"    #{r_fold_name} 👉Перейти👈 \n")
                    list_headlines.append('\n')
                else:
                    r_gen_name= str(gen_name).replace(" ", "_")
                    r_fold_name= str(fold_name).replace(" ", "_")
                    list_headlines.append(f" #{r_gen_name} :\n")
                    list_headlines.append(f"    #{r_fold_name} 👉Перейти👈 \n")
                    list_headlines.append('\n')
            except:
                r_gen_name= str(gen_name).replace(" ", "_")
                list_headlines.append(f" #{r_gen_name} : \n")
                r_fold_name= str(fold_name).replace(" ", "_")
                list_headlines.append(f"    #{r_fold_name} 👉Перейти👈 \n")

        text_message = "".join(list_headlines)
        for text in spliter()._split_text(text_message): 
            if type(text) == tuple:
                text = text[0]           
            await client.send_message(chat_id, text=text)
            

    
    #TODO: Refactor to other place 
    @Client.on_message(filters.channel & filters.command('get_heads_list'))
    async def parse_to_message_headlines(self,client: Client, message: types.Message):
        data_list = repo.get_values(getQueue=True)
        list_heads = self.parse_to_list_headlines(data_list=data_list)
        list_to_str = "".join(list_heads)
        await client.send_message(chat_id=message.chat.id,text=list_to_str)
    #TODO: Refactor to other place  






class files_list:
    
    
    
    async def createMessage(self, client: Client,chat_id: int, files_names_list:list) -> list:
        list_teamplates = []
        text_lenght = "[](https://t.me/c/1746116176/1164)".join(files_names_list)
        text_lenght = text_lenght +  's' *300
        for i in spliter()._split_text(text_lenght):
            msg = await client.send_message(chat_id=chat_id,text= '```Teamplate message```')
            list_teamplates.append(msg.id)
        return list_teamplates
    
    
    async def editMessage(self,client: Client,chat_id,msg_ids: list,data_list: list,files_list:list, link_list):
        message = []
        link_list.reverse()
        name_fold= str(data_list[1]).replace(" ","_")   
        gen_name = str(data_list[0]).replace(" ","_")   
        # heads 
        message.append(f"#{gen_name} \n")
        message.append(f'#{name_fold}: \n')
        message.append('\n')
        # queue_list [[gen_name, name_fold, [list_files_names], [list_path]]]       
        
        check_list =[]
        for video_file in files_list:
            if 'cap.txt' in video_file:
                continue
            if '.mp4' in video_file:
                check_list.append(video_file)
        
        for document_file in files_list:
            if 'cap.txt' in document_file:
                continue
            if '.mp4' in document_file:
                continue
            check_list.append(document_file)
            
        i = 0
        for file in check_list: 
            message.append(f" [{file}]({link_list[i]}) \n") 
            message.append( "\n")
            i +=1  
        text_message = "".join(message)
        t = 0
        for text in spliter()._split_text(text_message):
            if type(text) == tuple:
                text = text[0]       
            await client.edit_message_text(chat_id,msg_ids[t], text=text)
            t+=1
    
       
    async def get_link_from_files(self, client: Client, chat_id:int, file_names_list: list ) -> list:
        link_list = [] 
        
        check_list =[]
        
        for file in file_names_list:
            if 'cap.txt' in file:
                continue
            check_list.append(file)
        async for history_message  in client.get_chat_history(chat_id=chat_id,limit=len(check_list)):
            link_list.append(history_message.link)
        return link_list
    
    
    